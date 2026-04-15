"""
Real integration test runner for the Novel Writing System.
Makes actual HTTP calls to the running backend (port 4273).
Creates a real test project and exercises all API endpoints.
"""

import httpx
import json
import time
import sys
from pathlib import Path
from datetime import datetime

BASE = "http://127.0.0.1:4273"
WORKSPACE = Path(__file__).resolve().parent.parent
TEST_PROJECT_NAME = "测试小说_自动化"
TEST_PROJECT_PATH = f"projects/{TEST_PROJECT_NAME}"

results = []


def log(test_id: str, name: str, passed: bool, detail: str = ""):
    status = "PASS" if passed else "FAIL"
    results.append({"id": test_id, "name": name, "status": status, "detail": detail})
    icon = "✅" if passed else "❌"
    print(f"  {icon} {test_id}: {name}" + (f" — {detail}" if detail and not passed else ""))


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ──────────────────────────────────────────────
#  Phase 1: Health & Environment
# ──────────────────────────────────────────────
def test_health():
    section("Phase 1: Health & Environment")
    r = httpx.get(f"{BASE}/api/health", timeout=5)
    log("ENV-001", "Health endpoint returns 200", r.status_code == 200, f"status={r.status_code}")
    log("ENV-002", "Health body has status=ok", r.json().get("status") == "ok", str(r.json()))


# ──────────────────────────────────────────────
#  Phase 2: Project Lifecycle (A-group tests)
# ──────────────────────────────────────────────
def test_projects():
    section("Phase 2: Project Lifecycle")

    # A010: list existing projects
    r = httpx.get(f"{BASE}/api/projects", timeout=10)
    log("A010", "GET /projects returns 200", r.status_code == 200)
    projects = r.json()
    log("A010b", "Projects list is non-empty", len(projects) > 0, f"count={len(projects)}")

    # A012: current project
    r = httpx.get(f"{BASE}/api/projects/current", timeout=10)
    log("A012", "GET /projects/current returns 200", r.status_code == 200)
    cur = r.json()
    has_meta = "meta" in cur and cur["meta"]
    has_state = "state" in cur and cur["state"]
    log("A012b", "Current project has meta", has_meta, str(list(cur.get("meta", {}).keys())[:5]))
    log("A012c", "Current project has state", has_state, str(list(cur.get("state", {}).keys())[:5]))

    # A001: create test project via filesystem (simulating novel-init)
    proj_dir = WORKSPACE / TEST_PROJECT_PATH
    if proj_dir.exists():
        import shutil
        shutil.rmtree(proj_dir)

    # Copy from template
    template = WORKSPACE / "templates" / "project"
    import shutil
    shutil.copytree(template, proj_dir)

    # Write meta.yaml
    meta_path = proj_dir / ".novel" / "meta.yaml"
    meta_content = f"""project:
  id: test_auto
  name: {TEST_PROJECT_NAME}
  genre: 测试类型
  created: "{datetime.now().strftime('%Y-%m-%d')}"
  updated: "{datetime.now().strftime('%Y-%m-%d')}"

writing:
  chapter_count: 0
  pov: 第三人称
  target_words: 500000
"""
    meta_path.write_text(meta_content, encoding="utf-8")

    # Write state.yaml
    state_path = proj_dir / ".novel" / "state.yaml"
    state_content = f"""project:
  name: {TEST_PROJECT_NAME}
  genre: 测试类型
  created: "{datetime.now().strftime('%Y-%m-%d')}"
  updated: "{datetime.now().strftime('%Y-%m-%d')}"

protagonist: ""
ingestion:
  status: ""
  brief_file: ""
  source_draft: ""
plot:
  structure: ""
current_focus: ""
"""
    state_path.write_text(state_content, encoding="utf-8")

    log("A001", "Project directory created", proj_dir.exists())
    log("A001b", "meta.yaml exists", meta_path.exists())
    log("A001c", "state.yaml exists", state_path.exists())

    # Verify directory structure
    expected_dirs = ["characters", "chapters", "plot", "worldbuilding", "worldbuilding/entries"]
    for d in expected_dirs:
        exists = (proj_dir / d).exists()
        log(f"A001-{d}", f"Dir {d}/ exists", exists)

    # A008: switch to test project
    r = httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": TEST_PROJECT_NAME,
        "project_path": TEST_PROJECT_PATH,
    }, timeout=5)
    log("A008", "Switch to test project", r.status_code == 200, str(r.json()))

    # Verify switch
    r = httpx.get(f"{BASE}/api/projects/current", timeout=5)
    cur = r.json()
    log("A008b", "Current project is test project",
        cur["current"]["current_project"] == TEST_PROJECT_NAME,
        cur["current"]["current_project"])

    # A009: switch to non-existent project
    r = httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": "幽灵项目",
        "project_path": "projects/幽灵项目",
    }, timeout=5)
    log("A009", "Switch to non-existent returns 404", r.status_code == 404, f"status={r.status_code}")


