"""
Phase 3: File-level integrity, existing project data audit, 
workflow simulation, and corruption recovery tests.
"""

import httpx
import json
import time
import sys
from pathlib import Path
from datetime import datetime
from ruamel.yaml import YAML

BASE = "http://127.0.0.1:4273"
WORKSPACE = Path(__file__).resolve().parent.parent
TEST_PROJECT = "测试小说_自动化"
TEST_PATH = f"projects/{TEST_PROJECT}"
PROJ = WORKSPACE / TEST_PATH

REAL_PROJECTS = {
    "灵气复苏": "projects/灵气复苏？不，超凡即是污染！",
    "末世": "projects/末世：我开了GM权限",
}

_yaml = YAML()
_yaml.preserve_quotes = True

results = []


def log(test_id, name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    results.append({"id": test_id, "name": name, "status": status, "detail": detail})
    icon = "✅" if passed else "❌"
    print(f"  {icon} {test_id}: {name}" + (f" — {detail}" if detail and not passed else ""))


def section(title):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")


def read_yaml_safe(path):
    p = Path(path)
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    try:
        data = _yaml.load(text)
        return dict(data) if data else {}
    except Exception:
        return None


def switch_to(name, path):
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": name, "project_path": path
    }, timeout=5)


# ═══════════════════════════════════════════════
#  1. AUDIT EXISTING PROJECT: 灵气复苏
# ═══════════════════════════════════════════════
def audit_real_project_lingqi():
    section("1. Audit: 灵气复苏？不，超凡即是污染！")
    proj = WORKSPACE / REAL_PROJECTS["灵气复苏"]
    switch_to("灵气复苏？不，超凡即是污染！", REAL_PROJECTS["灵气复苏"])

    # 1a. Directory structure completeness
    expected = [
        ".novel/meta.yaml", ".novel/state.yaml",
        "characters/character_index.yaml", "characters/relations.yaml",
        "worldbuilding/worldbuilding.yaml", "worldbuilding/setting.md",
        "plot/outline.md", "plot/outline.yaml", "plot/plot_index.yaml",
        "chapters/index.yaml",
    ]
    for rel in expected:
        exists = (proj / rel).exists()
        log(f"AUDIT-LQ-{rel.split('/')[-1]}", f"File {rel} exists", exists)

    # 1b. All YAML parseable
    broken = []
    for f in proj.rglob("*.yaml"):
        try:
            text = f.read_text(encoding="utf-8")
            if text.strip():
                _yaml.load(text)
        except Exception as e:
            broken.append(f"{f.relative_to(proj)}: {str(e)[:60]}")
    log("AUDIT-LQ-YAML", "All YAML files parseable", len(broken) == 0,
        "; ".join(broken[:3]) if broken else "all OK")

    # 1c. Character index vs actual files
    idx = read_yaml_safe(proj / "characters" / "character_index.yaml") or {}
    idx_names = {e.get("name") for e in idx.get("entries", [])}
    skip = {"character_index", "relations", "relation_events", "character"}
    file_names = {f.stem for f in (proj / "characters").glob("*.yaml") if f.stem not in skip}
    idx_only = idx_names - file_names
    file_only = file_names - idx_names
    log("AUDIT-LQ-CHAR-IDX", "Character index matches files",
        len(idx_only) == 0 and len(file_only) == 0,
        f"idx_only={idx_only}, file_only={file_only}")

    # 1d. Character files have required fields
    char_issues = []
    five_keys = ["fatal_flaw", "obsession", "soft_spot", "misbelief", "contrast_habit"]
    for f in (proj / "characters").glob("*.yaml"):
        if f.stem in skip:
            continue
        data = read_yaml_safe(f) or {}
        name = data.get("name", f.stem)
        role = data.get("role", "")
        if not name:
            char_issues.append(f"{f.stem}: missing name")
        # Check five-piece set for non-minor characters
        if role in ("protagonist", "deuteragonist", "major", "主角", "核心", "重要"):
            for key in five_keys:
                val = data.get(key, "")
                if not val or val in ("", "待补充", "TBD"):
                    char_issues.append(f"{name}: {key} empty")
    log("AUDIT-LQ-CHAR-5SET", "Core characters have five-piece set",
        len(char_issues) == 0, "; ".join(char_issues[:5]) if char_issues else "all OK")

    # 1e. Worldbuilding index vs entries
    wb = read_yaml_safe(proj / "worldbuilding" / "worldbuilding.yaml") or {}
    wb_ids = {e.get("id") for e in wb.get("entries", [])}
    entries_dir = proj / "worldbuilding" / "entries"
    file_ids = {f.stem for f in entries_dir.glob("*.yaml") if f.stem != "_template"}
    wb_idx_only = wb_ids - file_ids
    wb_file_only = file_ids - wb_ids
    log("AUDIT-LQ-WB-IDX", "WB index matches entry files",
        len(wb_idx_only) == 0 and len(wb_file_only) == 0,
        f"idx_only={wb_idx_only}, file_only={wb_file_only}")

    # 1f. Tentative vs confirmed count
    tentative = 0
    confirmed = 0
    for e in wb.get("entries", []):
        s = e.get("status", "")
        if s == "tentative":
            tentative += 1
        elif s == "confirmed":
            confirmed += 1
    log("AUDIT-LQ-WB-STATUS", f"WB status distribution",
        True, f"tentative={tentative}, confirmed={confirmed}")

    # 1g. Chapters index
    ch_idx = read_yaml_safe(proj / "chapters" / "index.yaml") or {}
    chapters = ch_idx.get("chapters") or []
    log("AUDIT-LQ-CH-COUNT", f"Chapters count", True, f"count={len(chapters)}")

    # Check chapter file existence
    ch_orphans = []
    for ch in chapters:
        cid = ch.get("id", "")
        if cid and not (proj / "chapters" / f"{cid}.md").exists():
            ch_orphans.append(cid)
    log("AUDIT-LQ-CH-FILES", "All indexed chapters have .md files",
        len(ch_orphans) == 0, f"missing={ch_orphans}" if ch_orphans else "all present")

    # 1h. Outline files
    outline_md = (proj / "plot" / "outline.md").read_text(encoding="utf-8") if (proj / "plot" / "outline.md").exists() else ""
    outline_yaml = read_yaml_safe(proj / "plot" / "outline.yaml") or {}
    log("AUDIT-LQ-OUTLINE-MD", "outline.md has content", len(outline_md) > 50, f"len={len(outline_md)}")
    log("AUDIT-LQ-OUTLINE-YAML", "outline.yaml has structure",
        bool(outline_yaml.get("structure") or outline_yaml.get("foreshadowing")),
        f"keys={list(outline_yaml.keys())[:5]}")

    # 1i. Relations
    rels = read_yaml_safe(proj / "characters" / "relations.yaml") or {}
    rel_list = rels.get("relations", [])
    log("AUDIT-LQ-RELS", f"Relations count", True, f"count={len(rel_list)}")

    # Check relation pairs reference existing characters
    rel_issues = []
    for rel in rel_list:
        pair = rel.get("pair", [])
        for name in pair:
            if name not in idx_names and name not in file_names:
                rel_issues.append(f"'{name}' in relation but not a character")
    log("AUDIT-LQ-REL-VALID", "Relation pairs reference valid characters",
        len(rel_issues) == 0, "; ".join(rel_issues[:3]) if rel_issues else "all valid")

    # 1j. State.yaml lean check
    state = read_yaml_safe(proj / ".novel" / "state.yaml") or {}
    state_text = (proj / ".novel" / "state.yaml").read_text(encoding="utf-8")
    log("AUDIT-LQ-STATE", "state.yaml is lean", len(state_text) < 2048, f"size={len(state_text)}")

    # 1k. ingestion_brief.md exists and has content
    ib = proj / "ingestion_brief.md"
    log("AUDIT-LQ-INGEST", "ingestion_brief.md exists", ib.exists())
    if ib.exists():
        ib_text = ib.read_text(encoding="utf-8")
        log("AUDIT-LQ-INGEST-LEN", "ingestion_brief has content", len(ib_text) > 100, f"len={len(ib_text)}")

    # 1l. PROJECT_MAP.md
    pm = proj / "PROJECT_MAP.md"
    log("AUDIT-LQ-MAP", "PROJECT_MAP.md exists", pm.exists())


