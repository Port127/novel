"""
Deep integration tests – data integrity, edge cases, stress scenarios.
Operates on the test project created by run_tests.py.
"""

import httpx
import json
import shutil
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


def read_yaml_file(path):
    text = Path(path).read_text(encoding="utf-8")
    return dict(_yaml.load(text)) if text.strip() else {}


def ensure_test_project():
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": TEST_PROJECT, "project_path": TEST_PATH
    }, timeout=5)


# ──────────────────────────────────────────────
#  1. Orphan & Inconsistency Detection
# ──────────────────────────────────────────────
def test_orphans():
    section("1. Orphan & Inconsistency Detection")
    ensure_test_project()

    # G044: create chapter via API, then delete only the .md file
    httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch_orphan", "title": "孤儿测试", "content": "# 孤儿\n\n临时",
    }, timeout=5)
    md = PROJ / "chapters" / "ch_orphan.md"
    if md.exists():
        md.unlink()

    # Index still has ch_orphan but file is gone
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    ids = [c["id"] for c in r.json().get("chapters", [])]
    log("ORPHAN-001", "Index still lists orphan chapter", "ch_orphan" in ids)

    # Try to read orphan chapter – should not crash
    r = httpx.get(f"{BASE}/api/chapters/ch_orphan", timeout=5)
    log("ORPHAN-002", "Read orphan chapter doesn't crash", r.status_code == 200,
        f"content empty='{r.json().get('content', '')[:30]}'")

    # Try to update orphan chapter content – should create the file
    r = httpx.put(f"{BASE}/api/chapters/ch_orphan", json={"content": "# 恢复\n\n重新写入"}, timeout=5)
    log("ORPHAN-003", "PUT to orphan chapter succeeds", r.status_code == 200)
    log("ORPHAN-003b", "File recreated", md.exists())

    # Clean up
    httpx.delete(f"{BASE}/api/chapters/ch_orphan", timeout=5)

    # Q025: create character file without index entry
    rogue_char = PROJ / "characters" / "幽灵角色.yaml"
    rogue_char.write_text("name: 幽灵角色\nrole: ghost\n", encoding="utf-8")
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    names = [e["name"] for e in r.json().get("entries", [])]
    log("ORPHAN-004", "Rogue file NOT in index (expected orphan)",
        "幽灵角色" not in names, f"names={names}")
    rogue_char.unlink()

    # N012: delete character that has relations
    # First create a character and manually add a relation
    httpx.post(f"{BASE}/api/characters", json={"name": "关系测试A", "role": "minor"}, timeout=5)
    rel_path = PROJ / "characters" / "relations.yaml"
    rel_data = read_yaml_file(rel_path) if rel_path.exists() else {}
    rels = rel_data.get("relations", [])
    rels.append({"pair": ["关系测试A", "李远"], "type": "friend", "strength": 5})
    rel_data["relations"] = rels
    with open(rel_path, "w", encoding="utf-8") as f:
        _yaml.dump(rel_data, f)

    # Delete the character
    httpx.delete(f"{BASE}/api/characters/关系测试A", timeout=5)

    # Check if relation still exists (orphan relation)
    rel_data = read_yaml_file(rel_path)
    orphan_rels = [r for r in rel_data.get("relations", []) if "关系测试A" in str(r.get("pair", []))]
    log("ORPHAN-005", "Relation orphaned after char delete (API doesn't clean)",
        len(orphan_rels) > 0, f"orphan_count={len(orphan_rels)}")
    # This is a known gap: API delete doesn't clean relations

    # Clean the orphan relation
    rel_data["relations"] = [r for r in rel_data.get("relations", []) if "关系测试A" not in str(r.get("pair", []))]
    with open(rel_path, "w", encoding="utf-8") as f:
        _yaml.dump(rel_data, f)

    # N020: delete chapter that has hooks in outline.yaml
    httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch_hook", "title": "钩子章节", "content": "# 钩子\n\n有伏笔",
    }, timeout=5)
    outline_yaml = PROJ / "plot" / "outline.yaml"
    if outline_yaml.exists():
        oy = read_yaml_file(outline_yaml)
        foreshadowing = oy.get("foreshadowing", [])
        foreshadowing.append({
            "id": "hook_test_001", "name": "测试伏笔",
            "level": "B", "status": "planted", "plant_chapter": "ch_hook",
        })
        oy["foreshadowing"] = foreshadowing
        with open(outline_yaml, "w", encoding="utf-8") as f:
            _yaml.dump(oy, f)

    httpx.delete(f"{BASE}/api/chapters/ch_hook", timeout=5)
    oy = read_yaml_file(outline_yaml)
    orphan_hooks = [h for h in oy.get("foreshadowing", []) if h.get("plant_chapter") == "ch_hook"]
    log("ORPHAN-006", "Hook orphaned after chapter delete (API doesn't clean hooks)",
        len(orphan_hooks) > 0, f"orphan_hooks={len(orphan_hooks)}")

    # Clean up
    oy["foreshadowing"] = [h for h in oy.get("foreshadowing", []) if h.get("plant_chapter") != "ch_hook"]
    with open(outline_yaml, "w", encoding="utf-8") as f:
        _yaml.dump(oy, f)