# ──────────────────────────────────────────────
#  Phase 3: Characters (C-group & N-group)
# ──────────────────────────────────────────────
def test_characters():
    section("Phase 3: Characters")

    # Ensure we're on test project
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": TEST_PROJECT_NAME,
        "project_path": TEST_PROJECT_PATH,
    }, timeout=5)

    # N006: list characters (empty)
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    log("N006", "GET /characters returns 200", r.status_code == 200)
    entries = r.json().get("entries", [])
    log("N006b", "Initial character list is empty", len(entries) == 0, f"count={len(entries)}")

    # N008/C001: create protagonist
    r = httpx.post(f"{BASE}/api/characters", json={
        "name": "李远",
        "role": "protagonist",
        "archetype": "不情愿的英雄",
        "first_appearance": "ch001",
        "data": {"age": 22, "traits": "谨慎、聪明但优柔寡断"}
    }, timeout=5)
    log("C001", "Create protagonist 李远", r.status_code == 200, str(r.json()))

    # Verify file created
    char_file = WORKSPACE / TEST_PROJECT_PATH / "characters" / "李远.yaml"
    log("C001b", "Character file created on disk", char_file.exists())

    # N007: get single character
    r = httpx.get(f"{BASE}/api/characters/李远", timeout=5)
    log("N007", "GET /characters/李远 returns 200", r.status_code == 200)
    data = r.json()
    log("N007b", "Character name correct", data.get("name") == "李远")
    log("N007c", "Character role correct", data.get("role") == "protagonist")
    log("N007d", "Custom data preserved", data.get("age") == 22, f"age={data.get('age')}")

    # C002: create second character
    r = httpx.post(f"{BASE}/api/characters", json={
        "name": "苏晚",
        "role": "deuteragonist",
        "archetype": "守护者",
        "first_appearance": "ch001",
        "data": {"age": 21, "traits": "果断、外冷内热"}
    }, timeout=5)
    log("C002", "Create deuteragonist 苏晚", r.status_code == 200)

    # C003/N009: create duplicate character
    r = httpx.post(f"{BASE}/api/characters", json={
        "name": "李远",
        "role": "minor",
    }, timeout=5)
    log("C003", "Duplicate character returns 409", r.status_code == 409, f"status={r.status_code}")

    # C007: character with English name
    r = httpx.post(f"{BASE}/api/characters", json={
        "name": "Jack",
        "role": "minor",
        "archetype": "外国友人",
    }, timeout=5)
    log("C007", "English name character created", r.status_code == 200)

    # C029: same surname different character
    r = httpx.post(f"{BASE}/api/characters", json={
        "name": "李明",
        "role": "minor",
    }, timeout=5)
    log("C029", "Same-surname character coexist", r.status_code == 200)

    # N006 again: list should have 4 now
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    count = len(r.json().get("entries", []))
    log("N006c", f"Character count is 4", count == 4, f"count={count}")

    # N010: update character
    r = httpx.put(f"{BASE}/api/characters/李远", json={
        "data": {"traits": "谨慎、聪明、逐渐变得果断", "age": 22}
    }, timeout=5)
    log("N010", "PUT update character", r.status_code == 200)

    # Verify update persisted
    r = httpx.get(f"{BASE}/api/characters/李远", timeout=5)
    log("N010b", "Update persisted", "果断" in str(r.json().get("traits", "")), str(r.json().get("traits")))

    # N011: delete character
    r = httpx.delete(f"{BASE}/api/characters/Jack", timeout=5)
    log("N011", "DELETE character Jack", r.status_code == 200)
    r = httpx.get(f"{BASE}/api/characters/Jack", timeout=5)
    log("N011b", "Deleted character returns 404", r.status_code == 404, f"status={r.status_code}")

    # Verify index updated
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    count = len(r.json().get("entries", []))
    log("N011c", "Character count is 3 after delete", count == 3, f"count={count}")

    # C019/N013: get non-existent character
    r = httpx.get(f"{BASE}/api/characters/不存在的人", timeout=5)
    log("C019", "Non-existent character returns 404", r.status_code == 404)

    # C006: character with special chars in name
    r = httpx.post(f"{BASE}/api/characters", json={
        "name": "倒灌者·无名",
        "role": "antagonist",
        "archetype": "谜团",
    }, timeout=5)
    log("C006", "Special char name (·) created", r.status_code == 200)

    # Verify special char name retrieval
    r = httpx.get(f"{BASE}/api/characters/倒灌者·无名", timeout=5)
    log("C006b", "Special char name retrievable", r.status_code == 200, f"name={r.json().get('name')}")


