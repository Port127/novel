#!/usr/bin/env python
"""AI 生成脚本：使用 LLM 生成世界观、大纲、人物、章节计划。

用法:
    python scripts/generate.py world <project_id> [--prompt <描述>] [--from-draft <草稿文件>]
    python scripts/generate.py outline <project_id> [--chapters <章节数>] [--prompt <描述>] [--from-draft <草稿文件>]
    python scripts/generate.py character <project_id> [--prompt <描述>] [--from-draft <草稿文件>]
    python scripts/generate.py chapter <project_id> [--from-outline] [--from-draft <草稿文件>]

草稿来源可以是：
    --from-draft notes.yaml     # 从项目内的 notes.yaml 读取
    --from-draft path/to/file   # 从指定文件读取
    --from-draft "直接内容"     # 直接使用提供的文本
"""
import sys
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


def load_draft(project_id: str, draft_source: str, draft_type: str = "outline") -> str:
    """加载草稿内容。

    Args:
        project_id: 项目ID
        draft_source: 草稿来源（文件路径、"notes.yaml" 或直接内容）
        draft_type: 草稿类型（outline/character/chapter），用于从 notes.yaml 读取对应字段

    Returns:
        草稿文本内容
    """
    if not draft_source:
        return ""

    # 如果是 notes.yaml，从项目内的 notes.yaml 读取对应字段
    if draft_source == "notes.yaml" or draft_source == "notes":
        notes_file = get_project_dir(project_id) / "settings" / "notes.yaml"
        if not notes_file.exists():
            print(f"⚠️  notes.yaml 不存在")
            return ""
        notes_data = load_yaml(notes_file)
        # 尝试读取对应类型的草稿字段
        draft_field = f"{draft_type}_draft"
        if notes_data.get(draft_field):
            return notes_data[draft_field]
        # 也尝试读取通用的 idea 字段
        if notes_data.get("idea"):
            return notes_data["idea"]
        print(f"⚠️  notes.yaml 中未找到 {draft_field} 或 idea 字段")
        return ""

    # 如果是文件路径，尝试读取文件
    draft_path = Path(draft_source)
    if draft_path.exists():
        content = draft_path.read_text(encoding="utf-8")
        # 如果是 yaml 文件，尝试提取相关字段
        if draft_path.suffix in [".yaml", ".yml"]:
            try:
                draft_data = yaml.safe_load(content)
                if isinstance(draft_data, dict):
                    # 尝试找到相关内容
                    for key in [draft_type, f"{draft_type}_draft", "idea", "content", "draft"]:
                        if draft_data.get(key):
                            if isinstance(draft_data[key], str):
                                return draft_data[key]
                            elif isinstance(draft_data[key], dict):
                                return yaml.dump(draft_data[key], allow_unicode=True)
            except:
                pass
        return content

    # 否则视为直接提供的文本内容
    return draft_source


def update_project_timestamp(project_id: str):
    """更新项目时间戳。"""
    project_yaml = get_project_dir(project_id) / "project.yaml"
    data = load_yaml(project_yaml)
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    save_yaml(project_yaml, data)


def save_history(project_id: str, action: str, prompt: str, result: dict, draft_source: str = None):
    """保存 AI 生成历史。"""
    history_dir = get_project_dir(project_id) / "history"
    history_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = history_dir / f"{action}_{timestamp}.yaml"
    history_data = {
        "action": action,
        "timestamp": timestamp,
        "prompt": prompt,
        "draft_source": draft_source,
        "result": result,
        "api_stats": get_api_stats(),
    }
    save_yaml(history_file, history_data)


# ──────────────────────────────────────────────
# 世界观生成
# ──────────────────────────────────────────────