# ──────────────────────────────────────────────
#  2. Batch & Stress
# ──────────────────────────────────────────────
def test_batch_stress():
    section("2. Batch & Stress")
    ensure_test_project()

    # Create 20 characters rapidly
    created = 0
    for i in range(20):
        r = httpx.post(f"{BASE}/api/characters", json={
            "name": f"批量角色_{i:03d}", "role": "minor",
        }, timeout=5)
        if r.status_code == 200:
            created += 1
    log("STRESS-001", f"Batch create 20 characters", created == 20, f"created={created}")

    # Verify index count
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    count = len(r.json().get("entries", []))
    log("STRESS-001b", f"Index reflects batch create", count >= 20, f"total={count}")

    # Read all 20 back
    read_ok = 0
    for i in range(20):
        r = httpx.get(f"{BASE}/api/characters/批量角色_{i:03d}", timeout=5)
        if r.status_code == 200:
            read_ok += 1
    log("STRESS-002", "All 20 characters readable", read_ok == 20, f"readable={read_ok}")

    # Delete all 20
    deleted = 0
    for i in range(20):
        r = httpx.delete(f"{BASE}/api/characters/批量角色_{i:03d}", timeout=5)
        if r.status_code == 200:
            deleted += 1
    log("STRESS-003", "All 20 deleted", deleted == 20, f"deleted={deleted}")

    # Verify index cleaned
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    remaining = [e for e in r.json().get("entries", []) if e["name"].startswith("批量角色")]
    log("STRESS-003b", "No batch chars in index", len(remaining) == 0, f"remaining={len(remaining)}")

    # Create 15 worldbuilding entries
    wb_created = 0
    for i in range(15):
        r = httpx.post(f"{BASE}/api/worldbuilding/entries", json={
            "id": f"stress_wb_{i:03d}", "name": f"压力设定{i}", "category": "world_rule",
        }, timeout=5)
        if r.status_code == 200:
            wb_created += 1
    log("STRESS-004", f"Batch create 15 WB entries", wb_created == 15, f"created={wb_created}")

    # Delete them
    for i in range(15):
        httpx.delete(f"{BASE}/api/worldbuilding/entries/stress_wb_{i:03d}", timeout=5)
    r = httpx.get(f"{BASE}/api/worldbuilding", timeout=5)
    stress_left = [e for e in r.json().get("entries", []) if "stress_wb" in e.get("id", "")]
    log("STRESS-004b", "All stress WB entries cleaned", len(stress_left) == 0, f"left={len(stress_left)}")

    # Create 10 chapters rapidly
    ch_created = 0
    for i in range(10, 20):
        r = httpx.post(f"{BASE}/api/chapters", json={
            "id": f"ch{i:03d}", "title": f"压力章节{i}", "content": f"# 章节{i}\n\n{'测试内容。' * 100}",
        }, timeout=5)
        if r.status_code == 200:
            ch_created += 1
    log("STRESS-005", f"Batch create 10 chapters", ch_created == 10, f"created={ch_created}")

    # Clean up
    for i in range(10, 20):
        httpx.delete(f"{BASE}/api/chapters/ch{i:03d}", timeout=5)


