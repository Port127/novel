# Novel V2

小说写作工具，支持交互式创作和 CLI 操作。

## 项目定位

- **novel-material**（上游）：素材检索库，存储已有小说的结构化分析结果
- **novel-v2**（本项目）：写作工具，用于创作新小说

## 核心功能

| 功能 | 说明 |
|------|------|
| 项目管理 | 创建/删除/查看写作项目 |
| 设定生成 | AI 生成世界观、大纲、人物设定 |
| 章节规划 | 将大纲转化为章节摘要和张力曲线 |
| 正文写作 | AI 生成、续写、改写章节内容 |
| 导出 | 导出 TXT/Markdown/EPUB 格式 |

## 使用方式

### 方式一：交互式对话（推荐）

直接和 Claude 对话，Claude 会调用 Skill 交互式创作：

```
"帮我写个大纲"
→ Claude 询问核心想法 → 逐步细化 → 生成大纲 → 展示调整

"帮我设计人物"
→ Claude 询问主角设定 → 反派 → 配角 → 生成人物 → 展示关系网络

"规划章节"
→ Claude 确认大纲 → 生成章节计划 → 展示张力曲线

"写第1章"
→ Claude 确认章节信息 → 询问写作方向 → 生成正文 → 展示调整选项
```

### 方式二：CLI 命令行工具

通过全新重构的 CLI 工具进行项目管理：

```bash
# 1. 环境安装
make install

# 2. 创建新项目
novel new my_project_name --genre 修仙 --author "作者名"

# 3. 列出所有项目
novel list

# 4. 查看项目详情
novel show nv_xxxxxxxx

# 5. 删除项目
novel delete nv_xxxxxxxx

```bash
# 创建项目（使用模板）
novel new "我的小说" --genre 修仙 --author 作者名 --template default

# 查看项目列表
novel list

# 查看项目详情
novel show <project_id>

# 使用 Skills 完成设定（推荐）
```

## 安装配置

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入：
# - LLM_API_KEY（必须，用于 AI 生成）
# - LLM_API_BASE（可选，默认 OpenAI）
# - LLM_MODEL（可选，默认 gpt-4o-mini）
```

## 目录结构

```
novel-v2/
├── templates/                 # 项目模板
│   └── default/               # 默认模板（800章规模）
│       ├── project.yaml       # 项目元信息模板
│       ├── settings/          # 设定模板（模块化目录）
│       │   ├── worldbuilding/
│       │   ├── characters/
│       │   ├── outline/
│       │   └── chapters/
│       └── content/chapters/  # 正文目录模板
│
├── novels/                    # 写作项目目录
│   └── {project_id}/          # 单个项目
│       ├── project.yaml       # 项目元信息
│       ├── settings/          # 设定文件（模块化目录）
│       │   ├── worldbuilding/
│       │   │   ├── power_system.yaml
│       │   │   ├── factions/_index.yaml + faction_*.yaml
│       │   │   ├── locations/_index.yaml + location_*.yaml
│       │   │   └── lore/*.yaml
│       │   ├── characters/
│       │   │   ├── protagonist/protagonist.yaml
│       │   │   ├── antagonist/_index.yaml + antagonist_*.yaml
│       │   │   ├── supporting/_index.yaml + supporting_*.yaml
│       │   │   └── relationships.yaml
│       │   ├── outline/
│       │   │   ├── premise.yaml
│       │   │   ├── acts/_index.yaml + act_*.yaml
│       │   │   ├── hooks.yaml
│       │   │   └── pacing.yaml
│       │   ├── chapters/
│       │   │   ├── _index.yaml
│       │   │   └── chapter_template.yaml
│       │   └── notes.yaml     # 草稿/笔记
│       ├── content/chapters/  # 章节正文
│       │   └── chapter_*.md
│       ├── drafts/            # 草稿文件夹
│       ├── exports/           # 导出文件
│       └── history/           # AI 生成历史记录
│
├── src/novel/                 # V3 核心引擎及 CLI
│   ├── project.py             # 项目管理
│   ├── stats.py               # 统计查看
│   ├── export.py              # 导出
│   └── utils/
│       └── llm_client.py      # LLM 客户端
│
├── data/schemas/              # YAML Schema 定义
│   ├── project.schema.yaml
│   ├── worldbuilding.schema.yaml
│   ├── characters.schema.yaml
│   ├── outline.schema.yaml
│   └── chapters.schema.yaml
│
└── .claude/skills/            # Claude Code Skills
    ├── generate-outline/SKILL.md
    ├── generate-character/SKILL.md
    ├── generate-chapter/SKILL.md
    ├── write-chapter/SKILL.md
    ├── show-project/SKILL.md
    └── export-novel/SKILL.md
```