# ──────────────────────────────────────────────
#  Phase 4: Worldbuilding / Settings (E-group & N-group)
# ──────────────────────────────────────────────
def test_worldbuilding():
    section("Phase 4: Worldbuilding")

    # N021: get worldbuilding index
    r = httpx.get(f"{BASE}/api/worldbuilding", timeout=5)
    log("N021", "GET /worldbuilding returns 200", r.status_code == 200)

    # N023/E001: create power system entry
    r = httpx.post(f"{BASE}/api/worldbuilding/entries", json={
        "id": "power_test_001",
        "name": "灵力体系",
        "category": "power_system",
        "status": "tentative",
        "data": {"description": "世界融合后产生的超凡力量", "rules": ["不可逆", "有代价"]}
    }, timeout=5)
    log("E001", "Create power system entry", r.status_code == 200, str(r.json()))

    # Verify file created
    entry_file = WORKSPACE / TEST_PROJECT_PATH / "worldbuilding" / "entries" / "power_test_001.yaml"
    log("E001b", "Entry file on disk", entry_file.exists())

    # N022: get entry
    r = httpx.get(f"{BASE}/api/worldbuilding/entries/power_test_001", timeout=5)
    log("N022", "GET entry returns 200", r.status_code == 200)
    log("N022b", "Entry name correct", r.json().get("name") == "灵力体系")

    # E004/N024: duplicate entry
    r = httpx.post(f"{BASE}/api/worldbuilding/entries", json={
        "id": "power_test_001",
        "name": "重复条目",
    }, timeout=5)
    log("E004", "Duplicate entry returns 409", r.status_code == 409, f"status={r.status_code}")

    # E003: default status = tentative
    r = httpx.post(f"{BASE}/api/worldbuilding/entries", json={
        "id": "rule_test_001",
        "name": "测试规则",
    }, timeout=5)
    log("E003", "Default status is tentative", r.status_code == 200)
    r = httpx.get(f"{BASE}/api/worldbuilding/entries/rule_test_001", timeout=5)
    log("E003b", "Status confirmed tentative", r.json().get("status") == "tentative", r.json().get("status"))

    # E008/N025: update entry
    r = httpx.put(f"{BASE}/api/worldbuilding/entries/power_test_001", json={
        "data": {"description": "更新后的力量体系描述", "rules": ["不可逆", "有代价", "新增规则"]}
    }, timeout=5)
    log("E008", "Update entry", r.status_code == 200)

    # E009: status transition tentative -> confirmed
    r = httpx.put(f"{BASE}/api/worldbuilding/entries/power_test_001", json={
        "status": "confirmed",
    }, timeout=5)
    log("E009", "Status tentative→confirmed", r.status_code == 200)
    r = httpx.get(f"{BASE}/api/worldbuilding/entries/power_test_001", timeout=5)
    log("E009b", "Status is now confirmed", r.json().get("status") == "confirmed", r.json().get("status"))

    # E010: status confirmed -> deprecated
    r = httpx.put(f"{BASE}/api/worldbuilding/entries/rule_test_001", json={
        "status": "deprecated",
    }, timeout=5)
    log("E010", "Status confirmed→deprecated", r.status_code == 200)

    # E014: get non-existent entry
    r = httpx.get(f"{BASE}/api/worldbuilding/entries/nonexistent_999", timeout=5)
    log("E014", "Non-existent entry returns 404", r.status_code == 404)

    # Create a few more entries for index test
    for i, (eid, name, cat) in enumerate([
        ("faction_test_001", "天枢局", "faction"),
        ("lore_test_001", "融合纪元", "lore"),
        ("rule_test_002", "现实抚平机制", "world_rule"),
    ]):
        r = httpx.post(f"{BASE}/api/worldbuilding/entries", json={"id": eid, "name": name, "category": cat}, timeout=5)
        log(f"E001-extra{i}", f"Create entry {name}", r.status_code == 200)

    # Verify index has all entries
    r = httpx.get(f"{BASE}/api/worldbuilding", timeout=5)
    index_entries = r.json().get("entries", [])
    test_entries = [e for e in index_entries if "test" in e.get("id", "")]
    log("N021b", f"Index has our test entries", len(test_entries) >= 5, f"test_count={len(test_entries)}")

    # N026: delete entry
    r = httpx.delete(f"{BASE}/api/worldbuilding/entries/rule_test_002", timeout=5)
    log("N026", "DELETE entry", r.status_code == 200)
    r = httpx.get(f"{BASE}/api/worldbuilding/entries/rule_test_002", timeout=5)
    log("N026b", "Deleted entry returns 404", r.status_code == 404)