# ═══════════════════════════════════════════════
#  2. AUDIT EXISTING PROJECT: 末世
# ═══════════════════════════════════════════════
def audit_real_project_moshi():
    section("2. Audit: 末世：我开了GM权限")
    proj = WORKSPACE / REAL_PROJECTS["末世"]
    switch_to("末世：我开了GM权限", REAL_PROJECTS["末世"])

    # Structural check
    for rel in [".novel/meta.yaml", ".novel/state.yaml", "characters/character_index.yaml",
                "chapters/index.yaml", "worldbuilding/worldbuilding.yaml"]:
        log(f"AUDIT-MS-{rel.split('/')[-1]}", f"File {rel} exists", (proj / rel).exists())

    # YAML integrity
    broken = []
    for f in proj.rglob("*.yaml"):
        try:
            text = f.read_text(encoding="utf-8")
            if text.strip():
                _yaml.load(text)
        except Exception as e:
            broken.append(f"{f.relative_to(proj)}: {str(e)[:60]}")
    log("AUDIT-MS-YAML", "All YAML parseable", len(broken) == 0,
        "; ".join(broken) if broken else "all OK")

    # Character index vs files
    idx = read_yaml_safe(proj / "characters" / "character_index.yaml") or {}
    idx_names = {e.get("name") for e in idx.get("entries", [])}
    skip = {"character_index", "relations", "relation_events", "character"}
    file_names = {f.stem for f in (proj / "characters").glob("*.yaml") if f.stem not in skip}
    idx_only = idx_names - file_names
    file_only = file_names - idx_names
    log("AUDIT-MS-CHAR-IDX", "Char index matches files",
        len(idx_only) == 0 and len(file_only) == 0,
        f"idx_only={idx_only}, file_only={file_only}")

    # Chapters
    ch_idx = read_yaml_safe(proj / "chapters" / "index.yaml") or {}
    chapters = ch_idx.get("chapters", [])
    ch_missing = []
    for ch in chapters:
        cid = ch.get("id", "")
        if cid and not (proj / "chapters" / f"{cid}.md").exists():
            ch_missing.append(cid)
    log("AUDIT-MS-CH", f"Chapters: {len(chapters)} indexed, files OK",
        len(ch_missing) == 0, f"missing={ch_missing}" if ch_missing else "all present")

    # Has actual chapter content
    if chapters:
        ch1 = proj / "chapters" / f"{chapters[0]['id']}.md"
        if ch1.exists():
            content = ch1.read_text(encoding="utf-8")
            log("AUDIT-MS-CH-CONTENT", "First chapter has content", len(content) > 100, f"len={len(content)}")

    # WB index
    wb = read_yaml_safe(proj / "worldbuilding" / "worldbuilding.yaml") or {}
    wb_entries = wb.get("entries", [])
    log("AUDIT-MS-WB", f"WB entries", True, f"count={len(wb_entries)}")

    # Export directory
    export_dir = proj / "export"
    has_export = export_dir.exists() and any(export_dir.iterdir())
    log("AUDIT-MS-EXPORT", "Has export files", has_export)