# ──────────────────────────────────────────────
#  3. Data Format & Content Edge Cases
# ──────────────────────────────────────────────
def test_data_edge_cases():
    section("3. Data Format & Content Edge Cases")
    ensure_test_project()

    # T004: emoji in character name
    r = httpx.post(f"{BASE}/api/characters", json={"name": "测试😀角色", "role": "minor"}, timeout=5)
    emoji_ok = r.status_code == 200
    log("T004-emoji", "Emoji in character name", emoji_ok, f"status={r.status_code}")
    if emoji_ok:
        r2 = httpx.get(f"{BASE}/api/characters/测试😀角色", timeout=5)
        log("T004-emoji-read", "Read emoji character", r2.status_code == 200)
        httpx.delete(f"{BASE}/api/characters/测试😀角色", timeout=5)

    # Very long character name
    long_name = "非常长的角色名字" * 10
    r = httpx.post(f"{BASE}/api/characters", json={"name": long_name, "role": "minor"}, timeout=5)
    log("T003-longname", "Very long character name", r.status_code in (200, 422, 500),
        f"status={r.status_code}")
    if r.status_code == 200:
        httpx.delete(f"{BASE}/api/characters/{long_name}", timeout=5)

    # Empty content chapter
    r = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch_empty", "title": "空内容", "content": "",
    }, timeout=5)
    log("T013-empty", "Empty content chapter created", r.status_code == 200)
    r = httpx.get(f"{BASE}/api/chapters/ch_empty", timeout=5)
    log("T013-empty-read", "Empty chapter readable", r.status_code == 200,
        f"content='{r.json().get('content', 'NONE')[:20]}'")
    httpx.delete(f"{BASE}/api/chapters/ch_empty", timeout=5)

    # Chapter with huge content (~50K chars)
    big_content = "# 巨型章节\n\n" + ("这是一段非常长的测试内容，用于验证系统对大文件的处理能力。" * 500)
    r = httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch_big", "title": "巨型章节", "content": big_content,
    }, timeout=10)
    log("T003-bigch", "50K char chapter created", r.status_code == 200,
        f"content_len={len(big_content)}")
    if r.status_code == 200:
        r = httpx.get(f"{BASE}/api/chapters/ch_big", timeout=10)
        log("T003-bigch-read", "Big chapter readable",
            len(r.json().get("content", "")) > 10000,
            f"read_len={len(r.json().get('content', ''))}")
        httpx.delete(f"{BASE}/api/chapters/ch_big", timeout=5)

    # Character with deeply nested data
    nested = {"name": "嵌套测试", "role": "minor", "data": {
        "personality": {"surface": "冷淡", "core": "温柔", "layers": [
            {"depth": 1, "trait": "防御性"},
            {"depth": 2, "trait": "恐惧"},
            {"depth": 3, "trait": "渴望认同"},
        ]},
        "history": [{"year": y, "event": f"事件{y}"} for y in range(2000, 2025)],
    }}
    r = httpx.post(f"{BASE}/api/characters", json=nested, timeout=5)
    log("T012-nested", "Deeply nested character data", r.status_code == 200)
    if r.status_code == 200:
        r = httpx.get(f"{BASE}/api/characters/嵌套测试", timeout=5)
        data = r.json()
        has_layers = "layers" in str(data)
        log("T012-nested-read", "Nested data preserved", has_layers, f"has_layers={has_layers}")
        httpx.delete(f"{BASE}/api/characters/嵌套测试", timeout=5)

    # Worldbuilding entry with special YAML chars in data
    r = httpx.post(f"{BASE}/api/worldbuilding/entries", json={
        "id": "special_yaml_001",
        "name": "YAML特殊字符测试",
        "data": {
            "description": "包含: 冒号、# 井号、- 破折号、{大括号}、[方括号]",
            "rules": ["规则: 含冒号", "# 含井号开头"],
        }
    }, timeout=5)
    log("T012-yaml-special", "YAML special chars in entry", r.status_code == 200)
    if r.status_code == 200:
        r = httpx.get(f"{BASE}/api/worldbuilding/entries/special_yaml_001", timeout=5)
        desc = r.json().get("description", "")
        log("T012-yaml-read", "Special chars preserved", "冒号" in desc, f"desc={desc[:40]}")
        httpx.delete(f"{BASE}/api/worldbuilding/entries/special_yaml_001", timeout=5)