WORLD_SYSTEM_PROMPT = """你是一个专业的小说世界观设计助手。
根据用户的描述，生成一个完整的小说世界观设定。

返回 JSON 格式，包含以下字段：
- world_type: 世界观类型（如：修仙、都市、科幻、悬疑、历史、武侠、奇幻）
- setting_period: 时间背景
- power_system: 力量体系对象
  - name: 体系名称
  - type: 体系类型（灵气/魔法/斗气/科技/超能力）
  - ranks: 等级列表（每个等级包含 name, description, capabilities）
  - rules: 规则列表
  - limitations: 限制列表
- factions: 势力列表（每个势力包含 name, type, stance, territory, key_figures, description）
- locations: 地点列表（每个地点包含 name, type, description, significance）
- lore: 背景知识
  - history: 历史事件列表
  - artifacts: 重要物品列表
  - terminology: 术语列表

注意：
1. 等级体系要合理，一般 5-10 级
2. 势力之间要有关系（正派/中立/反派）
3. 规则要能推动剧情发展
"""


def generate_world(project_id: str, prompt: str = None, draft: str = None) -> dict:
    """生成世界观设定。

    Args:
        project_id: 项目ID
        prompt: 用户额外描述
        draft: 草稿来源（文件路径、"notes.yaml" 或直接内容）
    """
    reset_api_stats()
    project = load_project(project_id)
    settings_dir = get_project_dir(project_id) / "settings"

    # 加载现有世界观作为上下文
    existing_world = load_yaml(settings_dir / "worldbuilding.yaml")
    genre = project.get("genre", "修仙")

    # 加载草稿内容
    draft_content = load_draft(project_id, draft, "world") if draft else ""

    # 构建用户提示
    draft_section = ""
    if draft_content:
        draft_section = f"""
用户提供的草稿/想法：
{draft_content}
"""

    prompt_section = ""
    if prompt:
        prompt_section = f"""
用户额外要求：{prompt}
"""

    user_prompt = f"""请为以下小说生成世界观设定：

小说名称：{project.get('name')}
类型：{genre}

现有世界观（可参考或补充）：{json.dumps(existing_world, ensure_ascii=False) if existing_world.get('world_type') else '未设定'}
{draft_section}{prompt_section}
请根据以上信息生成完整的世界观设定。"""

    print(f"🤖 正在生成世界观设定...")
    print(f"   类型: {genre}")
    if draft_content:
        print(f"   草稿来源: {draft}")
    print(f"   描述: {prompt or '根据设定生成'}")

    config = load_config()
    result = call_llm(
        system_prompt=WORLD_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        config=config,
        max_tokens_override=4096,
    )

    # 保存结果
    save_yaml(settings_dir / "worldbuilding.yaml", result)
    save_history(project_id, "generate_world", user_prompt, result, draft)
    update_project_timestamp(project_id)

    stats = get_api_stats()
    print(f"✅ 世界观生成完成")
    print(f"   力量等级数: {len(result.get('power_system', {}).get('ranks', []))}")
    print(f"   势力数: {len(result.get('factions', []))}")
    print(f"   地点数: {len(result.get('locations', []))}")
    print(f"   API 调用: {stats['calls']} 次 | Tokens: {stats['tokens_total']}")

    return result


# ──────────────────────────────────────────────
# 大纲生成
# ──────────────────────────────────────────────

OUTLINE_SYSTEM_PROMPT = """你是一个专业的小说大纲设计助手。
根据世界观和用户描述，生成完整的小说大纲。

返回 JSON 格式，包含以下字段：
- premise: 核心前提（一句话概括）
- theme: 主题标签列表
- tone: 基调标签列表
- acts: 幕列表（每幕包含）
  - act: 幕编号
  - title: 幕名称
  - chapters: [起始章, 结束章]
  - arc: 叙事弧线描述
  - sequences: 序列列表（每个序列包含）
    - sequence: 序列编号
    - title: 序列名称
    - chapters: [起始章, 结束章]
    - beats: 节拍列表（每个节拍包含）
      - beat: 节拍编号
      - title: 节拍名称
      - chapter: 所在章节
      - description: 节拍描述
      - tension: 张力值（1-5）
  - turning_point: 转折点信息
    - chapter: 转折章节
    - description: 转折描述
    - type: 转折类型（inciting_incident/first_threshold/midpoint/dark_night/climax）
- hooks: 钩子列表（可选，每个包含 hook_id, hook_type, planted_chapter, detail, harvested_chapter, resolution）
- pacing_curve: 节奏曲线关键节点（可选）

注意：
1. 三幕式结构：第一幕（铺垫）、第二幕（冲突）、第三幕（解决）
2. 每幕的章节范围要根据总章节数合理分配
3. 转折点要明确
"""