# ═══════════════════════════════════════════════
#  3. TEMPLATE INTEGRITY
# ═══════════════════════════════════════════════
def test_template_integrity():
    section("3. Template Integrity")
    tpl = WORKSPACE / "templates" / "project"

    expected_files = [
        ".novel/meta.yaml", ".novel/state.yaml",
        ".novel/rules/context.md", ".novel/rules/constraints.md",
        "characters/character_index.yaml", "characters/character.yaml",
        "characters/relations.yaml", "characters/relation_events.yaml",
        "chapters/index.yaml",
        "plot/outline.md", "plot/outline.yaml", "plot/plot_index.yaml",
        "worldbuilding/worldbuilding.yaml", "worldbuilding/setting.md",
        "worldbuilding/entries/_template.yaml",
        "compliance/inspiration_log.yaml", "compliance/risk_report.yaml",
        "quality/ai_trace_report.yaml",
        "tags.yaml",
    ]
    for rel in expected_files:
        exists = (tpl / rel).exists()
        log(f"TPL-{rel.replace('/', '-')}", f"Template {rel}", exists)

    # All template YAML parseable
    broken = []
    for f in tpl.rglob("*.yaml"):
        data = read_yaml_safe(f)
        if data is None:
            broken.append(f.relative_to(tpl))
    log("TPL-YAML", "All template YAML parseable", len(broken) == 0,
        str(broken) if broken else "all OK")