# ──────────────────────────────────────────────
#  4. Cross-project Isolation
# ──────────────────────────────────────────────
def test_project_isolation():
    section("4. Cross-project Isolation")

    # Create character in test project
    ensure_test_project()
    httpx.post(f"{BASE}/api/characters", json={"name": "隔离测试角色", "role": "minor"}, timeout=5)

    # Switch to real project
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": "灵气复苏？不，超凡即是污染！",
        "project_path": "projects/灵气复苏？不，超凡即是污染！",
    }, timeout=5)

    # The test character should NOT be visible
    r = httpx.get(f"{BASE}/api/characters/隔离测试角色", timeout=5)
    log("Q029-a", "Test char NOT in real project", r.status_code == 404,
        f"status={r.status_code}")

    # Real project's characters should be visible
    r = httpx.get(f"{BASE}/api/characters/赵宋", timeout=5)
    log("Q029-b", "赵宋 visible in real project", r.status_code == 200)

    # Switch to 末世 project
    httpx.post(f"{BASE}/api/projects/switch", json={
        "project_name": "末世：我开了GM权限",
        "project_path": "projects/末世：我开了GM权限",
    }, timeout=5)
    r = httpx.get(f"{BASE}/api/characters/隔离测试角色", timeout=5)
    log("Q029-c", "Test char NOT in 末世 project", r.status_code == 404)

    # Switch back and verify test char still there
    ensure_test_project()
    r = httpx.get(f"{BASE}/api/characters/隔离测试角色", timeout=5)
    log("Q029-d", "Test char still in test project", r.status_code == 200)

    # Clean up
    httpx.delete(f"{BASE}/api/characters/隔离测试角色", timeout=5)

    # Q026: operations go to correct project after switch
    ensure_test_project()
    r = httpx.post(f"{BASE}/api/characters", json={"name": "项目归属测试", "role": "minor"}, timeout=5)
    log("Q026", "Character created in correct project", r.status_code == 200)
    file_exists = (PROJ / "characters" / "项目归属测试.yaml").exists()
    log("Q026b", "File in correct project directory", file_exists)
    real_proj_file = (WORKSPACE / "projects" / "灵气复苏？不，超凡即是污染！" / "characters" / "项目归属测试.yaml")
    log("Q026c", "File NOT in other project", not real_proj_file.exists())
    httpx.delete(f"{BASE}/api/characters/项目归属测试", timeout=5)


