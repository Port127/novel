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
    chapters_dir = get_project_dir(project_id) / "settings" / "chapters"
    index = load_yaml(chapters_dir / "_index.yaml")

    stats = {
        "total": index.get("total_chapters", 0),
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
        words = chapter.get("word_count_actual", 0)

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
            "tension": chapter.get("tension_level"),
        })

    if stats["draft"] + stats["written"] + stats["revised"] > 0:
        stats["avg_words"] = stats["total_words"] // (stats["draft"] + stats["written"] + stats["revised"])

    return stats


def get_worldbuilding_stats(project_id: str) -> dict:
    """获取世界观统计（模块化结构）。"""
    wb_dir = get_project_dir(project_id) / "settings" / "worldbuilding"

    # 力量体系
    power_system = load_yaml(wb_dir / "power_system.yaml")
    power_ranks = len(power_system.get("levels", []))

    # 势力
    factions_index = load_yaml(wb_dir / "factions" / "_index.yaml")
    factions_count = len(factions_index.get("factions", []))

    # 地点
    locations_index = load_yaml(wb_dir / "locations" / "_index.yaml")
    locations_count = len(locations_index.get("locations", []))

    return {
        "power_system_name": power_system.get("name", "未设定"),
        "power_ranks": power_ranks,
        "factions": factions_count,
        "locations": locations_count,
    }


def get_characters_stats(project_id: str) -> dict:
    """获取人物统计（模块化结构）。"""
    chars_dir = get_project_dir(project_id) / "settings" / "characters"

    # 主角
    protagonist = load_yaml(chars_dir / "protagonist" / "protagonist.yaml")
    protagonist_name = protagonist.get("name", "未设定")

    # 反派
    antagonist_index = load_yaml(chars_dir / "antagonist" / "_index.yaml")
    antagonists = antagonist_index.get("antagonists", [])

    # 配角
    supporting_index = load_yaml(chars_dir / "supporting" / "_index.yaml")
    supporting = supporting_index.get("supporting_characters", [])

    # 龙套
    minor_index = load_yaml(chars_dir / "minor" / "_index.yaml")
    minor = minor_index.get("minor_characters", [])

    return {
        "protagonist": protagonist_name,
        "antagonists": len(antagonists),
        "supporting": len(supporting),
        "minor": len(minor),
        "total": 1 + len(antagonists) + len(supporting) + len(minor),
    }


def get_outline_stats(project_id: str) -> dict:
    """获取大纲统计（模块化结构）。"""
    outline_dir = get_project_dir(project_id) / "settings" / "outline"

    # 核心设定
    premise = load_yaml(outline_dir / "premise.yaml")
    premise_statement = premise.get("premise_statement", "未设定")

    # 幕结构
    acts_index = load_yaml(outline_dir / "acts" / "_index.yaml")
    acts = acts_index.get("acts", [])

    # 统计节拍数（遍历各幕）
    beats_count = 0
    for act_info in acts:
        act_file = outline_dir / "acts" / act_info.get("path", "")
        if act_file.exists():
            act_data = load_yaml(act_file)
            for seq in act_data.get("sequences", []):
                beats_count += len(seq.get("beats", []))

    return {
        "premise": premise_statement[:50] + "..." if len(premise_statement) > 50 else premise_statement,
        "acts": len(acts),
        "beats": beats_count,
    }


def show_stats(project_id: str, detail: bool = False):
    """显示项目统计。"""
    project_yaml = get_project_dir(project_id) / "project.yaml"
    if not project_yaml.exists():
        print(f"❌ 项目不存在: {project_id}")
        return

    project = load_yaml(project_yaml)
    chapter_stats = get_chapter_stats(project_id)
    worldbuilding_stats = get_worldbuilding_stats(project_id)
    characters_stats = get_characters_stats(project_id)
    outline_stats = get_outline_stats(project_id)

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

    # 目标信息
    target = project.get("target", {})
    print(f"\n目标:")
    print(f"  目标章数: {target.get('chapters', 800)}")
    print(f"  单章字数: {target.get('words_per_chapter', 4000)}")
    print(f"  总字数目标: {target.get('total_words', 3200000)}")

    print(f"\n设定统计:")
    print(f"  力量体系: {worldbuilding_stats['power_system_name']}")
    print(f"  力量等级: {worldbuilding_stats['power_ranks']}")
    print(f"  势力: {worldbuilding_stats['factions']}")
    print(f"  地点: {worldbuilding_stats['locations']}")
    print(f"  人物总数: {characters_stats['total']}")
    print(f"  - 主角: {characters_stats['protagonist']}")
    print(f"  - 反派: {characters_stats['antagonists']}")
    print(f"  - 配角: {characters_stats['supporting']}")
    print(f"  大纲幕数: {outline_stats['acts']}")
    print(f"  大纲节拍: {outline_stats['beats']}")
    print(f"  核心前提: {outline_stats['premise']}")

    print(f"\n章节统计:")
    print(f"  目标章节: {chapter_stats['total']}")
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

    # Pipeline 状态
    pipeline = project.get("pipeline_status", {})
    print(f"\nPipeline 状态:")
    print(f"  当前阶段: {pipeline.get('current_stage', 0)}")
    print(f"  已完成阶段: {pipeline.get('completed_stages', [])}")

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
            title = c['title'][:20] if c['title'] else "未命名"
            print(f"  {status_icon} 第{c['chapter']:3d}章 | {title:20s} | {c['status']:8s} | {c['words']:5d}字 | 张力{c['tension']}")
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