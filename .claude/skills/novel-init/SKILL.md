---
name: novel-init
description: 创建新的小说项目
when_to_use: 用户想要开始写一本新小说时使用
argument-hint: "[书名] [类型]"
arguments: name genre
---

# 任务

创建一个新的小说写作项目。

## 前置检查

1. 检查 `$0` (name) 是否提供
2. 如果未提供，询问用户书名和类型

## 输入参数

- `$0` (name): 书名（必需）
- `$1` (genre): 类型/流派，如仙侠、都市、悬疑等（可选，默认"未分类"）

## 执行步骤

### 1. 检查项目是否已存在

读取 `.projects.yaml`，检查是否已有同名项目。

如果存在：
- 询问用户是否切换到现有项目，或使用新名称

### 2. 创建项目目录

从 `templates/project/` 复制结构到 `projects/$0/`：

```
projects/$0/
├── .novel/
│   ├── meta.yaml              ← 项目元信息
│   ├── state.yaml             ← 运行状态（AI维护）
│   ├── materials.yaml         ← 素材引用
│   └── rules/                 ← 项目专属 Cursor Rules 源文件
│       ├── context.md         ← 项目上下文（→ .cursor/rules/novel-project-context.mdc）
│       └── constraints.md     ← 世界观护栏（→ .cursor/rules/novel-core-constraints.mdc）
├── ingestion_brief.md         ← 素材消化摘要（由 /draft-ingest 生成）
├── characters/
│   ├── character_index.yaml   ← 人物索引（自动聚合）
│   ├── relations.yaml         ← 关系快照
│   └── relation_events.yaml   ← 关系演进事件
├── plot/
│   ├── outline.md             ← 叙述性大纲
│   ├── outline.yaml           ← 结构化大纲（含伏笔/节奏）
│   └── plot_index.yaml        ← 情节索引（自动聚合）
├── scenes/                    ← 场景档案目录
├── timeline/
│   └── main.yaml
├── compliance/
│   ├── inspiration_log.yaml
│   └── risk_report.yaml
├── quality/
│   └── ai_trace_report.yaml
├── worldbuilding/
│   ├── setting.md             ← 叙述性世界观
│   ├── worldbuilding.yaml     ← 世界观索引（指向 entries/）
│   └── entries/               ← 设定集条目（由 /setting-add 生成）
│       └── _template.yaml     ← 条目模板
└── chapters/
    ├── index.yaml
    └── (章节文件按需生成)
```

### 3. 初始化状态文件

写入 `projects/$0/.novel/meta.yaml`：

```yaml
project_id: "proj_{{日期8位}}_{{random4}}"
type: novel
name: $0
genre: $1
sub_genre: []
author: ""
created: {{今天日期}}
updated: {{今天日期}}
status: drafting
writing:
  pov: ""
  target_word_count: 0
  current_word_count: 0
  chapter_count: 0
  update_frequency: ""
external_refs:
  material_lib: ../novel-material
  knowledge_lib: ../novel-knowledge
style:
  template: ""
  prose: []
  strength: []
  notes: ""
```

写入 `projects/$0/.novel/materials.yaml`：

```yaml
# 素材引用
# 素材库已独立为 novel-material 项目
# 路径：../novel-material/data/

external_material_lib: ../novel-material

local_materials: []

referenced_materials: []
# 从 novel-material 引用的素材ID列表
# 素材ID格式：nm_{type}_{YYYYMMDD}_{random4}
```

如果 `../novel-material/data/index.yaml` 存在，自动读取已有素材列表填入 `referenced_materials`。

写入 `projects/$0/.novel/state.yaml`（仅存储不可从源文件推导的状态）：

```yaml
project:
  name: $0
  genre: $1
  created: {{今天日期}}
  updated: {{今天日期}}

protagonist: ""

ingestion:
  status: pending
  brief_file: ""
  source_draft: ""

plot:
  structure: ""

current_focus: ""
```

### 4. 初始化项目 Rules

从 `templates/project/.novel/rules/` 复制 `context.md` 和 `constraints.md` 到 `projects/$0/.novel/rules/`。

将 `context.md` 中的占位符替换为实际值：
- `{{项目名称}}` → `$0`
- `{{类型}}` → `$1`
- `{{当前阶段}}` → `待素材消化`
- `{{一句话概括故事核心}}` → 留空，后续由 `/draft-ingest` 或 `/pipeline-outline-bootstrap` 填充

将两个文件同步到 `.cursor/rules/`（包裹 YAML 前置，同 `/novel-switch` 步骤 3）：
- `context.md` → `.cursor/rules/novel-project-context.mdc`
- `constraints.md` → `.cursor/rules/novel-core-constraints.mdc`

这一步确保新项目创建后，`.cursor/rules/` 立刻指向新书，不会残留上一本书的护栏。

**成功标准**: `projects/$0/.novel/rules/` 下有 `context.md` 和 `constraints.md`，且 `.cursor/rules/` 已同步

### 5. 更新项目列表

更新 `.projects.yaml`：

```yaml
projects:
  - name: $0
    path: projects/$0
    genre: $1
    created: {{今天日期}}
    status: active
```

### 6. 设置为当前项目

更新 `.current.yaml`：

```yaml
current_project: $0
current_path: projects/$0
last_updated: {{今天日期}}
```

**成功标准**: `.current.yaml` 的 `current_project` 等于 `$0`

## 输出格式

```
✅ 项目创建完成

📚 书名：《$0》
🏷️ 类型：$1
📁 位置：projects/$0/

下一步：
   /draft-ingest [草稿路径]                素材消化（有草稿时优先）
   /pipeline-outline-bootstrap [草稿或想法] 从素材到可写大纲
   /character-add [姓名] [定位] [年龄]...  创建角色
   /setting-add [设定名称]                 添加设定条目

当前工作项目已切换为《$0》
```

## 注意事项

- 书名中的特殊字符自动替换为下划线
- 类型可后续修改
- 如需创建示例内容，可加 `--with-examples` 参数