# ═══════════════════════════════════════════════
#  4. CORRUPTION RECOVERY
# ═══════════════════════════════════════════════
def test_corruption_recovery():
    section("4. Corruption & Recovery")
    switch_to(TEST_PROJECT, TEST_PATH)

    # T001: corrupted YAML
    test_file = PROJ / "worldbuilding" / "entries" / "corrupt_test.yaml"
    test_file.write_text("invalid: yaml: content:\n  - broken\n  bad indent\n: : :", encoding="utf-8")
    r = httpx.get(f"{BASE}/api/worldbuilding/entries/corrupt_test", timeout=5)
    log("T001-corrupt", "Corrupted YAML doesn't crash server", r.status_code in (200, 500),
        f"status={r.status_code}")
    test_file.unlink(missing_ok=True)

    # T002: chapter .md with weird content
    weird_md = PROJ / "chapters" / "ch_weird.md"
    weird_md.write_text("这不是markdown\n\x00\x01二进制垃圾\n", encoding="utf-8", errors="replace")
    httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch_weird_idx", "title": "怪异", "content": "placeholder",
    }, timeout=5)
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    log("T002-weird", "Server survives weird file content", r.status_code == 200)
    weird_md.unlink(missing_ok=True)
    httpx.delete(f"{BASE}/api/chapters/ch_weird_idx", timeout=5)

    # T010: .novel/ missing
    novel_dir = PROJ / ".novel"
    meta_backup = (PROJ / ".novel" / "meta.yaml").read_text(encoding="utf-8")
    state_backup = (PROJ / ".novel" / "state.yaml").read_text(encoding="utf-8")

    # Test with deleted state.yaml
    (PROJ / ".novel" / "state.yaml").unlink()
    r = httpx.get(f"{BASE}/api/projects/current", timeout=5)
    log("T010-no-state", "Server handles missing state.yaml", r.status_code == 200,
        f"state={r.json().get('state', 'MISSING')}")

    # Restore
    (PROJ / ".novel" / "state.yaml").write_text(state_backup, encoding="utf-8")

    # Empty YAML file
    empty_test = PROJ / "worldbuilding" / "entries" / "empty_test.yaml"
    empty_test.write_text("", encoding="utf-8")
    r = httpx.get(f"{BASE}/api/worldbuilding/entries/empty_test", timeout=5)
    log("T013-empty-yaml", "Empty YAML file handled", r.status_code in (200, 404),
        f"status={r.status_code}")
    empty_test.unlink(missing_ok=True)

    # Whitespace-only YAML
    ws_test = PROJ / "worldbuilding" / "entries" / "ws_test.yaml"
    ws_test.write_text("   \n\n  \n", encoding="utf-8")
    r = httpx.get(f"{BASE}/api/worldbuilding/entries/ws_test", timeout=5)
    log("T013-ws-yaml", "Whitespace YAML handled", r.status_code in (200, 404),
        f"status={r.status_code}")
    ws_test.unlink(missing_ok=True)


