#!/usr/bin/env python
"""检索脚本：从 novel-material 检索写作参考。

用法:
    python scripts/search.py --material-dir <路径> --type <类型> --query <查询> [--limit <数量>]
"""
import sys
import subprocess
from pathlib import Path

# 项目根目录
_ROOT = Path(__file__).resolve().parent.parent


def get_material_dir(material_dir_arg: str) -> Path:
    """获取 novel-material 目录路径。"""
    if material_dir_arg:
        return Path(material_dir_arg).resolve()
    # 默认查找同级目录
    default = _ROOT.parent / "novel-material"
    if default.exists():
        return default
    raise ValueError("未找到 novel-material 目录，请通过 --material-dir 指定")


def search_in_material(material_dir: Path, search_type: str, query: str, limit: int = 5) -> str:
    """调用 novel-material 的检索脚本。"""
    search_script = material_dir / "scripts" / "search" / f"search_{search_type}.py"

    if not search_script.exists():
        # 尝试其他可能的命名
        alternative_names = {
            "world": "search_world.py",
            "outline": "search_outline.py",
            "character": "search_character.py",
            "chapter": "search_chapter.py",
            "event": "search_event.py",
            "detail": "search_detail.py",
        }
        alt_name = alternative_names.get(search_type)
        if alt_name:
            search_script = material_dir / "scripts" / "search" / alt_name

        if not search_script.exists():
            print(f"❌ novel-material 中未找到检索脚本: {search_type}")
            print(f"   可用类型: world, outline, character, chapter, event, detail")
            return ""

    # 构建命令
    cmd = [
        sys.executable,
        str(search_script),
        query,
        "--limit", str(limit),
    ]

    print(f"🔍 检索类型: {search_type}")
    print(f"   查询: {query}")
    print(f"   数量: {limit}")
    print(f"   来源: {material_dir}")
    print()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(material_dir),
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"⚠️  检索返回错误: {result.stderr}")
            return ""
    except subprocess.TimeoutExpired:
        print(f"❌ 检索超时")
        return ""
    except Exception as e:
        print(f"❌ 检索失败: {e}")
        return ""


def list_available_searches(material_dir: Path):
    """列出可用的检索类型。"""
    search_dir = material_dir / "scripts" / "search"
    if not search_dir.exists():
        print(f"❌ novel-material 检索目录不存在: {search_dir}")
        return

    print(f"可用的检索类型:")
    print("-" * 40)
    for script in sorted(search_dir.glob("search_*.py")):
        name = script.stem.replace("search_", "")
        print(f"  {name}")
    print("-" * 40)


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python scripts/search.py --material-dir <路径> --type <类型> --query <查询> [--limit <数量>]")
        print("  python scripts/search.py --list --material-dir <路径>")
        print()
        print("检索类型: world, outline, character, chapter, event, detail")
        sys.exit(1)

    # 解析参数
    material_dir_arg = None
    search_type = None
    query = None
    limit = 5
    list_mode = False

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--material-dir" and i + 1 < len(sys.argv):
            material_dir_arg = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--type" and i + 1 < len(sys.argv):
            search_type = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--query" and i + 1 < len(sys.argv):
            query = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--list":
            list_mode = True
            i += 1
        else:
            i += 1

    try:
        material_dir = get_material_dir(material_dir_arg)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if list_mode:
        list_available_searches(material_dir)
        return

    if not search_type or not query:
        print("❌ 必须指定 --type 和 --query")
        sys.exit(1)

    result = search_in_material(material_dir, search_type, query, limit)
    if result:
        print(result)


if __name__ == "__main__":
    main()