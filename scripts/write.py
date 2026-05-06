#!/usr/bin/env python
"""章节写作脚本：AI 生成、续写、改写章节正文。

用法:
    python scripts/write.py new <project_id> <章节号> [--prompt <描述>]
    python scripts/write.py continue <project_id> <章节号> [--length <字数>]
    python scripts/write.py revise <project_id> <章节号> [--mode <模式>]
"""
import sys
import re
from pathlib import Path
from datetime import datetime
import yaml
import json

# 项目根目录
_ROOT = Path(__file__).resolve().parent.parent
NOVELS_DIR = _ROOT / "novels"
sys.path.insert(0, str(_ROOT))

from scripts.utils.llm_client import call_llm, load_config, get_api_stats, reset_api_stats


def get_project_dir(project_id: str) -> Path:
    """获取项目目录。"""
    return NOVELS_DIR / project_id


def load_project(project_id: str) -> dict:
    """加载项目配置。"""
    project_yaml = get_project_dir(project_id) / "project.yaml"
    if not project_yaml.exists():
        raise FileNotFoundError(f"项目不存在: {project_id}")
    with open(project_yaml, encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(file_path: Path, data: dict):
    """保存 YAML 文件。"""
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def load_yaml(file_path: Path) -> dict:
    """加载 YAML 文件。"""
    if not file_path.exists():
        return {}
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_settings(project_id: str) -> tuple[dict, dict, dict]:
    """加载设定文件。"""
    settings_dir = get_project_dir(project_id) / "settings"
    worldbuilding = load_yaml(settings_dir / "worldbuilding.yaml")
    characters = load_yaml(settings_dir / "characters.yaml")
    outline = load_yaml(settings_dir / "outline.yaml")
    return worldbuilding, characters, outline


def get_chapter_index(project_id: str) -> dict:
    """获取章节索引。"""
    chapters_yaml = get_project_dir(project_id) / "chapters" / "_index.yaml"
    return load_yaml(chapters_yaml)


def get_chapter_file(project_id: str, chapter_num: int) -> Path:
    """获取章节文件路径。"""
    return get_project_dir(project_id) / "chapters" / f"chapter_{chapter_num:03d}.md"


def count_words(text: str) -> int:
    """统计中文字数（排除空格、标点等）。"""
    # 统计中文字符
    chinese_chars = len(re.findall(r"[一-龥]", text))
    # 统计英文单词（按空格分割）
    english_words = len(re.findall(r"[a-zA-Z]+", text))
    return chinese_chars + english_words


def update_chapter_index(project_id: str, chapter_num: int, words: int, status: str):
    """更新章节索引。"""
    chapters_yaml = get_project_dir(project_id) / "chapters" / "_index.yaml"
    index = load_yaml(chapters_yaml)

    # 找到对应章节并更新
    for chapter in index.get("chapters", []):
        if chapter.get("chapter") == chapter_num:
            chapter["words"] = words
            chapter["status"] = status
            break

    # 更新统计
    total_words = sum(c.get("words", 0) for c in index.get("chapters", []))
    written_count = sum(1 for c in index.get("chapters", []) if c.get("status") in ["written", "revised"])
    draft_count = sum(1 for c in index.get("chapters", []) if c.get("status") == "draft")

    index["stats"] = {
        "total": len(index.get("chapters", [])),
        "planned": sum(1 for c in index.get("chapters", []) if c.get("status") == "planned"),
        "draft": draft_count,
        "written": written_count,
        "revised": sum(1 for c in index.get("chapters", []) if c.get("status") == "revised"),
        "total_words": total_words,
    }

    save_yaml(chapters_yaml, index)

    # 更新项目统计
    project_yaml = get_project_dir(project_id) / "project.yaml"
    project = load_yaml(project_yaml)
    project["stats"]["chapters_written"] = written_count + draft_count
    project["stats"]["words_total"] = total_words
    project["updated"] = datetime.now().strftime("%Y-%m-%d")
    save_yaml(project_yaml, project)


def save_history(project_id: str, action: str, chapter_num: int, prompt: str, content: str):
    """保存写作历史。"""
    history_dir = get_project_dir(project_id) / "history"
    history_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = history_dir / f"{action}_ch{chapter_num}_{timestamp}.yaml"
    history_data = {
        "action": action,
        "chapter": chapter_num,
        "timestamp": timestamp,
        "prompt": prompt,
        "content": content,
        "words": count_words(content),
        "api_stats": get_api_stats(),
    }
    save_yaml(history_file, history_data)


# ──────────────────────────────────────────────
# 章节生成
# ──────────────────────────────────────────────

WRITE_NEW_SYSTEM_PROMPT = """你是一个专业的小说写作助手。
根据章节大纲和设定，生成小说章节正文。

要求：
1. 使用 Markdown 格式输出正文
2. 保持风格一致性
3. 情节要符合大纲节拍
4. 人物行为要符合设定
5. 张力要符合节奏曲线
6. 正文开头不要标题，直接开始正文

输出纯正文内容，不要包含任何解释或说明。"""


def write_new_chapter(project_id: str, chapter_num: int, prompt: str = None) -> str:
    """生成新章节正文。"""
    reset_api_stats()
    project = load_project(project_id)
    worldbuilding, characters, outline = load_settings(project_id)
    index = get_chapter_index(project_id)

    # 获取章节信息
    chapter_info = None
    for c in index.get("chapters", []):
        if c.get("chapter") == chapter_num:
            chapter_info = c
            break

    if not chapter_info:
        raise ValueError(f"章节 {chapter_num} 未规划，请先运行 generate chapter")

    # 获取前一章内容（作为上下文）
    prev_chapter_file = get_chapter_file(project_id, chapter_num - 1)
    prev_content = ""
    if prev_chapter_file.exists():
        prev_content = prev_chapter_file.read_text(encoding="utf-8")
        # 只取最后 500 字作为衔接参考
        if len(prev_content) > 500:
            prev_content = "..." + prev_content[-500:]

    # 构建用户提示
    user_prompt = f"""请为以下小说生成第 {chapter_num} 章正文：

小说名称：{project.get('name')}
类型：{project.get('genre')}

世界观概要：
- 类型：{worldbuilding.get('world_type')}
- 力量体系：{worldbuilding.get('power_system', {}).get('name', '无')}

主要人物：
{json.dumps([{'name': c.get('name'), 'role': c.get('role'), 'traits': c.get('traits')} for c in characters.get('characters', [])[:5]], ensure_ascii=False)}

本章节信息：
- 标题：{chapter_info.get('title')}
- 摘要：{chapter_info.get('summary')}
- 张力值：{chapter_info.get('tension')}
- 出场人物：{chapter_info.get('characters', [])}
- 功能：{chapter_info.get('functions', [])}

前一章结尾（用于衔接）：
{prev_content if prev_content else '这是第一章'}

用户额外要求：{prompt or '无'}

请生成约 2000-3000 字的章节正文。"""

    print(f"🤖 正在生成第 {chapter_num} 章正文...")
    print(f"   标题: {chapter_info.get('title')}")
    print(f"   描述: {prompt or '自动生成'}")

    config = load_config()
    content = call_llm(
        system_prompt=WRITE_NEW_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        config=config,
        max_tokens_override=4096,
        timeout_override=180,
        json_response=False,
    )

    # 保存章节文件
    chapter_file = get_chapter_file(project_id, chapter_num)
    chapter_file.write_text(content, encoding="utf-8")

    # 更新索引和统计
    words = count_words(content)
    status = "draft" if words < 1500 else "written"
    update_chapter_index(project_id, chapter_num, words, status)

    # 保存历史
    save_history(project_id, "write_new", chapter_num, user_prompt, content)

    stats = get_api_stats()
    print(f"✅ 第 {chapter_num} 章生成完成")
    print(f"   字数: {words}")
    print(f"   状态: {status}")
    print(f"   API 调用: {stats['calls']} 次 | Tokens: {stats['tokens_total']}")

    return content


# ──────────────────────────────────────────────
# 章节续写
# ──────────────────────────────────────────────

WRITE_CONTINUE_SYSTEM_PROMPT = """你是一个专业的小说写作助手。
根据已有内容和设定，续写小说章节。

要求：
1. 保持风格和情节连贯
2. 续写内容要自然衔接
3. 推进情节发展
4. 输出纯正文内容，不要包含任何解释

输出续写内容，不要重复已有内容。"""


def write_continue_chapter(project_id: str, chapter_num: int, length: int = 1000) -> str:
    """续写章节。"""
    reset_api_stats()
    project = load_project(project_id)
    worldbuilding, characters, outline = load_settings(project_id)

    # 获取章节文件
    chapter_file = get_chapter_file(project_id, chapter_num)
    if not chapter_file.exists():
        raise FileNotFoundError(f"章节 {chapter_num} 文件不存在，请先使用 write-new 生成")

    existing_content = chapter_file.read_text(encoding="utf-8")

    # 构建用户提示
    user_prompt = f"""请续写第 {chapter_num} 章：

小说名称：{project.get('name')}

已有内容（最后部分）：
...{existing_content[-800:] if len(existing_content) > 800 else existing_content}

续写要求：
- 续写约 {length} 字
- 保持风格一致
- 自然衔接已有内容
- 推进情节发展

请输出续写内容。"""

    print(f"🤖 正在续写第 {chapter_num} 章...")
    print(f"   已有字数: {count_words(existing_content)}")
    print(f"   续写字数: {length}")

    config = load_config()
    new_content = call_llm(
        system_prompt=WRITE_CONTINUE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        config=config,
        max_tokens_override=2048,
        json_response=False,
    )

    # 合并内容
    full_content = existing_content + "\n\n" + new_content
    chapter_file.write_text(full_content, encoding="utf-8")

    # 更新统计
    words = count_words(full_content)
    status = "draft" if words < 1500 else "written"
    update_chapter_index(project_id, chapter_num, words, status)

    # 保存历史
    save_history(project_id, "write_continue", chapter_num, user_prompt, new_content)

    stats = get_api_stats()
    print(f"✅ 第 {chapter_num} 章续写完成")
    print(f"   新增字数: {count_words(new_content)}")
    print(f"   总字数: {words}")
    print(f"   API 调用: {stats['calls']} 次 | Tokens: {stats['tokens_total']}")

    return new_content


# ──────────────────────────────────────────────
# 章节改写
# ──────────────────────────────────────────────

REVISE_MODE_PROMPTS = {
    "polish": "润色已有内容，保持情节不变，优化表达和文笔。",
    "expand": "扩充内容，增加细节描写、环境描写、心理描写。",
    "condense": "精简内容，删减冗余，保留核心情节。",
    "rewrite": "重写章节，保留章节大纲，重新生成全部内容。",
}

WRITE_REVISE_SYSTEM_PROMPT = """你是一个专业的小说写作助手。
根据要求改写小说章节。

要求：
1. 输出改写后的完整章节正文
2. 保持风格一致
3. 输出纯正文内容

输出改写后的完整内容。"""


def write_revise_chapter(project_id: str, chapter_num: int, mode: str = "polish") -> str:
    """改写章节。"""
    reset_api_stats()
    project = load_project(project_id)
    worldbuilding, characters, outline = load_settings(project_id)

    # 获取章节文件
    chapter_file = get_chapter_file(project_id, chapter_num)
    if not chapter_file.exists():
        raise FileNotFoundError(f"章节 {chapter_num} 文件不存在")

    existing_content = chapter_file.read_text(encoding="utf-8")
    revise_instruction = REVISE_MODE_PROMPTS.get(mode, REVISE_MODE_PROMPTS["polish"])

    # 获取章节信息
    index = get_chapter_index(project_id)
    chapter_info = None
    for c in index.get("chapters", []):
        if c.get("chapter") == chapter_num:
            chapter_info = c
            break

    # 构建用户提示
    user_prompt = f"""请改写第 {chapter_num} 章：

小说名称：{project.get('name')}

章节标题：{chapter_info.get('title') if chapter_info else '未知'}
章节摘要：{chapter_info.get('summary') if chapter_info else '无'}

原始内容：
{existing_content}

改写模式：{mode}
改写说明：{revise_instruction}

请输出改写后的完整章节内容。"""

    print(f"🤖 正在改写第 {chapter_num} 章...")
    print(f"   模式: {mode}")
    print(f"   原字数: {count_words(existing_content)}")

    config = load_config()
    revised_content = call_llm(
        system_prompt=WRITE_REVISE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        config=config,
        max_tokens_override=4096,
        timeout_override=180,
        json_response=False,
    )

    # 备份原内容
    backup_file = chapter_file.with_suffix(".bak")
    backup_file.write_text(existing_content, encoding="utf-8")

    # 保存改写内容
    chapter_file.write_text(revised_content, encoding="utf-8")

    # 更新统计
    words = count_words(revised_content)
    status = "revised"
    update_chapter_index(project_id, chapter_num, words, status)

    # 保存历史
    save_history(project_id, f"write_revise_{mode}", chapter_num, user_prompt, revised_content)

    stats = get_api_stats()
    print(f"✅ 第 {chapter_num} 章改写完成")
    print(f"   新字数: {words}")
    print(f"   状态: {status}")
    print(f"   API 调用: {stats['calls']} 次 | Tokens: {stats['tokens_total']}")

    return revised_content


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────

def main():
    if len(sys.argv) < 4:
        print("用法:")
        print("  python scripts/write.py new <project_id> <章节号> [--prompt <描述>]")
        print("  python scripts/write.py continue <project_id> <章节号> [--length <字数>]")
        print("  python scripts/write.py revise <project_id> <章节号> [--mode <模式>]")
        print()
        print("改写模式：polish（润色）、expand（扩充）、condense（精简）、rewrite（重写）")
        sys.exit(1)

    command = sys.argv[1]
    project_id = sys.argv[2]
    chapter_num = int(sys.argv[3])

    # 解析可选参数
    prompt = None
    length = 1000
    mode = "polish"

    i = 4
    while i < len(sys.argv):
        if sys.argv[i] == "--prompt" and i + 1 < len(sys.argv):
            prompt = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--length" and i + 1 < len(sys.argv):
            length = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--mode" and i + 1 < len(sys.argv):
            mode = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    try:
        if command == "new":
            write_new_chapter(project_id, chapter_num, prompt)
        elif command == "continue":
            write_continue_chapter(project_id, chapter_num, length)
        elif command == "revise":
            write_revise_chapter(project_id, chapter_num, mode)
        else:
            print(f"未知命令: {command}")
            print("可用命令: new, continue, revise")
            sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 写作失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()