## 技能说明

| 技能 | 触发时机 | 功能 |
|------|----------|------|
| `generate-outline` | "生成大纲"、"规划情节"、"帮我写大纲" | 交互式生成小说大纲 |
| `generate-character` | "设计人物"、"创建主角"、"帮我设计角色" | 交互式生成人物设定 |
| `generate-chapter` | "规划章节"、"转化章节"、"把大纲变成章节" | 将大纲转化为章节计划 |
| `write-chapter` | "写第X章"、"生成正文"、"帮我写这一章" | 交互式写作章节正文 |
| `show-project` | "查看项目"、"项目进度"、"显示统计" | 展示项目详情和进度 |
| `export-novel` | "导出小说"、"导出TXT"、"生成文件" | 导出为各种格式 |

## 草稿系统

### 草稿来源

| 来源 | 使用方式 |
|------|----------|
| `settings/notes.yaml` | 项目内的草稿区，Skill 自动读取 |
| 直接提供内容 | `--from-draft "废柴逆袭故事..."` |
| 外部文件 | `--from-draft path/to/file.txt` |

### notes.yaml 示例

```yaml
# 写作笔记/草稿
idea: |
  废柴逆袭故事
  主角资质差但意志坚定
  预计50章

outline_draft: |
  第1幕：困境与转机（1-15章）
  主角入门受挫，获得秘籍
  
character_draft: |
  主角：李青云，废柴逆袭型
  反派：陈长老，觊觎秘籍
```

## CLI 命令速查

### 项目管理

```bash
novel new "书名" --genre 类型 --author 作者 --template default
novel list
novel show <project_id>
novel delete <project_id>
```

### 设定生成（通过 Skills）

```bash
# 使用 Skills 交互式生成（推荐）
# /create-novel — Pipeline 流程入口
# /generate-outline — 生成大纲
# /generate-character — 生成人物
# /generate-chapter — 章节规划
# /write-chapter — 写作正文
novel generate world <project_id> [--prompt "描述"]

# 大纲
novel generate outline <project_id> [--chapters 50] [--from-draft 草稿]

# 人物
novel generate character <project_id> [--from-draft 草稿]

# 章节规划
novel generate chapter <project_id>
```

### 章节写作

```bash
# 生成新章节
novel write new <project_id> <章节号> [--prompt "方向"]

# 续写
novel write continue <project_id> <章节号> [--length 1000]

# 改写（polish/expand/condense/rewrite）
novel write revise <project_id> <章节号> [--mode polish]
```

### 统计与导出

```bash
novel stats <project_id> [--detail]
novel export <project_id> [--format txt|md|epub]
```

## 状态流转

### 项目状态

```
planning → drafting → revising → completed
```

### 章节状态

```
planned（已规划）→ draft（草稿）→ written（已完成）→ revised（已润色）
```

| 状态 | 说明 |
|------|------|
| planned | 有摘要，无正文 |
| draft | 有正文（< 1500 字）|
| written | 正文完成（≥ 1500 字）|
| revised | 已润色修改 |

## 文档导航

- **[数据 Schema](data/schemas/)**：YAML 文件字段定义
- **[Skills 定义](.claude/skills/)**：交互式生成技能说明书