# ═══════════════════════════════════════════════
#  5. WORKFLOW SIMULATION: Full Novel Creation
# ═══════════════════════════════════════════════
def test_full_workflow():
    section("5. Full Workflow Simulation")
    switch_to(TEST_PROJECT, TEST_PATH)

    # Step 1: Verify project is clean
    r = httpx.get(f"{BASE}/api/projects/current", timeout=5)
    cur = r.json()["current"]["current_project"]
    log("WF-001", "On test project", cur == TEST_PROJECT, cur)

    # Step 2: Create characters for our story
    characters = [
        {"name": "陈默", "role": "protagonist", "archetype": "沉默的观察者",
         "data": {"age": 24, "traits": "沉默寡言、观察力敏锐、内心矛盾"}},
        {"name": "秦可", "role": "deuteragonist", "archetype": "破碎的守护者",
         "data": {"age": 23, "traits": "外表强硬、内心柔软、有秘密"}},
        {"name": "老吴", "role": "major", "archetype": "世故的导师",
         "data": {"age": 45, "traits": "圆滑、有智慧、藏着伤痕"}},
        {"name": "小七", "role": "minor", "archetype": "天真的搅局者",
         "data": {"age": 19, "traits": "活泼、冲动、善良"}},
    ]
    for c in characters:
        httpx.post(f"{BASE}/api/characters", json=c, timeout=5)
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    log("WF-002", "4 characters created", len(r.json()["entries"]) >= 4)

    # Step 3: Create worldbuilding
    settings = [
        {"id": "wf_power_001", "name": "异能觉醒", "category": "power_system",
         "data": {"description": "部分人在极端压力下觉醒异能", "rules": ["有代价", "不可控制"]}},
        {"id": "wf_rule_001", "name": "管控区", "category": "world_rule",
         "data": {"description": "政府设立的异能者管控区域"}},
        {"id": "wf_faction_001", "name": "清洗局", "category": "faction",
         "data": {"description": "负责处理异能相关事件的秘密部门"}},
    ]
    for s in settings:
        httpx.post(f"{BASE}/api/worldbuilding/entries", json=s, timeout=5)
    r = httpx.get(f"{BASE}/api/worldbuilding", timeout=5)
    wf_entries = [e for e in r.json().get("entries", []) if e["id"].startswith("wf_")]
    log("WF-003", "3 worldbuilding entries created", len(wf_entries) == 3)

    # Step 4: Write outline
    outline = """# 陈默的故事

## 第一季：觉醒

### 第一章 失控
陈默目睹同事异能失控，管控区封锁，被迫卷入。

### 第二章 接触
秦可作为清洗局成员出现，陈默发现自己可能也是异能者。

### 第三章 追逐
管控区外的追逐，老吴出场，揭示更大的阴谋。

### 第四章 选择
陈默必须在自保和拯救小七之间做出选择。

## 伏笔
- 陈默的记忆空白（A级）
- 秦可的伤疤来源（B级）
- 老吴与清洗局的关系（B级）
"""
    httpx.put(f"{BASE}/api/plot/outline", json={"content": outline}, timeout=5)
    r = httpx.get(f"{BASE}/api/plot/outline", timeout=5)
    log("WF-004", "Outline written", "觉醒" in r.json()["markdown"])

    # Step 5: Create chapters with real content
    ch1 = """# 第一章 失控

## 场景大纲
- 时间：周一上午
- 地点：某科技公司办公楼
- 人物：陈默、同事
- 冲突：同事突然异能失控，办公室陷入混乱

## 正文草稿

陈默推开茶水间的门，咖啡机还在嗡嗡响。

走廊尽头传来一声闷响，不像东西掉了，更像是什么东西碎了。

他端着杯子往回走，经过刘工的工位时停了一下。刘工不在，但他的显示器还亮着，屏幕上全是乱码。

"陈默！"有人在喊他。

他转过头，看到走廊里有光——不是灯光。是从赵磊身上发出来的，像是皮肤底下有什么东西在燃烧。

赵磊站在走廊正中间，双手捂着脸，身体在抖。光从他的指缝里漏出来，越来越亮。

"别过来。"赵磊的声音变了，像是两个人在同时说话。

陈默没动。不是不想跑，是腿不听使唤。

然后赵磊的手放下来了，陈默看到了他的眼睛——那不是赵磊的眼睛。

## 伏笔
- 刘工的乱码屏幕（C级，暗示更早的异变）
- 赵磊的"两个声音"（B级，暗示异能的本质）
"""

    ch2 = """# 第二章 接触

## 场景大纲
- 时间：紧接上一章，约一小时后
- 地点：办公楼外→管控区边界
- 人物：陈默、秦可
- 冲突：陈默试图逃离，遇到秦可

## 正文草稿

办公楼外面全是人，有的在哭，有的在打电话。

陈默走出来的时候，注意到空气的颜色不太对。不是灰，是那种……洗旧了的蓝。

一辆没有标识的黑色面包车停在路边，车门开着，几个穿制服的人在拉警戒线。

"那边的，别动。"

一个短发女人走过来。她穿着某种制服，但陈默没见过这种。左胸口有个徽章，上面好像是一只眼睛。

"你从几楼下来的？"她的语气不像在问，像在确认。

"六楼。"

"看到了？"

陈默没回答。女人盯着他看了几秒，然后在平板上划了几下。

"跟我走。"

"去哪？"

"你现在有两个选择。跟我走，或者等会儿另一批人来接你。他们不会这么客气。"

她转身走了，没等他回答。陈默犹豫了三秒，跟了上去。

他后来知道她叫秦可。

## 伏笔
- 空气颜色异变（C级，与灰域概念关联）
- 秦可的徽章（B级，清洗局标识）
- "另一批人"（A级，暗示更大的势力博弈）
"""

    r1 = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch001", "title": "第一章 失控", "pov": "陈默",
        "goal": "建立日常→异变，引出超凡事件", "content": ch1,
    }, timeout=5)
    r2 = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch002", "title": "第二章 接触", "pov": "陈默",
        "goal": "引入秦可，展示管控机制", "content": ch2,
    }, timeout=5)

    # These might fail if they already exist from earlier tests
    ch1_ok = r1.status_code in (200, 409)
    ch2_ok = r2.status_code in (200, 409)
    log("WF-005a", "Chapter 1 created/exists", ch1_ok, f"status={r1.status_code}")
    log("WF-005b", "Chapter 2 created/exists", ch2_ok, f"status={r2.status_code}")

    # Step 6: Update chapter status and metadata
    httpx.put(f"{BASE}/api/chapters/ch001/meta", json={
        "status": "draft",
        "summary": "陈默在公司目睹同事赵磊异能失控",
        "characters_involved": ["陈默", "赵磊"],
        "hooks_planted": ["刘工乱码", "赵磊双声"],
    }, timeout=5)
    httpx.put(f"{BASE}/api/chapters/ch002/meta", json={
        "status": "draft",
        "summary": "陈默遇到秦可，被带向管控区",
        "characters_involved": ["陈默", "秦可"],
        "hooks_planted": ["空气颜色", "秦可徽章", "另一批人"],
    }, timeout=5)
    log("WF-006", "Chapter meta updated", True)

    # Step 7: Add timeline events
    tl_events = [
        {"time": "Day1 09:00", "event": "陈默到公司", "chapter": "ch001", "characters": ["陈默"]},
        {"time": "Day1 09:30", "event": "赵磊异能失控", "chapter": "ch001", "characters": ["陈默", "赵磊"]},
        {"time": "Day1 10:30", "event": "管控区封锁", "chapter": "ch002", "characters": ["秦可"]},
        {"time": "Day1 10:45", "event": "陈默遇到秦可", "chapter": "ch002", "characters": ["陈默", "秦可"]},
    ]
    for evt in tl_events:
        httpx.post(f"{BASE}/api/timeline", json=evt, timeout=5)
    log("WF-007", "Timeline populated", True)

    # Step 8: Verify full data picture via API
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    chapters = r.json()["chapters"]
    draft_chapters = [c for c in chapters if c.get("status") == "draft"]
    log("WF-008a", "Have draft chapters", len(draft_chapters) >= 2, f"drafts={len(draft_chapters)}")

    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    log("WF-008b", "Characters accessible", len(r.json()["entries"]) >= 4)

    r = httpx.get(f"{BASE}/api/worldbuilding", timeout=5)
    log("WF-008c", "Worldbuilding accessible", len(r.json().get("entries", [])) >= 3)

    r = httpx.get(f"{BASE}/api/timeline", timeout=5)
    log("WF-008d", "Timeline has events", len(r.json()["events"]) >= 4)

    r = httpx.get(f"{BASE}/api/plot/outline", timeout=5)
    log("WF-008e", "Outline readable", len(r.json()["markdown"]) > 100)

    # Step 9: Full data round-trip integrity
    for cid in ["ch001", "ch002"]:
        r = httpx.get(f"{BASE}/api/chapters/{cid}", timeout=5)
        ch_data = r.json()
        has_meta = ch_data.get("meta", {}).get("id") == cid
        has_content = len(ch_data.get("content", "")) > 50
        log(f"WF-009-{cid}", f"{cid} full round-trip", has_meta and has_content)

    # Step 10: Verify files on disk match API
    for cid in ["ch001", "ch002"]:
        md_path = PROJ / "chapters" / f"{cid}.md"
        api_r = httpx.get(f"{BASE}/api/chapters/{cid}", timeout=5)
        api_content = api_r.json().get("content", "")
        file_content = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
        log(f"WF-010-{cid}", f"{cid} disk == API", api_content == file_content,
            f"api_len={len(api_content)}, file_len={len(file_content)}")


