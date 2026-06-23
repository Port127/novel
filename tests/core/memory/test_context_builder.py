from pathlib import Path
from novel.core.memory.context_builder import build_chapter_context
import yaml

def test_build_chapter_context(tmp_path):
    wb_dir = tmp_path / "settings" / "worldbuilding"
    wb_dir.mkdir(parents=True)
    with open(wb_dir / "power.yaml", "w", encoding="utf-8") as f:
        yaml.dump({"system": "magic"}, f)
    ctx = build_chapter_context(str(tmp_path))
    assert "magic" in ctx
