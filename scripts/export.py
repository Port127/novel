#!/usr/bin/env python
"""导出脚本：导出小说为各种格式。

用法:
    python scripts/export.py <project_id> [--format <格式>] [--output <路径>]
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


def get_sorted_chapters(project_id: str) -> list[tuple[int, Path]]:
    """获取排序后的章节文件列表。"""
    content_dir = get_project_dir(project_id) / "content" / "chapters"
    chapter_files = []

    for f in content_dir.glob("chapter_*.md"):
        match = re.search(r"chapter_(\d+)", f.name)
        if match:
            chapter_num = int(match.group(1))
            chapter_files.append((chapter_num, f))

    return sorted(chapter_files, key=lambda x: x[0])


def get_worldbuilding_info(project_id: str) -> dict:
    """获取世界观信息（模块化结构）。"""
    wb_dir = get_project_dir(project_id) / "settings" / "worldbuilding"
    power_system = load_yaml(wb_dir / "power_system.yaml")
    factions_index = load_yaml(wb_dir / "factions" / "_index.yaml")

    return {
        "power_system": power_system,
        "factions": factions_index.get("factions", []),
    }


def get_characters_info(project_id: str) -> dict:
    """获取人物信息（模块化结构）。"""
    chars_dir = get_project_dir(project_id) / "settings" / "characters"
    protagonist = load_yaml(chars_dir / "protagonist" / "protagonist.yaml")
    antagonist_index = load_yaml(chars_dir / "antagonist" / "_index.yaml")
    supporting_index = load_yaml(chars_dir / "supporting" / "_index.yaml")

    characters_list = []
    if protagonist.get("name"):
        characters_list.append({
            "name": protagonist.get("name"),
            "role": "主角",
            "description": protagonist.get("description", "")
        })
    for a in antagonist_index.get("antagonists", []):
        characters_list.append({
            "name": a.get("name"),
            "role": "反派",
            "description": ""
        })
    for s in supporting_index.get("supporting_characters", []):
        characters_list.append({
            "name": s.get("name"),
            "role": "配角",
            "description": ""
        })

    return {"characters": characters_list}


def get_chapters_index(project_id: str) -> dict:
    """获取章节索引（模块化结构）。"""
    chapters_dir = get_project_dir(project_id) / "settings" / "chapters"
    return load_yaml(chapters_dir / "_index.yaml")


def export_txt(project_id: str, output_path: Path, include_metadata: bool = True):
    """导出为 TXT 格式。"""
    project = load_yaml(get_project_dir(project_id) / "project.yaml")
    worldbuilding = get_worldbuilding_info(project_id)
    characters = get_characters_info(project_id)
    chapters_index = get_chapters_index(project_id)

    output_lines = []

    if include_metadata:
        output_lines.append("=" * 50)
        output_lines.append(project.get("name", "未命名"))
        output_lines.append(f"作者: {project.get('author', '匿名')}")
        output_lines.append("=" * 50)
        output_lines.append("")

        # 世界观简介
        power_system = worldbuilding.get("power_system", {})
        if power_system.get("name"):
            output_lines.append("【世界观简介】")
            output_lines.append(f"力量体系: {power_system.get('name')}")
            output_lines.append(f"类型: {power_system.get('type', '未知')}")
            output_lines.append("")

        # 人物简介
        if characters.get("characters"):
            output_lines.append("【主要人物】")
            for c in characters["characters"][:5]:
                output_lines.append(f"  {c.get('name')} ({c.get('role')})")
            output_lines.append("")

        output_lines.append("=" * 50)
        output_lines.append("正文")
        output_lines.append("=" * 50)
        output_lines.append("")

    # 章节正文
    chapter_files = get_sorted_chapters(project_id)
    total_words = 0

    for chapter_num, chapter_file in chapter_files:
        content = chapter_file.read_text(encoding="utf-8")

        # 获取章节标题
        chapter_info = None
        for c in chapters_index.get("chapters", []):
            if c.get("chapter") == chapter_num:
                chapter_info = c
                break

        title = chapter_info.get("title", f"第{chapter_num}章") if chapter_info else f"第{chapter_num}章"
        status = chapter_info.get("status", "planned") if chapter_info else "planned"

        if status == "planned":
            continue

        output_lines.append("")
        output_lines.append(f"第{chapter_num}章 {title}")
        output_lines.append("")
        output_lines.append(content)
        output_lines.append("")
        output_lines.append("-" * 30)

        total_words += count_words(content)

    output_path.write_text("\n".join(output_lines), encoding="utf-8")

    print(f"✅ TXT 导出完成")
    print(f"   文件: {output_path}")
    print(f"   章节数: {len(chapter_files)}")
    print(f"   总字数: {total_words}")


def export_markdown(project_id: str, output_path: Path):
    """导出为 Markdown 格式（分章节文件）。"""
    project = load_yaml(get_project_dir(project_id) / "project.yaml")
    chapters_index = get_chapters_index(project_id)

    output_dir = output_path if output_path.suffix == "" else output_path.parent / output_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    # 创建 README.md
    readme_content = f"""# {project.get('name', '未命名')}