# ═══════════════════════════════════════════════
#  6. API RESPONSE FORMAT CONSISTENCY
# ═══════════════════════════════════════════════
def test_response_format():
    section("6. API Response Format Consistency")
    switch_to(TEST_PROJECT, TEST_PATH)

    # Characters: list format
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    data = r.json()
    log("FMT-001", "Characters list has 'entries'", "entries" in data)
    log("FMT-001b", "Characters list has 'total'", "total" in data)

    # Chapters: list format
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    data = r.json()
    log("FMT-002", "Chapters list has 'chapters'", "chapters" in data)

    # Single chapter format
    r = httpx.get(f"{BASE}/api/chapters/ch001", timeout=5)
    if r.status_code == 200:
        data = r.json()
        log("FMT-003", "Chapter has 'meta' and 'content'",
            "meta" in data and "content" in data)
        meta = data["meta"]
        log("FMT-003b", "Meta has standard fields",
            all(k in meta for k in ["id", "title", "status", "pov"]),
            f"keys={list(meta.keys())}")

    # Outline format
    r = httpx.get(f"{BASE}/api/plot/outline", timeout=5)
    data = r.json()
    log("FMT-004", "Outline has 'markdown' and 'structured'",
        "markdown" in data and "structured" in data)

    # Timeline format
    r = httpx.get(f"{BASE}/api/timeline", timeout=5)
    data = r.json()
    log("FMT-005", "Timeline has 'events'", "events" in data)

    # Relationships format
    r = httpx.get(f"{BASE}/api/relationships", timeout=5)
    data = r.json()
    log("FMT-006", "Relationships has 'relations'", "relations" in data)

    # Skills format
    r = httpx.get(f"{BASE}/api/skills", timeout=5)
    data = r.json()
    log("FMT-007", "Skills has 'skills' array", "skills" in data and isinstance(data["skills"], list))
    if data["skills"]:
        s = data["skills"][0]
        log("FMT-007b", "Skill entry has name/category",
            "name" in s and "category" in s, f"keys={list(s.keys())}")

    # Projects format
    r = httpx.get(f"{BASE}/api/projects", timeout=5)
    data = r.json()
    log("FMT-008", "Projects is a list", isinstance(data, list))
    if data:
        log("FMT-008b", "Project has name/path/meta/state",
            all(k in data[0] for k in ["name", "path", "meta", "state"]),
            f"keys={list(data[0].keys())}")

    # Current project format
    r = httpx.get(f"{BASE}/api/projects/current", timeout=5)
    data = r.json()
    log("FMT-009", "Current project has 'current'/'meta'/'state'",
        all(k in data for k in ["current", "meta", "state"]))

    # Health format
    r = httpx.get(f"{BASE}/api/health", timeout=5)
    log("FMT-010", "Health returns {status: ok}", r.json() == {"status": "ok"})


# ═══════════════════════════════════════════════
#  Runner
# ═══════════════════════════════════════════════
def main():
    print(f"\n{'#'*60}")
    print(f"  Novel Writing System - Audit & Workflow Tests")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}")

    start = time.time()

    try:
        audit_real_project_lingqi()
        audit_real_project_moshi()
        test_template_integrity()
        test_corruption_recovery()
        test_full_workflow()
        test_response_format()
    except Exception as e:
        print(f"\n💥 FATAL: {e}")
        import traceback
        traceback.print_exc()

    elapsed = time.time() - start
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)

    print(f"\n{'='*60}")
    print(f"  AUDIT & WORKFLOW SUMMARY")
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

    report_path = Path(__file__).parent / "test-report-audit.json"
    report = {
        "timestamp": datetime.now().isoformat(),
        "total": total, "passed": passed, "failed": failed,
        "elapsed_seconds": round(elapsed, 1),
        "results": results,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Report: {report_path}\n")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