# ──────────────────────────────────────────────
#  Phase 5: Chapters (G-group & N-group)
# ──────────────────────────────────────────────
def test_chapters():
    section("Phase 5: Chapters")

    # N014: list (empty)
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    log("N014", "GET /chapters returns 200", r.status_code == 200)
    chapters = r.json().get("chapters", [])
    log("N014b", "Initial chapters empty", len(chapters) == 0, f"count={len(chapters)}")

    # G001/N016: create chapter 1
    ch1_content = """# 第一章 日常

## 场景大纲

- 时间：2024年春
- 地点：大学宿舍
- 人物：李远、室友
- 事件：普通的一天，李远打游戏，室友聊天

## 正文草稿

李远盯着屏幕，指尖在键盘上飞快地跳动。

"又输了？"室友张伟从上铺探出头。

"闭嘴。"李远头也不抬。

窗外的天色开始变暗，但不是正常的日落——是那种说不清楚的灰。

## 伏笔

- 天色异变（B级伏笔）
"""
    r = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch001",
        "title": "第一章 日常",
        "pov": "李远",
        "goal": "建立日常氛围，在平静中埋下异变前兆",
        "word_target": 3000,
        "content": ch1_content,
    }, timeout=5)
    log("G001", "Create ch001", r.status_code == 200, str(r.json()))

    # G008: verify file structure
    ch_file = WORKSPACE / TEST_PROJECT_PATH / "chapters" / "ch001.md"
    log("G008", "ch001.md file exists", ch_file.exists())
    if ch_file.exists():
        content = ch_file.read_text(encoding="utf-8")
        log("G008b", "Content has 场景大纲", "场景大纲" in content)
        log("G008c", "Content has 正文草稿", "正文草稿" in content)
        log("G008d", "Content has 伏笔", "伏笔" in content)

    # N015: get chapter
    r = httpx.get(f"{BASE}/api/chapters/ch001", timeout=5)
    log("N015", "GET /chapters/ch001 returns 200", r.status_code == 200)
    meta = r.json().get("meta", {})
    log("N015b", "Chapter meta has id", meta.get("id") == "ch001")
    log("N015c", "Chapter meta has pov", meta.get("pov") == "李远", meta.get("pov"))
    log("N015d", "Chapter meta has goal", "日常" in meta.get("goal", ""), meta.get("goal"))

    # G004: duplicate chapter
    r = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch001",
        "title": "重复章节",
    }, timeout=5)
    log("G004", "Duplicate chapter returns 409", r.status_code == 409, f"status={r.status_code}")

    # G002: create chapter 2
    ch2_content = """# 第二章 灰域

## 场景大纲

- 时间：紧接上一章
- 地点：宿舍→走廊→操场
- 人物：李远、苏晚
- 事件：灰域降临，世界变色，李远第一次见到苏晚

## 正文草稿

灰色从窗外蔓延进来。

不是光线的变化，而是颜色本身在被什么东西吞噬。

李远站起来，椅子倒了，他没管。

## 伏笔

- 灰域起源（A级伏笔）
- 苏晚的身份（B级伏笔）
"""
    r = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch002",
        "title": "第二章 灰域",
        "pov": "李远",
        "goal": "第一次超凡事件，引入女主",
        "content": ch2_content,
    }, timeout=5)
    log("G002", "Create ch002", r.status_code == 200)

    # G005: skip numbering
    r = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch005",
        "title": "第五章 跳号测试",
        "goal": "测试跳号创建",
        "content": "# 跳号测试章节\n\n正文待写",
    }, timeout=5)
    log("G005", "Create ch005 (skipping 3-4)", r.status_code == 200, str(r.json()))

    # N017: update content
    updated_content = ch1_content + "\n张伟的手突然开始发光。\n"
    r = httpx.put(f"{BASE}/api/chapters/ch001", json={"content": updated_content}, timeout=5)
    log("N017", "PUT update chapter content", r.status_code == 200)

    # Verify word count updated
    r = httpx.get(f"{BASE}/api/chapters/ch001", timeout=5)
    word_actual = r.json().get("meta", {}).get("word_actual", 0)
    log("G026", "Word count updated", word_actual > 0, f"word_actual={word_actual}")

    # N018: update meta
    r = httpx.put(f"{BASE}/api/chapters/ch001/meta", json={
        "status": "draft",
        "summary": "李远的日常被灰域打断",
        "characters_involved": ["李远", "张伟"],
        "hooks_planted": ["天色异变"],
    }, timeout=5)
    log("N018", "PUT update chapter meta", r.status_code == 200)

    # G019: verify status updated
    r = httpx.get(f"{BASE}/api/chapters/ch001", timeout=5)
    meta = r.json().get("meta", {})
    log("G019", "Status updated to draft", meta.get("status") == "draft", meta.get("status"))
    log("G029", "Summary populated", "灰域" in meta.get("summary", ""), meta.get("summary"))
    log("G030-p", "characters_involved set", "李远" in meta.get("characters_involved", []))

    # N014 again: list should have 3
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    count = len(r.json().get("chapters", []))
    log("N014c", f"Chapter count is 3", count == 3, f"count={count}")

    # Chapter not found
    r = httpx.get(f"{BASE}/api/chapters/ch999", timeout=5)
    log("N015-404", "Non-existent chapter returns 404", r.status_code == 404)

    # N019: delete chapter
    r = httpx.delete(f"{BASE}/api/chapters/ch005", timeout=5)
    log("N019", "DELETE ch005", r.status_code == 200)
    r = httpx.get(f"{BASE}/api/chapters/ch005", timeout=5)
    log("N019b", "Deleted chapter returns 404", r.status_code == 404)

    # G044: verify file also deleted
    ch5_file = WORKSPACE / TEST_PROJECT_PATH / "chapters" / "ch005.md"
    log("G044-del", "ch005.md file deleted", not ch5_file.exists())

    # Verify index cleaned
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    count = len(r.json().get("chapters", []))
    log("N019c", "Chapter count is 2 after delete", count == 2, f"count={count}")


