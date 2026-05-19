#!/usr/bin/env python
"""项目管理脚本：创建、删除、列出写作项目。

用法:
    python scripts/project.py create <项目名> [--genre <类型>] [--author <作者>] [--template <模板>]
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
import yaml

# 项目根目录
_ROOT = Path(__file__).resolve().parent.parent
NOVELS_DIR = _ROOT / "novels"
SCHEMAS_DIR = _ROOT / "data" / "schemas"
TEMPLATES_DIR = _ROOT / "templates"


def generate_project_id() -> str:
    """生成项目ID: nv_{YYYYMMDD}_{random4}"""
    date_str = datetime.now().strftime("%Y%m%d")
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"nv_{date_str}_{random_str}"


def list_available_templates() -> list:
    """列出可用模板。"""
    if not TEMPLATES_DIR.exists():
        return []

    templates = []
    for template_dir in TEMPLATES_DIR.iterdir():
        if template_dir.is_dir():
            template_yaml = template_dir / "template.yaml"
            if template_yaml.exists():
                with open(template_yaml, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                templates.append({
                    "name": template_dir.name,
                    "description": data.get("description", ""),
                    "version": data.get("template_version", "1.0")
                })

    return templates


def create_project(name: str, genre: str = "修仙", author: str = "匿名", template: str = "default") -> str:
    """从模板创建新写作项目。"""
    project_id = generate_project_id()
    project_dir = NOVELS_DIR / project_id

    # 检查模板是否存在
    template_dir = TEMPLATES_DIR / template
    if not template_dir.exists():
        print(f"❌ 模板不存在: {template}")
        print(f"可用模板:")
        for t in list_available_templates():
            print(f"  - {t['name']}: {t['description']}")
        return None

    # 从模板复制整个目录结构
    shutil.copytree(template_dir, project_dir)

    # 创建额外目录（模板不含的）
    (project_dir / "drafts").mkdir(exist_ok=True)
    (project_dir / "exports").mkdir(exist_ok=True)
    (project_dir / "history").mkdir(exist_ok=True)

    # 更新 project.yaml（填充项目信息）
    project_yaml_path = project_dir / "project.yaml"
    today = datetime.now().strftime("%Y-%m-%d")

    with open(project_yaml_path, encoding="utf-8") as f:
        project_data = yaml.safe_load(f)

    project_data["project_id"] = project_id
    project_data["name"] = name
    project_data["author"] = author
    project_data["genre"] = genre
    project_data["created"] = today
    project_data["updated"] = today

    with open(project_yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(project_data, f, allow_unicode=True, default_flow_style=False)

    print(f"✅ 项目创建成功: {project_id}")
    print(f"   模板: {template}")
    print(f"   目录: {project_dir}")
    print(f"   名称: {name}")
    print(f"   类型: {genre}")
    print()
    print("Pipeline 流程:")
    print("   1. 阶段1 - 世界观设定")
    print("   2. 阶段2 - 人物设定")
    print("   3. 阶段3 - 大纲设定")
    print("   4. 阶段4 - 章节规划")
    print("   5. 阶段5 - 正文写作")
    print()
    print("下一步:")
    print("   使用 /create-novel 开始 Pipeline 流程")

    return project_id


def delete_project(project_id: str) -> bool:
    """删除写作项目。"""
    project_dir = NOVELS_DIR / project_id

    if not project_dir.exists():
        print(f"❌ 项目不存在: {project_id}")
        return False

    print(f"⚠️  即将删除项目: {project_id}")
    print(f"   目录: {project_dir}")

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
                        "pipeline_stage": data.get("pipeline_status", {}).get("current_stage", 0),
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
        print(f"    章节: {p['chapters']} | 字数: {p['words']} | Pipeline阶段: {p['pipeline_stage']}")
    print("-" * 60)

    return projects


def show_project(project_id: str) -> dict:
    """显示项目详情。"""
    project_dir = NOVELS_DIR / project_id

    if not project_dir.exists():
        print(f"❌ 项目不存在: {project_id}")
        return {}

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

    # Pipeline 状态
    pipeline = data.get("pipeline_status", {})
    print("Pipeline 状态:")
    print(f"  当前阶段: {pipeline.get('current_stage', 0)}")
    print(f"  已完成阶段: {pipeline.get('completed_stages', [])}")
    print()

    print("统计:")
    stats = data.get("stats", {})
    print(f"  已写章节: {stats.get('chapters_written', 0)}")
    print(f"  计划章节: {stats.get('chapters_planned', 0)}")
    print(f"  总字数: {stats.get('words_total', 0)}")
    print()

    # 目标信息
    target = data.get("target", {})
    if target:
        print("目标:")
        print(f"  目标章数: {target.get('chapters', 800)}")
        print(f"  单章字数: {target.get('words_per_chapter', 4000)}")
        print(f"  总字数目标: {target.get('total_words', 3200000)}")
        print()

    print("目录结构:")
    for subdir in ["settings", "chapters", "content", "drafts", "exports", "history"]:
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
        print("  python scripts/project.py create <项目名> [--genre <类型>] [--author <作者>] [--template <模板>]")
        print("  python scripts/project.py delete <project_id>")
        print("  python scripts/project.py list")
        print("  python scripts/project.py show <project_id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("用法: python scripts/project.py create <项目名> [--genre <类型>] [--author <作者>] [--template <模板>]")
            print("可用模板:")
            for t in list_available_templates():
                print(f"  - {t['name']}: {t['description']}")
            sys.exit(1)

        name = sys.argv[2]
        genre = "修仙"
        author = "匿名"
        template = "default"

        # 解析可选参数
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--genre" and i + 1 < len(sys.argv):
                genre = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--author" and i + 1 < len(sys.argv):
                author = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--template" and i + 1 < len(sys.argv):
                template = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        create_project(name, genre, author, template)

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