作者: {project.get('author', '匿名')}
类型: {project.get('genre', '未知')}
状态: {project.get('status', 'planning')}

## 章节目录

"""
    chapter_files = get_sorted_chapters(project_id)
    for chapter_num, _ in chapter_files:
        chapter_info = None
        for c in chapters_index.get("chapters", []):
            if c.get("chapter") == chapter_num:
                chapter_info = c
                break
        title = chapter_info.get("title", f"第{chapter_num}章") if chapter_info else f"第{chapter_num}章"
        readme_content += f"- [第{chapter_num}章 {title}](chapter_{chapter_num:03d}.md)\n"

    (output_dir / "README.md").write_text(readme_content, encoding="utf-8")

    # 复制章节文件
    for chapter_num, chapter_file in chapter_files:
        dest_file = output_dir / f"chapter_{chapter_num:03d}.md"
        content = chapter_file.read_text(encoding="utf-8")

        chapter_info = None
        for c in chapters_index.get("chapters", []):
            if c.get("chapter") == chapter_num:
                chapter_info = c
                break
        title = chapter_info.get("title", f"第{chapter_num}章") if chapter_info else f"第{chapter_num}章"

        full_content = f"# 第{chapter_num}章 {title}\n\n{content}"
        dest_file.write_text(full_content, encoding="utf-8")

    print(f"✅ Markdown 导出完成")
    print(f"   目录: {output_dir}")
    print(f"   章节数: {len(chapter_files)}")


def export_epub(project_id: str, output_path: Path):
    """导出为 EPUB 格式（需要 pandoc）。"""
    import subprocess

    temp_dir = _ROOT / "temp_export" / project_id
    export_markdown(project_id, temp_dir)

    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("❌ 未安装 pandoc，无法导出 EPUB")
            print("   安装方法: brew install pandoc")
            return
    except FileNotFoundError:
        print("❌ 未安装 pandoc，无法导出 EPUB")
        print("   安装方法: brew install pandoc")
        return

    project = load_yaml(get_project_dir(project_id) / "project.yaml")
    md_files = sorted(temp_dir.glob("chapter_*.md"))

    cmd = [
        "pandoc",
        "-o", str(output_path),
        "--epub-title-page=true",
        "--metadata", f"title={project.get('name')}",
        "--metadata", f"author={project.get('author')}",
        str(temp_dir / "README.md"),
    ] + [str(f) for f in md_files]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ EPUB 导出完成")
        print(f"   文件: {output_path}")
    else:
        print(f"❌ EPUB 导出失败: {result.stderr}")

    import shutil
    shutil.rmtree(temp_dir.parent, ignore_errors=True)


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python scripts/export.py <project_id> [--format <格式>] [--output <路径>]")
        print()
        print("导出格式: txt, md, epub")
        sys.exit(1)

    project_id = sys.argv[1]

    format_type = "txt"
    output_arg = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            format_type = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_arg = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    project_dir = get_project_dir(project_id)
    if not project_dir.exists():
        print(f"❌ 项目不存在: {project_id}")
        sys.exit(1)

    exports_dir = project_dir / "exports"
    exports_dir.mkdir(exist_ok=True)

    if output_arg:
        output_path = Path(output_arg)
    else:
        timestamp = datetime.now().strftime("%Y%m%d")
        if format_type == "txt":
            output_path = exports_dir / f"{project_id}_{timestamp}.txt"
        elif format_type == "md":
            output_path = exports_dir / f"{project_id}_{timestamp}"
        elif format_type == "epub":
            output_path = exports_dir / f"{project_id}_{timestamp}.epub"
        else:
            output_path = exports_dir / f"{project_id}_{timestamp}.txt"

    if format_type == "txt":
        export_txt(project_id, output_path)
    elif format_type == "md":
        export_markdown(project_id, output_path)
    elif format_type == "epub":
        export_epub(project_id, output_path)
    else:
        print(f"❌ 不支持的格式: {format_type}")
        print("   支持格式: txt, md, epub")
        sys.exit(1)


if __name__ == "__main__":
    main()