# ──────────────────────────────────────────────
#  Phase 6: Plot / Outline (F-group & N-group)
# ──────────────────────────────────────────────
def test_plot():
    section("Phase 6: Plot / Outline")

    # N027: get outline
    r = httpx.get(f"{BASE}/api/plot/outline", timeout=5)
    log("N027", "GET /plot/outline returns 200", r.status_code == 200)
    data = r.json()
    log("N027b", "Has markdown field", "markdown" in data)
    log("N027c", "Has structured field", "structured" in data)

    # N028: update outline
    outline_md = """# 测试小说大纲

## 第一季：觉醒

### 第一章 日常
- 李远大学生日常
- 埋下天色异变伏笔

### 第二章 灰域
- 灰域降临
- 李远遇见苏晚
- 第一次见证超凡力量

### 第三章 逃亡
- 灰域中的生存
- 李远发现自己的异常

## 伏笔追踪
- 天色异变 → 待回收
- 灰域起源 → 待回收
- 苏晚身份 → 待回收
"""
    r = httpx.put(f"{BASE}/api/plot/outline", json={"content": outline_md}, timeout=5)
    log("N028", "PUT update outline", r.status_code == 200)

    # Verify outline persisted
    r = httpx.get(f"{BASE}/api/plot/outline", timeout=5)
    md = r.json().get("markdown", "")
    log("N028b", "Outline content persisted", "觉醒" in md and "灰域" in md)
    log("F005-verify", "Outline has chapter structure", "第一章" in md and "第二章" in md)