def generate_outline(project_id: str, chapters: int = 50, prompt: str = None, draft: str = None) -> dict:
    """生成大纲设定。

    Args:
        project_id: 项目ID
        chapters: 预计章节数
        prompt: 用户额外描述
        draft: 草稿来源（文件路径、"notes.yaml" 或直接内容）
    """
    reset_api_stats()
    project = load_project(project_id)
    settings_dir = get_project_dir(project_id) / "settings"

    # 加载世界观作为上下文
    worldbuilding = load_yaml(settings_dir / "worldbuilding.yaml")
    characters = load_yaml(settings_dir / "characters.yaml")

    # 加载草稿内容
    draft_content = load_draft(project_id, draft, "outline") if draft else ""

    if not worldbuilding.get("world_type"):
        print("⚠️  建议：先生成世界观设定（generate-world），以便大纲更完整")

    # 构建用户提示
    draft_section = ""
    if draft_content:
        draft_section = f"""
用户提供的草稿/想法：
{draft_content}
"""

    prompt_section = ""
    if prompt:
        prompt_section = f"""
用户额外要求：{prompt}
"""

    user_prompt = f"""请为以下小说生成大纲：

小说名称：{project.get('name')}
类型：{project.get('genre')}
预计章节数：{chapters}

世界观设定：{json.dumps(worldbuilding, ensure_ascii=False) if worldbuilding.get('world_type') else '未设定'}

现有人物：{json.dumps(characters.get('characters', []), ensure_ascii=False) if characters.get('characters') else '未设定'}
{draft_section}{prompt_section}
请根据以上信息生成完整的大纲结构。"""

    print(f"🤖 正在生成大纲...")
    print(f"   章节数: {chapters}")
    if draft_content:
        print(f"   草稿来源: {draft}")
    print(f"   描述: {prompt or '根据设定生成'}")

    config = load_config()
    result = call_llm(
        system_prompt=OUTLINE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        config=config,
        max_tokens_override=8192,
        timeout_override=180,
    )

    # 保存结果
    save_yaml(settings_dir / "outline.yaml", result)
    save_history(project_id, "generate_outline", user_prompt, result, draft)
    update_project_timestamp(project_id)

    # 更新项目统计
    project_yaml = get_project_dir(project_id) / "project.yaml"
    project_data = load_yaml(project_yaml)
    project_data["stats"]["chapters_planned"] = chapters
    save_yaml(project_yaml, project_data)

    stats = get_api_stats()
    print(f"✅ 大纲生成完成")
    print(f"   幕数: {len(result.get('acts', []))}")
    total_beats = sum(
        len(seq.get("beats", []))
        for act in result.get("acts", [])
        for seq in act.get("sequences", [])
    )
    print(f"   节拍数: {total_beats}")
    print(f"   API 调用: {stats['calls']} 次 | Tokens: {stats['tokens_total']}")

    return result


# ──────────────────────────────────────────────
# 人物生成
# ──────────────────────────────────────────────