# ──────────────────────────────────────────────
#  5. State Consistency After Operations
# ──────────────────────────────────────────────
def test_state_consistency():
    section("5. State Consistency After Operations")
    ensure_test_project()

    # After all operations, verify:
    # 1. index.yaml matches actual files
    r = httpx.get(f"{BASE}/api/chapters", timeout=5)
    indexed_ids = {c["id"] for c in r.json().get("chapters", [])}
    ch_dir = PROJ / "chapters"
    file_ids = {f.stem for f in ch_dir.glob("*.md")} if ch_dir.exists() else set()
    idx_only = indexed_ids - file_ids
    file_only = file_ids - indexed_ids
    log("STATE-001", "Chapter index-file sync",
        len(idx_only) == 0 and len(file_only) == 0,
        f"idx_only={idx_only}, file_only={file_only}")

    # 2. character_index.yaml matches actual files
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    indexed_names = {e["name"] for e in r.json().get("entries", [])}
    char_dir = PROJ / "characters"
    skip = {"character_index", "relations", "relation_events", "character"}
    file_names = {f.stem for f in char_dir.glob("*.yaml") if f.stem not in skip}
    idx_only = indexed_names - file_names
    file_only = file_names - indexed_names
    log("STATE-002", "Character index-file sync",
        len(idx_only) == 0 and len(file_only) == 0,
        f"idx_only={idx_only}, file_only={file_only}")

    # 3. worldbuilding.yaml matches entries/
    r = httpx.get(f"{BASE}/api/worldbuilding", timeout=5)
    wb_data = r.json()
    indexed_ids = {e["id"] for e in wb_data.get("entries", [])}
    entries_dir = PROJ / "worldbuilding" / "entries"
    skip_entries = {"_template"}
    file_ids = {f.stem for f in entries_dir.glob("*.yaml") if f.stem not in skip_entries}
    idx_only = indexed_ids - file_ids
    file_only = file_ids - indexed_ids
    log("STATE-003", "Worldbuilding index-file sync",
        len(idx_only) == 0 and len(file_only) == 0,
        f"idx_only={idx_only}, file_only={file_only}")

    # 4. All YAML files parseable
    broken = []
    for f in PROJ.rglob("*.yaml"):
        try:
            text = f.read_text(encoding="utf-8")
            if text.strip():
                _yaml.load(text)
        except Exception as e:
            broken.append(f"{f.relative_to(PROJ)}: {e}")
    log("STATE-004", "All project YAML valid", len(broken) == 0,
        "; ".join(broken[:3]) if broken else "all OK")

    # 5. No empty YAML files (that should have content)
    for name, path in [
        ("meta.yaml", PROJ / ".novel" / "meta.yaml"),
        ("state.yaml", PROJ / ".novel" / "state.yaml"),
    ]:
        content = path.read_text(encoding="utf-8") if path.exists() else ""
        log(f"STATE-005-{name}", f"{name} has content", len(content.strip()) > 10,
            f"size={len(content)}")


# ──────────────────────────────────────────────
#  6. API Error Handling
# ──────────────────────────────────────────────
def test_api_errors():
    section("6. API Error Handling")
    ensure_test_project()

    # Invalid JSON
    r = httpx.post(f"{BASE}/api/characters",
                   content="not json",
                   headers={"Content-Type": "application/json"},
                   timeout=5)
    log("ERR-001", "Invalid JSON returns 422", r.status_code == 422, f"status={r.status_code}")

    # Missing required field
    r = httpx.post(f"{BASE}/api/chapters", json={"title": "无id"}, timeout=5)
    log("ERR-002", "Missing required field returns 422", r.status_code == 422, f"status={r.status_code}")

    # PUT to non-existent character
    r = httpx.put(f"{BASE}/api/characters/不存在", json={"role": "protagonist"}, timeout=5)
    log("ERR-003", "PUT non-existent char returns 404", r.status_code == 404)

    # PUT to non-existent chapter meta
    r = httpx.put(f"{BASE}/api/chapters/ch999/meta", json={"title": "ghost"}, timeout=5)
    log("ERR-004", "PUT non-existent chapter meta returns 404", r.status_code == 404)

    # PUT to non-existent chapter content
    r = httpx.put(f"{BASE}/api/chapters/ch999", json={"content": "ghost"}, timeout=5)
    log("ERR-005", "PUT non-existent chapter content returns 404", r.status_code == 404)

    # PUT to non-existent entry
    r = httpx.put(f"{BASE}/api/worldbuilding/entries/ghost_999", json={"name": "ghost"}, timeout=5)
    log("ERR-006", "PUT non-existent WB entry returns 404", r.status_code == 404)

    # DELETE non-existent (should still return 200 or 404)
    r = httpx.delete(f"{BASE}/api/characters/完全不存在的角色", timeout=5)
    log("ERR-007", "DELETE non-existent char doesn't crash",
        r.status_code in (200, 404), f"status={r.status_code}")

    r = httpx.delete(f"{BASE}/api/chapters/ch_ghost", timeout=5)
    log("ERR-008", "DELETE non-existent chapter doesn't crash",
        r.status_code in (200, 404), f"status={r.status_code}")

    # GET invalid endpoint
    r = httpx.get(f"{BASE}/api/nonexistent", timeout=5)
    log("ERR-009", "Non-existent endpoint returns 404/405",
        r.status_code in (404, 405), f"status={r.status_code}")

    # POST to read-only endpoint
    r = httpx.post(f"{BASE}/api/relationships", json={"test": True}, timeout=5)
    log("ERR-010", "POST to read-only relationships",
        r.status_code in (404, 405, 422), f"status={r.status_code}")