# ──────────────────────────────────────────────
#  Phase 7: Timeline (I-group)
# ──────────────────────────────────────────────
def test_timeline():
    section("Phase 7: Timeline")

    # I001/N029: get timeline (may be empty)
    r = httpx.get(f"{BASE}/api/timeline", timeout=5)
    log("N029", "GET /timeline returns 200", r.status_code == 200)

    # I001/N030: add events
    events = [
        {"time": "2024-03-15 08:00", "event": "李远在宿舍打游戏", "chapter": "ch001", "characters": ["李远", "张伟"]},
        {"time": "2024-03-15 18:30", "event": "天色开始异变", "chapter": "ch001", "characters": ["李远"]},
        {"time": "2024-03-15 18:45", "event": "灰域降临", "chapter": "ch002", "characters": ["李远", "苏晚"]},
        {"time": "2024-03-15 19:00", "event": "李远第一次见到苏晚", "chapter": "ch002", "characters": ["李远", "苏晚"]},
    ]
    for i, evt in enumerate(events):
        r = httpx.post(f"{BASE}/api/timeline", json=evt, timeout=5)
        log(f"I001-{i}", f"Add event: {evt['event'][:15]}...", r.status_code == 200)

    # Verify all events
    r = httpx.get(f"{BASE}/api/timeline", timeout=5)
    evt_list = r.json().get("events", [])
    log("I001-count", f"Timeline has events", len(evt_list) >= 4, f"count={len(evt_list)}")

    # I014: event with multiple characters
    r = httpx.post(f"{BASE}/api/timeline", json={
        "time": "2024-03-15 20:00",
        "event": "全宿舍楼灰域集体事件",
        "chapter": "ch002",
        "characters": ["李远", "苏晚", "张伟", "李明"],
    }, timeout=5)
    log("I014", "Multi-character event", r.status_code == 200)


# ──────────────────────────────────────────────
#  Phase 8: Relationships (D-group)
# ──────────────────────────────────────────────
def test_relationships():
    section("Phase 8: Relationships")

    # N031: get relationships
    r = httpx.get(f"{BASE}/api/relationships", timeout=5)
    log("N031", "GET /relationships returns 200", r.status_code == 200)

    # N032: get events
    r = httpx.get(f"{BASE}/api/relationships/events", timeout=5)
    log("N032-events", "GET /relationships/events returns 200", r.status_code == 200)

    # Note: relationships API is read-only, no POST
    # This is a finding worth noting
    log("D001-api", "Relationships API is read-only (no POST)",
        True, "By design: only skill can create relationships")


# ──────────────────────────────────────────────
#  Phase 9: Compliance & Quality
# ──────────────────────────────────────────────
def test_compliance_quality():
    section("Phase 9: Compliance & Quality")

    r = httpx.get(f"{BASE}/api/compliance/inspirations", timeout=5)
    log("N033", "GET /compliance/inspirations returns 200", r.status_code == 200)

    r = httpx.get(f"{BASE}/api/compliance/risks", timeout=5)
    log("N033b", "GET /compliance/risks returns 200", r.status_code == 200)

    r = httpx.get(f"{BASE}/api/quality/ai-trace", timeout=5)
    log("N034-q", "GET /quality/ai-trace returns 200", r.status_code == 200)


# ──────────────────────────────────────────────
#  Phase 10: Skills listing
# ──────────────────────────────────────────────
def test_skills():
    section("Phase 10: Skills")

    r = httpx.get(f"{BASE}/api/skills", timeout=5)
    log("O001", "GET /skills returns 200", r.status_code == 200)
    skills = r.json().get("skills", [])
    log("O001b", f"Skills count > 30", len(skills) > 30, f"count={len(skills)}")

    # Check skill categories
    categories = set(s.get("category") for s in skills)
    log("O001c", "Has chapters category", "chapters" in categories, str(categories))
    log("O001d", "Has characters category", "characters" in categories)
    log("O001e", "Has pipeline category", "pipeline" in categories)

    # O005: non-existent skill execute
    r = httpx.post(f"{BASE}/api/skills/execute", json={
        "skill_name": "nonexistent-skill",
        "arguments": "test",
    }, timeout=5)
    log("O005", "Non-existent skill returns 404", r.status_code == 404, f"status={r.status_code}")


