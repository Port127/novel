#!/usr/bin/env python
"""项目管理脚本：创建、删除、列出写作项目。

用法:
    python scripts/project.py create <项目名> [--genre <类型>] [--author <作者>]
    python scripts/project.py delete <project_id>
    python scripts/project.py list
    python scripts/project.py show <project_id>
"""
import sys
import shutil
from pathlib import Path
from datetime import datetime
import random
import string

# 项目根目录
_ROOT = Path(__file__).resolve().parent.parent
NOVELS_DIR = _ROOT / "novels"
SCHEMAS_DIR = _ROOT / "data" / "schemas"


def generate_project_id() -> str:
    """生成项目ID: nv_{YYYYMMDD}_{random4}"""
    date_str = datetime.now().strftime("%Y%m%d")
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"nv_{date_str}_{random_str}"


def create_project(name: str, genre: str = "修仙", author: str = "匿名") -> str:
    """创建新写作项目。"""
    project_id = generate_project_id()
    project_dir = NOVELS_DIR / project_id

    # 创建目录结构
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "settings").mkdir(exist_ok=True)
    (project_dir / "chapters").mkdir(exist_ok=True)
    (project_dir / "drafts").mkdir(exist_ok=True)
    (project_dir / "exports").mkdir(exist_ok=True)
    (project_dir / "history").mkdir(exist_ok=True)

    # 创建 project.yaml
    today = datetime.now().strftime("%Y-%m-%d")
    project_yaml = f"""project_id: {project_id}
name: "{name}"
author: {author}
genre: {genre}
status: planning

created: {today}
updated: {today}

stats:
  chapters_written: 0
  chapters_planned: 0
  words_total: 0

references: []

ai_config:
  model: gpt-4o-mini
  style_guide: ""
  auto_save: true
"""
    (project_dir / "project.yaml").write_text(project_yaml, encoding="utf-8")

    # 创建空的设定文件
    settings_dir = project_dir / "settings"
    (settings_dir / "worldbuilding.yaml").write_text(
        f"""world_type: {genre}
setting_period: ""

power_system:
  name: ""
  type: ""
  ranks: []

factions: []
locations: []
lore:
  history: []
  artifacts: []
  terminology: []
""",
        encoding="utf-8",
    )
    (settings_dir / "characters.yaml").write_text("characters: []\n", encoding="utf-8")
    (settings_dir / "outline.yaml").write_text(
        """premise: ""
theme: []
tone: []

acts: []
plotlines: []
hooks: []
pacing_curve: []
""",
        encoding="utf-8",
    )
    (settings_dir / "notes.yaml").write_text("notes: []\n", encoding="utf-8")

    # 创建章节索引
    (project_dir / "chapters" / "_index.yaml").write_text(
        """chapters: []

stats:
  total: 0
  planned: 0
  draft: 0
  written: 0
  revised: 0
  total_words: 0
""",
        encoding="utf-8",
    )

    print(f"✅ 项目创建成功: {project_id}")
    print(f"   目录: {project_dir}")
    print(f"   名称: {name}")
    print(f"   类型: {genre}")
    print()
    print("下一步:")
    print(f"   1. 编辑设定: {project_dir}/settings/")
    print(f"   2. 生成设定: python scripts/generate.py world {project_id}")
    print(f"   3. 规划大纲: python scripts/generate.py outline {project_id}")

    return project_id


def delete_project(project_id: str) -> bool:
    """删除写作项目。"""
    project_dir = NOVELS_DIR / project_id

    if not project_dir.exists():
        print(f"❌ 项目不存在: {project_id}")
        return False

    # 确认删除
    print(f"⚠️  即将删除项目: {project_id}")
    print(f"   目录: {project_dir}")

    # 直接删除（在完全授权模式下）
    shutil.rmtree(project_dir)
    print(f"✅ 项目已删除: {project_id}")
    return True


def list_projects() -> list:
    """列出所有写作项目。"""
    if not NOVELS_DIR.exists():
        print("暂无项目")
        return []

    projects = []
    for project_dir in sorted(NOVELS_DIR.iterdir()):
        if project_dir.is_dir() and project_dir.name.startswith("nv_"):
            project_yaml = project_dir / "project.yaml"
            if project_yaml.exists():
                # 读取基本信息
                import yaml

                with open(project_yaml, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                projects.append(
                    {
                        "id": project_dir.name,
                        "name": data.get("name", "未知"),
                        "genre": data.get("genre", "未知"),
                        "status": data.get("status", "未知"),
                        "chapters": data.get("stats", {}).get("chapters_written", 0),
                        "words": data.get("stats", {}).get("words_total", 0),
                    }
                )

    if not projects:
        print("暂无项目")
        return []

    print(f"共 {len(projects)} 个项目:")
    print("-" * 60)
    for p in projects:
        print(f"  {p['id']}")
        print(f"    名称: {p['name']} | 类型: {p['genre']} | 状态: {p['status']}")
        print(f"    章节: {p['chapters']} | 字数: {p['words']}")
    print("-" * 60)

    return projects


def show_project(project_id: str) -> dict:
    """显示项目详情。"""
    project_dir = NOVELS_DIR / project_id

    if not project_dir.exists():
        print(f"❌ 项目不存在: {project_id}")
        return {}

    import yaml

    project_yaml = project_dir / "project.yaml"
    with open(project_yaml, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    print(f"项目详情: {project_id}")
    print("=" * 60)
    print(f"名称: {data.get('name')}")
    print(f"作者: {data.get('author')}")
    print(f"类型: {data.get('genre')}")
    print(f"状态: {data.get('status')}")
    print(f"创建: {data.get('created')}")
    print(f"更新: {data.get('updated')}")
    print()
    print("统计:")
    stats = data.get("stats", {})
    print(f"  已写章节: {stats.get('chapters_written', 0)}")
    print(f"  计划章节: {stats.get('chapters_planned', 0)}")
    print(f"  总字数: {stats.get('words_total', 0)}")
    print()
    print("目录结构:")
    for subdir in ["settings", "chapters", "drafts", "exports", "history"]:
        sub_path = project_dir / subdir
        if sub_path.exists():
            files = list(sub_path.iterdir())
            print(f"  {subdir}/ ({len(files)} 文件)")
    print("=" * 60)

    return data


def main():
    """CLI 入口。"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python scripts/project.py create <项目名> [--genre <类型>] [--author <作者>]")
        print("  python scripts/project.py delete <project_id>")
        print("  python scripts/project.py list")
        print("  python scripts/project.py show <project_id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("用法: python scripts/project.py create <项目名> [--genre <类型>] [--author <作者>]")
            sys.exit(1)

        name = sys.argv[2]
        genre = "修仙"
        author = "匿名"

        # 解析可选参数
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--genre" and i + 1 < len(sys.argv):
                genre = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--author" and i + 1 < len(sys.argv):
                author = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        create_project(name, genre, author)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("用法: python scripts/project.py delete <project_id>")
            sys.exit(1)
        delete_project(sys.argv[2])

    elif command == "list":
        list_projects()

    elif command == "show":
        if len(sys.argv) < 3:
            print("用法: python scripts/project.py show <project_id>")
            sys.exit(1)
        show_project(sys.argv[2])

    else:
        print(f"未知命令: {command}")
        print("可用命令: create, delete, list, show")
        sys.exit(1)


if __name__ == "__main__":
    main()