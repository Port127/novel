---
name: character-add
description: 创建新角色，并补齐缺陷、执念、软肋和反差特征，让角色更立体、更可用于冲突和弧光设计。
when_to_use: 用户想要创建新的小说角色，或觉得角色只有身份标签还不够立体
argument-hint: "[姓名] [定位] [年龄] [身份] [性格]..."
arguments: name role age identity personality
---

# 任务

创建一个新角色，生成角色卡片并更新项目状态。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 如果为空，提示：`请先使用 /novel-init 创建项目`
3. 检查 `$0` 是否提供，未提供则询问

## 输入参数

- `$0` (name): 姓名（必需，除批量模式外）
- `$1` (role): 角色定位（主角/配角/反派/路人等）
- `$2` (age): 年龄
- `$3` (identity): 身份/职业
- `$4+` (personality): 性格特点等额外信息
- `--from`: 从文件或引用内容中提取角色信息（见步骤 0）
- `--quick`: 跳过逐条确认，快速落地（设定标 tentative 级）

参数格式灵活，支持：
- `/character-add 张三 主角 25岁 剑客 隐忍坚毅`
- `/character-add 李四，反派，50岁，宗门长老`
- `/character-add 林砚 配角 19岁 学徒 温顺敏感 但极度怕被抛下`
- `/character-add 张三 --from drafts/张三参考.md`（用参考内容填充单人角色卡）
- `/character-add --from chapters/ch003.md`（批量：扫描章节中所有出场角色）

## 执行步骤

### 0. 引用模式（--from）

当指定 `--from` 时，按 [引用提取协议](_protocols/from-extraction.md) 执行提取与确认流程。

根据是否同时提供了姓名，分两种子模式：

**A. 单人参考模式**（提供了姓名 + `--from`）：
将 `--from` 内容视为**该角色的参考资料**（灵感来源、人设笔记、原型描述等），从中提炼并填充角色卡字段。重点：
- 从参考内容中提炼性格、缺陷、执念等，用自己的语言重新组织，不照搬原文
- 如果参考内容包含灵感来源（如"参考了某角色"），记入 `notes` 而非写进人设字段
- 提炼结果展示给用户确认后写入

**B. 批量提取模式**（只有 `--from`，无姓名）：
扫描源文件中的所有人物，逐个提取。重点：
- 扫描人物姓名、身份、性格、行为特征
- 从对白和行为推断缺陷、执念、软肋等立体化字段
- 每个角色拆为一条创建请求，逐个确认（加 `--quick` 跳过确认）
- 5 人以上时先输出汇总表，用户选择要创建哪些

### 1. 检查是否已存在

读取 `{current_path}/.novel/state.yaml` 的 `characters` 列表。

如果同名角色已存在：
- 询问用户是否编辑现有角色（调用 /character-edit）
- 或创建新版本

### 2. 创建结构化角色档案

写入 `{current_path}/characters/$0.yaml`（基于 `templates/project/characters/character.yaml`）：

除基本信息外，优先补齐以下立体化字段：
- 会害到自己的缺陷
- 放不下的执念
- 真正在意的人或事
- 一条反差习惯或反差反应
- 一条容易触发悲剧的误判或结构点
- 语言画像（speech_pattern）——这个角色"怎么说话"

```yaml
name: "$0"
aliases: []
role: $1          # protagonist / supporting / minor / antagonist
archetype: ""
narrative_function: ""
first_appearance: ""
first_scene: ""

profile:
  age: "$2"
  gender: ""
  occupation: "$3"
  affiliation: []
  location: ""

traits: [$4]
moral_spectrum: ""
fatal_flaw: ""
obsession: ""
soft_spot: ""
misbelief: ""
contrast_habit: ""
tragedy_trigger: ""

speech_pattern:
  tone: ""
  sentence_style: ""
  catchphrase: []
  profanity_level: ""
  education_voice: ""
  verbal_tics: []
  taboo_words: []
  sample_lines: []

appearance: ""
backstory: ""
abilities: []

arc: []

relations: []

appearance_stats:
  scene_count: 0
  active_chapters: ""
  dominant_scene_types: []
  tension_avg: 0

notes: ""
```

### 3. 更新人物索引

在 `{current_path}/characters/character_index.yaml` 追加条目：

```yaml
entries:
  - name: "$0"
    role: $1
    archetype: ""
    file: characters/$0.yaml
    first_appearance: ""
    affiliation: []
    scene_count: 0
```

### 4. 更新项目状态

更新 `{current_path}/.novel/state.yaml`：
- `project.updated`：今天日期

**成功标准**: `characters/$0.yaml` 创建，`character_index.yaml` 已追加

## 输出格式

```
✅ 角色创建完成

👤 姓名：$0
🎭 定位：$1
🎂 年龄：$2
⚔️ 身份：$3

📄 文件：characters/$0.yaml

下一步：
   /character-edit $0 补充缺陷/执念/软肋/弧光
   /relationship-add $0 [其他角色] [关系] 建立关系
   /character-add [另一个角色] 继续创建
```

## 模板

角色档案模板位于 `templates/project/characters/character.yaml`。

## 注意事项

- 姓名作为文件名，特殊字符替换为下划线
- 信息较少时生成基础档案，后续可通过 /character-edit 补充
- 自动记录创建日期
- `character_index.yaml` 不存在时自动创建
- 优先给角色一个会伤到自己的缺点、误判或执念，不要只有优点标签
- `speech_pattern` 至少填 `tone`、`profanity_level` 和 1-2 条 `sample_lines`——从角色的性格、身份、教育水平推断说话方式。如果用户给了对白样本或参考内容（`--from`），优先从中提炼语言特征