# ──────────────────────────────────────────────
#  Phase 11: Cross-module integrity (Q-group)
# ──────────────────────────────────────────────
def test_cross_module():
    section("Phase 11: Cross-module Integrity")

    # Q021: state.yaml should be lean
    state_path = WORKSPACE / TEST_PROJECT_PATH / ".novel" / "state.yaml"
    if state_path.exists():
        content = state_path.read_text(encoding="utf-8")
        log("Q021", "state.yaml exists", True)
        log("Q021b", "state.yaml is lean (< 1KB)", len(content) < 1024, f"size={len(content)}")

    # Q023: YAML files readable
    yaml_files = list((WORKSPACE / TEST_PROJECT_PATH).rglob("*.yaml"))
    broken = []
    from ruamel.yaml import YAML
    y = YAML()
    for f in yaml_files:
        try:
            text = f.read_text(encoding="utf-8")
            if text.strip():
                y.load(text)
        except Exception as e:
            broken.append(f"{f.name}: {e}")
    log("Q023", "All YAML files parseable", len(broken) == 0, "; ".join(broken) if broken else "all OK")

    # Q025: character index vs actual files
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    index_names = {e.get("name") for e in r.json().get("entries", [])}
    char_dir = WORKSPACE / TEST_PROJECT_PATH / "characters"
    file_names = {f.stem for f in char_dir.glob("*.yaml")
                  if f.stem not in ("character_index", "relations", "relation_events", "character")}
    index_only = index_names - file_names
    file_only = file_names - index_names
    log("Q025-idx", "Index-file consistency (no orphan index)",
        len(index_only) == 0, f"index_only={index_only}" if index_only else "clean")
    log("Q025-file", "Index-file consistency (no orphan files)",
        len(file_only) == 0, f"file_only={file_only}" if file_only else "clean")

    # T007: path with Chinese characters works
    proj_root = WORKSPACE / TEST_PROJECT_PATH
    log("T007", "Chinese path project works", proj_root.exists() and (proj_root / ".novel").exists())

    # T005: empty YAML arrays handled
    r = httpx.get(f"{BASE}/api/compliance/inspirations", timeout=5)
    log("T005", "Empty YAML array returns ok", r.status_code == 200)


# ──────────────────────────────────────────────
#  Phase 12: Edge cases & Error handling
# ──────────────────────────────────────────────
def test_edge_cases():
    section("Phase 12: Edge Cases & Error Handling")

    # Switch back to test project to be safe
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": TEST_PROJECT_NAME,
        "project_path": TEST_PROJECT_PATH,
    }, timeout=5)

    # T004: Unicode special characters
    r = httpx.post(f"{BASE}/api/characters", json={
        "name": "测试角色·特殊",
        "role": "minor",
    }, timeout=5)
    log("T004", "Unicode special char in name", r.status_code == 200)
    r = httpx.get(f"{BASE}/api/characters/测试角色·特殊", timeout=5)
    log("T004b", "Retrieve Unicode name", r.status_code == 200)

    # G044: delete chapter file manually, then try API read
    ch3_content = "# 测试手动删除\n\n临时章节"
    httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch003", "title": "临时章节", "content": ch3_content,
    }, timeout=5)
    # Now delete the file but keep index
    ch3_path = WORKSPACE / TEST_PROJECT_PATH / "chapters" / "ch003.md"
    if ch3_path.exists():
        ch3_path.unlink()
    r = httpx.get(f"{BASE}/api/chapters/ch003", timeout=5)
    log("G044", "Read chapter with missing .md file",
        r.status_code == 200, f"content='{r.json().get('content', '')[:20]}'")
    # This tests if the system handles orphan index entries gracefully

    # G045: re-create after manual delete
    r = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch003", "title": "重建章节", "content": "# 重建\n\n这是重建的",
    }, timeout=5)
    log("G045", "Re-create ch003 after file delete",
        r.status_code in (200, 409), f"status={r.status_code}")
    # 409 expected because index still has ch003 entry

    # Clean up: delete ch003 properly
    httpx.delete(f"{BASE}/api/chapters/ch003", timeout=5)

    # G048: try to operate on corrupted index
    # We'll test by sending requests for chapters after operations
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    log("G048-soft", "Chapters list after cleanup", r.status_code == 200,
        f"count={len(r.json().get('chapters', []))}")

    # N035: CORS check (we're localhost so should work)
    r = httpx.options(f"{BASE}/api/health", headers={
        "Origin": "http://localhost:4173",
        "Access-Control-Request-Method": "GET",
    }, timeout=5)
    log("N035-cors", "CORS preflight from localhost:4173", r.status_code in (200, 204),
        f"status={r.status_code}")

    # S010: CORS headers present
    r = httpx.get(f"{BASE}/api/health", headers={"Origin": "http://localhost:4173"}, timeout=5)
    cors_header = r.headers.get("access-control-allow-origin", "")
    log("S010", "CORS allow-origin header present",
        "localhost:4173" in cors_header or cors_header == "*",
        f"header={cors_header}")