CHARACTER_SYSTEM_PROMPT = """你是一个专业的小说人物设计助手。
根据世界观和用户描述，生成小说人物设定。

返回 JSON 格式，包含以下字段：
- characters: 人物列表（每个人物包含）
  - name: 人物名称
  - role: 角色类型（protagonist/antagonist/supporting/minor）
  - archetype: 人物原型
  - description: 核心描述
  - traits: 性格特征列表
  - psychology: 心理维度（主角/反派必填）
    - fatal_flaw: 关键缺陷
    - obsession: 执念
    - soft_spot: 软肋
    - misbelief: 误判
  - arc: 人物弧线
    - type: 弧线类型（成长弧线/堕落弧线/悲剧弧线/探索弧线）
    - start: 起点状态
    - end: 终点状态
    - stages: 弧线阶段列表（可选）
  - key_events: 关键事件列表（可选）
  - relationships: 关系列表（可选）
  - appearance: 外貌描述（可选）
  - faction_affiliations: 阵营归属（可选）

注意：
1. 至少生成一个主角（protagonist）
2. 主角要有完整的心理维度和弧线
3. 人物之间要有关系网络
"""


def generate_character(project_id: str, prompt: str = None, draft: str = None) -> dict:
    """生成人物设定。

    Args:
        project_id: 项目ID
        prompt: 用户额外描述
        draft: 草稿来源（文件路径、"notes.yaml" 或直接内容）
    """
    reset_api_stats()
    project = load_project(project_id)
    settings_dir = get_project_dir(project_id) / "settings"

    # 加载世界观和大纲作为上下文
    worldbuilding = load_yaml(settings_dir / "worldbuilding.yaml")
    outline = load_yaml(settings_dir / "outline.yaml")

    # 加载草稿内容
    draft_content = load_draft(project_id, draft, "character") if draft else ""

    if not worldbuilding.get("world_type"):
        print("⚠️  建议：先生成世界观设定（generate-world）")

    # 构建用户提示
    draft_section = ""
    if draft_content:
        draft_section = f"""
用户提供的草稿/想法：
{draft_content}
"""

    prompt_section = ""
    if prompt:
        prompt_section = f"""
用户额外要求：{prompt}
"""

    user_prompt = f"""请为以下小说生成人物设定：

小说名称：{project.get('name')}
类型：{project.get('genre')}

世界观设定：{json.dumps(worldbuilding, ensure_ascii=False) if worldbuilding.get('world_type') else '未设定'}

大纲概要：{json.dumps({'premise': outline.get('premise'), 'theme': outline.get('theme')}, ensure_ascii=False) if outline.get('premise') else '未设定'}
{draft_section}{prompt_section}
请根据以上信息生成完整的人物设定。"""

    print(f"🤖 正在生成人物...")
    if draft_content:
        print(f"   草稿来源: {draft}")
    print(f"   描述: {prompt or '根据设定生成'}")

    config = load_config()
    result = call_llm(
        system_prompt=CHARACTER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        config=config,
        max_tokens_override=4096,
    )

    # 保存结果
    save_yaml(settings_dir / "characters.yaml", result)
    save_history(project_id, "generate_character", user_prompt, result, draft)
    update_project_timestamp(project_id)

    stats = get_api_stats()
    print(f"✅ 人物生成完成")
    chars = result.get("characters", [])
    roles_count = {}
    for c in chars:
        role = c.get("role", "unknown")
        roles_count[role] = roles_count.get(role, 0) + 1
    print(f"   总人物数: {len(chars)}")
    for role, count in roles_count.items():
        print(f"   {role}: {count}")
    print(f"   API 调用: {stats['calls']} 次 | Tokens: {stats['tokens_total']}")

    return result


# ──────────────────────────────────────────────
# 章节规划生成
# ──────────────────────────────────────────────

CHAPTER_PLAN_SYSTEM_PROMPT = """你是一个专业的小说章节规划助手。
根据大纲，生成章节计划。

返回 JSON 格式，包含以下字段：
- chapters: 章节列表（每章包含）
  - chapter: 章节号
  - title: 章节标题
  - status: 状态（planned）
  - words: 0
  - summary: 章节摘要
  - tension: 张力值（1-5）
  - characters: 出场人物列表（可选）
  - functions: 章节功能标签（可选）
  - beat_ref: 对应大纲节拍（可选）
    - act: 幕编号
    - sequence: 序列编号
    - beat: 节拍编号
- stats: 统计信息
  - total: 总章数
  - planned: 已规划数
  - draft: 0
  - written: 0
  - revised: 0
  - total_words: 0

注意：
1. 每章要有明确的摘要
2. 张力值要符合节奏曲线
"""