# ──────────────────────────────────────────────
#  7. Timeline Data Integrity
# ──────────────────────────────────────────────
def test_timeline_integrity():
    section("7. Timeline Data Integrity")
    ensure_test_project()

    # Ensure timeline dir exists
    tl_dir = PROJ / "timeline"
    tl_dir.mkdir(parents=True, exist_ok=True)
    tl_file = tl_dir / "main.yaml"
    if not tl_file.exists():
        tl_file.write_text("events: []\nthreads: []\n", encoding="utf-8")

    # Add events with same time (potential conflict)
    r1 = httpx.post(f"{BASE}/api/timeline", json={
        "time": "2024-01-01 12:00", "event": "事件A同时", "chapter": "ch001",
    }, timeout=5)
    r2 = httpx.post(f"{BASE}/api/timeline", json={
        "time": "2024-01-01 12:00", "event": "事件B同时", "chapter": "ch001",
    }, timeout=5)
    log("I003-dup", "Two events at same time allowed", r1.status_code == 200 and r2.status_code == 200)

    # Add event with empty time
    r = httpx.post(f"{BASE}/api/timeline", json={
        "time": "", "event": "无时间事件",
    }, timeout=5)
    log("I002-empty", "Empty time event", r.status_code == 200, "API accepts empty time")

    # I012: Read timeline
    r = httpx.get(f"{BASE}/api/timeline", timeout=5)
    events = r.json().get("events", [])
    log("I012-read", "Timeline readable after mixed adds", r.status_code == 200, f"count={len(events)}")


# ──────────────────────────────────────────────
#  8. Chapter Lifecycle State Transitions
# ──────────────────────────────────────────────
def test_chapter_lifecycle():
    section("8. Chapter Lifecycle State Transitions")
    ensure_test_project()

    # Create a lifecycle test chapter
    httpx.post(f"{BASE}/api/chapters", json={
        "id": "ch_lc", "title": "生命周期测试", "content": "# 测试\n\n初始内容",
    }, timeout=5)

    # Initial status should be outline
    r = httpx.get(f"{BASE}/api/chapters/ch_lc", timeout=5)
    status = r.json()["meta"]["status"]
    log("G019-init", "Initial status is outline", status == "outline", f"status={status}")

    # Transition: outline -> draft
    r = httpx.put(f"{BASE}/api/chapters/ch_lc/meta", json={"status": "draft"}, timeout=5)
    log("G019-draft", "Transition to draft", r.status_code == 200)

    # Transition: draft -> revise
    r = httpx.put(f"{BASE}/api/chapters/ch_lc/meta", json={"status": "revise"}, timeout=5)
    log("G020", "Transition to revise", r.status_code == 200)

    # Transition: revise -> final
    r = httpx.put(f"{BASE}/api/chapters/ch_lc/meta", json={"status": "final"}, timeout=5)
    log("G021", "Transition to final", r.status_code == 200)

    # G022: skip states (outline -> final directly) – API allows it
    httpx.put(f"{BASE}/api/chapters/ch_lc/meta", json={"status": "outline"}, timeout=5)
    r = httpx.put(f"{BASE}/api/chapters/ch_lc/meta", json={"status": "final"}, timeout=5)
    log("G022", "Skip states allowed by API (no guard)",
        r.status_code == 200, "API has no state machine guard")

    # G023: downgrade status
    r = httpx.put(f"{BASE}/api/chapters/ch_lc/meta", json={"status": "draft"}, timeout=5)
    log("G023", "Status downgrade allowed", r.status_code == 200,
        "API allows final→draft (no guard)")

    # G024: set arbitrary status (invalid)
    r = httpx.put(f"{BASE}/api/chapters/ch_lc/meta", json={"status": "invalid_status"}, timeout=5)
    log("G024-invalid", "Invalid status accepted by API",
        r.status_code == 200, "API has no validation on status values")

    httpx.delete(f"{BASE}/api/chapters/ch_lc", timeout=5)