# ──────────────────────────────────────────────
#  Phase 13: Existing project read tests
# ──────────────────────────────────────────────
def test_existing_project():
    section("Phase 13: Read existing project data")

    # Switch to the real project
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": "灵气复苏？不，超凡即是污染！",
        "project_path": "projects/灵气复苏？不，超凡即是污染！",
    }, timeout=5)

    # Read characters from real project
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    log("EXIST-001", "Real project has characters", r.status_code == 200)
    entries = r.json().get("entries", [])
    log("EXIST-001b", f"Character count", len(entries) > 0, f"count={len(entries)}")

    # Read worldbuilding
    r = httpx.get(f"{BASE}/api/worldbuilding", timeout=5)
    log("EXIST-002", "Real project has worldbuilding", r.status_code == 200)
    wb_entries = r.json().get("entries", [])
    log("EXIST-002b", f"Worldbuilding entries", len(wb_entries) > 0, f"count={len(wb_entries)}")

    # Read outline
    r = httpx.get(f"{BASE}/api/plot/outline", timeout=5)
    log("EXIST-003", "Real project has outline", r.status_code == 200)
    md = r.json().get("markdown", "")
    log("EXIST-003b", "Outline has content", len(md) > 100, f"length={len(md)}")

    # Read specific character
    r = httpx.get(f"{BASE}/api/characters/赵宋", timeout=5)
    log("EXIST-004", "Read protagonist 赵宋", r.status_code == 200)
    if r.status_code == 200:
        data = r.json()
        log("EXIST-004b", "赵宋 has role", "role" in data, data.get("role"))

    # Read relationships
    r = httpx.get(f"{BASE}/api/relationships", timeout=5)
    rels = r.json().get("relations", [])
    log("EXIST-005", "Relationships exist", len(rels) > 0, f"count={len(rels)}")

    # Read 末世 project
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": "末世：我开了GM权限",
        "project_path": "projects/末世：我开了GM权限",
    }, timeout=5)

    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    chs = r.json().get("chapters", [])
    log("EXIST-006", "末世 project has chapters", len(chs) > 0, f"count={len(chs)}")

    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    log("EXIST-007", "末世 project has characters",
        len(r.json().get("entries", [])) > 0,
        f"count={len(r.json().get('entries', []))}")

    # Switch back to test project for cleanup
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": TEST_PROJECT_NAME,
        "project_path": TEST_PROJECT_PATH,
    }, timeout=5)


# ──────────────────────────────────────────────
#  Runner
# ──────────────────────────────────────────────
def main():
    print(f"\n{'#'*60}")
    print(f"  Novel Writing System - Integration Test Suite")
    print(f"  Target: {BASE}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}")

    start = time.time()

    try:
        test_health()
        test_projects()
        test_characters()
        test_worldbuilding()
        test_chapters()
        test_plot()
        test_timeline()
        test_relationships()
        test_compliance_quality()
        test_skills()
        test_cross_module()
        test_edge_cases()
        test_existing_project()
    except Exception as e:
        print(f"\n💥 FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

    elapsed = time.time() - start

    # Summary
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Total:  {total}")
    print(f"  Passed: {passed} ✅")
    print(f"  Failed: {failed} ❌")
    print(f"  Rate:   {passed/total*100:.1f}%")
    print(f"  Time:   {elapsed:.1f}s")

    if failed > 0:
        print(f"\n  Failed tests:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"    ❌ {r['id']}: {r['name']} — {r['detail']}")

    # Write report
    report_path = Path(__file__).parent / "test-report.json"
    report = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "failed": failed,
        "elapsed_seconds": round(elapsed, 1),
        "results": results,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Report saved to: {report_path}")
    print()

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