def generate_chapter_plan(project_id: str, from_outline: bool = True, draft: str = None) -> dict:
    """生成章节规划。

    Args:
        project_id: 项目ID
        from_outline: 是否从大纲生成
        draft: 草稿来源（文件路径、"notes.yaml" 或直接内容）
    """
    reset_api_stats()
    project = load_project(project_id)
    settings_dir = get_project_dir(project_id) / "settings"
    chapters_dir = get_project_dir(project_id) / "chapters"

    # 加载大纲和人物作为上下文
    outline = load_yaml(settings_dir / "outline.yaml")
    characters = load_yaml(settings_dir / "characters.yaml")

    # 加载草稿内容
    draft_content = load_draft(project_id, draft, "chapter") if draft else ""

    if not outline.get("acts"):
        print("❌ 请先生成大纲（generate-outline）")
        return {}

    # 构建用户提示
    draft_section = ""
    if draft_content:
        draft_section = f"""
用户提供的草稿/想法：
{draft_content}
"""

    user_prompt = f"""请根据以下大纲生成章节计划：

小说名称：{project.get('name')}

大纲结构：{json.dumps(outline, ensure_ascii=False)}

人物列表：{json.dumps([c.get('name') for c in characters.get('characters', [])], ensure_ascii=False) if characters.get('characters') else '未设定'}
{draft_section}
请将大纲的每个节拍转化为章节，生成章节计划。"""

    print(f"🤖 正在生成章节规划...")
    if draft_content:
        print(f"   草稿来源: {draft}")

    config = load_config()
    result = call_llm(
        system_prompt=CHAPTER_PLAN_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        config=config,
        max_tokens_override=8192,
        timeout_override=180,
    )

    # 保存结果
    save_yaml(chapters_dir / "_index.yaml", result)
    save_history(project_id, "generate_chapter_plan", user_prompt, result, draft)
    update_project_timestamp(project_id)

    stats = get_api_stats()
    print(f"✅ 章节规划完成")
    print(f"   总章数: {len(result.get('chapters', []))}")
    print(f"   API 调用: {stats['calls']} 次 | Tokens: {stats['tokens_total']}")

    return result


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python scripts/generate.py world <project_id> [--prompt <描述>] [--from-draft <草稿>]")
        print("  python scripts/generate.py outline <project_id> [--chapters <章节数>] [--prompt <描述>] [--from-draft <草稿>]")
        print("  python scripts/generate.py character <project_id> [--prompt <描述>] [--from-draft <草稿>]")
        print("  python scripts/generate.py chapter <project_id> [--from-outline] [--from-draft <草稿>]")
        print()
        print("草稿来源可以是：")
        print("  --from-draft notes.yaml     从项目内的 notes.yaml 读取")
        print("  --from-draft path/to/file   从指定文件读取")
        print("  --from-draft \"直接内容\"     直接使用提供的文本")
        sys.exit(1)

    command = sys.argv[1]
    project_id = sys.argv[2]

    # 解析可选参数
    prompt = None
    chapters = 50
    from_outline = True
    draft = None

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--prompt" and i + 1 < len(sys.argv):
            prompt = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--chapters" and i + 1 < len(sys.argv):
            chapters = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--from-outline":
            from_outline = True
            i += 1
        elif sys.argv[i] == "--from-draft" and i + 1 < len(sys.argv):
            draft = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    try:
        if command == "world":
            generate_world(project_id, prompt, draft)
        elif command == "outline":
            generate_outline(project_id, chapters, prompt, draft)
        elif command == "character":
            generate_character(project_id, prompt, draft)
        elif command == "chapter":
            generate_chapter_plan(project_id, from_outline, draft)
        else:
            print(f"未知命令: {command}")
            print("可用命令: world, outline, character, chapter")
            sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()