# ──────────────────────────────────────────────
#  9. Concurrent-style rapid operations
# ──────────────────────────────────────────────
def test_rapid_operations():
    section("9. Rapid Sequential Operations")
    ensure_test_project()

    # Rapid create-read-update-delete cycle
    cycles_ok = 0
    for i in range(10):
        name = f"rapid_{i:03d}"
        c = httpx.post(f"{BASE}/api/characters", json={"name": name, "role": "minor"}, timeout=5)
        r = httpx.get(f"{BASE}/api/characters/{name}", timeout=5)
        u = httpx.put(f"{BASE}/api/characters/{name}", json={"role": "protagonist"}, timeout=5)
        d = httpx.delete(f"{BASE}/api/characters/{name}", timeout=5)
        if all(x.status_code == 200 for x in [c, r, u, d]):
            cycles_ok += 1
    log("RAPID-001", "10 CRUD cycles OK", cycles_ok == 10, f"ok={cycles_ok}")

    # Rapid chapter operations
    ch_ok = 0
    for i in range(5):
        cid = f"ch_rapid_{i:03d}"
        c = httpx.post(f"{BASE}/api/chapters", json={
            "id": cid, "title": f"Rapid {i}", "content": f"# {i}\n\n{'x'*100}",
        }, timeout=5)
        r = httpx.get(f"{BASE}/api/chapters/{cid}", timeout=5)
        u = httpx.put(f"{BASE}/api/chapters/{cid}", json={"content": f"# Updated {i}\n\n{'y'*200}"}, timeout=5)
        m = httpx.put(f"{BASE}/api/chapters/{cid}/meta", json={"status": "draft"}, timeout=5)
        d = httpx.delete(f"{BASE}/api/chapters/{cid}", timeout=5)
        if all(x.status_code == 200 for x in [c, r, u, m, d]):
            ch_ok += 1
    log("RAPID-002", "5 chapter CRUD cycles OK", ch_ok == 5, f"ok={ch_ok}")


# ──────────────────────────────────────────────
#  10. Multi-project Switch Stress
# ──────────────────────────────────────────────
def test_project_switch_stress():
    section("10. Project Switch Stress")

    projects = [
        (TEST_PROJECT, TEST_PATH),
        ("灵气复苏？不，超凡即是污染！", "projects/灵气复苏？不，超凡即是污染！"),
        ("末世：我开了GM权限", "projects/末世：我开了GM权限"),
    ]

    switch_ok = 0
    for _ in range(5):
        for name, path in projects:
            r = httpx.post(f"{BASE}/api/projects/switch", json={
                "project_name": name, "project_path": path,
            }, timeout=5)
            if r.status_code == 200:
                v = httpx.get(f"{BASE}/api/projects/current", timeout=5)
                if v.json()["current"]["current_project"] == name:
                    switch_ok += 1
    log("SWITCH-001", f"15 rapid project switches", switch_ok == 15, f"ok={switch_ok}/15")

    # After rapid switching, verify data isolation still holds
    ensure_test_project()
    r = httpx.get(f"{BASE}/api/characters", timeout=5)
    test_chars = r.json().get("entries", [])
    has_zhao = any(e["name"] == "赵宋" for e in test_chars)
    log("SWITCH-002", "No cross-contamination after switches", not has_zhao,
        "赵宋 should not be in test project")


# ──────────────────────────────────────────────
#  Runner
# ──────────────────────────────────────────────
def main():
    print(f"\n{'#'*60}")
    print(f"  Novel Writing System - Deep Integration Tests")
    print(f"  Target: {BASE}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}")

    start = time.time()

    try:
        test_orphans()
        test_batch_stress()
        test_data_edge_cases()
        test_project_isolation()
        test_state_consistency()
        test_api_errors()
        test_timeline_integrity()
        test_chapter_lifecycle()
        test_rapid_operations()
        test_project_switch_stress()
    except Exception as e:
        print(f"\n💥 FATAL: {e}")
        import traceback
        traceback.print_exc()

    elapsed = time.time() - start
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)

    print(f"\n{'='*60}")
    print(f"  DEEP TEST SUMMARY")
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

    report_path = Path(__file__).parent / "test-report-deep.json"
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
