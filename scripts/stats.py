#!/usr/bin/env python
"""统计脚本：显示项目字数、进度等信息。

用法:
    python scripts/stats.py <project_id>
    python scripts/stats.py <project_id> --detail
"""
import sys
import re
from pathlib import Path
from datetime import datetime
import yaml

# 项目根目录
_ROOT = Path(__file__).resolve().parent.parent
NOVELS_DIR = _ROOT / "novels"


def get_project_dir(project_id: str) -> Path:
    """获取项目目录。"""
    return NOVELS_DIR / project_id


def load_yaml(file_path: Path) -> dict:
    """加载 YAML 文件。"""
    if not file_path.exists():
        return {}
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def count_words(text: str) -> int:
    """统计中文字数。"""
    chinese_chars = len(re.findall(r"[一-龥]", text))
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    return chinese_chars + english_words


def get_chapter_stats(project_id: str) -> dict:
    """获取章节统计。"""
    chapters_dir = get_project_dir(project_id) / "chapters"
    index = load_yaml(chapters_dir / "_index.yaml")

    stats = {
        "total": len(index.get("chapters", [])),
        "planned": 0,
        "draft": 0,
        "written": 0,
        "revised": 0,
        "total_words": 0,
        "avg_words": 0,
        "chapters_detail": [],
    }

    for chapter in index.get("chapters", []):
        status = chapter.get("status", "planned")
        words = chapter.get("words", 0)

        if status == "planned":
            stats["planned"] += 1
        elif status == "draft":
            stats["draft"] += 1
            stats["total_words"] += words
        elif status == "written":
            stats["written"] += 1
            stats["total_words"] += words
        elif status == "revised":
            stats["revised"] += 1
            stats["total_words"] += words

        stats["chapters_detail"].append({
            "chapter": chapter.get("chapter"),
            "title": chapter.get("title"),
            "status": status,
            "words": words,
            "tension": chapter.get("tension"),
        })

    if stats["draft"] + stats["written"] + stats["revised"] > 0:
        stats["avg_words"] = stats["total_words"] // (stats["draft"] + stats["written"] + stats["revised"])

    return stats


def get_settings_stats(project_id: str) -> dict:
    """获取设定统计。"""
    settings_dir = get_project_dir(project_id) / "settings"

    worldbuilding = load_yaml(settings_dir / "worldbuilding.yaml")
    characters = load_yaml(settings_dir / "characters.yaml")
    outline = load_yaml(settings_dir / "outline.yaml")

    return {
        "world_type": worldbuilding.get("world_type", "未设定"),
        "power_ranks": len(worldbuilding.get("power_system", {}).get("ranks", [])),
        "factions": len(worldbuilding.get("factions", [])),
        "locations": len(worldbuilding.get("locations", [])),
        "characters": len(characters.get("characters", [])),
        "acts": len(outline.get("acts", [])),
        "premise": outline.get("premise", "未设定"),
    }


def show_stats(project_id: str, detail: bool = False):
    """显示项目统计。"""
    project_yaml = get_project_dir(project_id) / "project.yaml"
    if not project_yaml.exists():
        print(f"❌ 项目不存在: {project_id}")
        return

    project = load_yaml(project_yaml)
    chapter_stats = get_chapter_stats(project_id)
    settings_stats = get_settings_stats(project_id)

    print(f"\n{'='*60}")
    print(f"项目统计: {project.get('name')}")
    print(f"{'='*60}")

    print(f"\n基本信息:")
    print(f"  项目ID: {project_id}")
    print(f"  作者: {project.get('author')}")
    print(f"  类型: {project.get('genre')}")
    print(f"  状态: {project.get('status')}")
    print(f"  创建: {project.get('created')}")
    print(f"  更新: {project.get('updated')}")

    print(f"\n设定统计:")
    print(f"  世界观类型: {settings_stats['world_type']}")
    print(f"  力量等级: {settings_stats['power_ranks']}")
    print(f"  势力: {settings_stats['factions']}")
    print(f"  地点: {settings_stats['locations']}")
    print(f"  人物: {settings_stats['characters']}")
    print(f"  大纲幕数: {settings_stats['acts']}")
    print(f"  核心前提: {settings_stats['premise']}")

    print(f"\n章节统计:")
    print(f"  总章节: {chapter_stats['total']}")
    print(f"  已规划: {chapter_stats['planned']}")
    print(f"  草稿: {chapter_stats['draft']}")
    print(f"  已写: {chapter_stats['written']}")
    print(f"  已润色: {chapter_stats['revised']}")
    print(f"  总字数: {chapter_stats['total_words']}")
    print(f"  平均字数/章: {chapter_stats['avg_words']}")

    # 进度百分比
    if chapter_stats['total'] > 0:
        progress = (chapter_stats['draft'] + chapter_stats['written'] + chapter_stats['revised']) / chapter_stats['total'] * 100
        print(f"  写作进度: {progress:.1f}%")

    if detail:
        print(f"\n章节详情:")
        print(f"{'-'*60}")
        for c in chapter_stats['chapters_detail']:
            status_icon = {
                "planned": "○",
                "draft": "◐",
                "written": "●",
                "revised": "★",
            }.get(c['status'], "○")
            print(f"  {status_icon} 第{c['chapter']:3d}章 | {c['title'][:20]:20s} | {c['status']:8s} | {c['words']:5d}字 | 张力{c['tension']}")
        print(f"{'-'*60}")

    print(f"\n{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python scripts/stats.py <project_id>")
        print("  python scripts/stats.py <project_id> --detail")
        sys.exit(1)

    project_id = sys.argv[1]
    detail = "--detail" in sys.argv

    show_stats(project_id, detail)


if __name__ == "__main__":
    main()