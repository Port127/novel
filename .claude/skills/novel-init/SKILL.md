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
│   └── materials.yaml         ← 素材引用
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
│   └── worldbuilding.yaml     ← 结构化世界观
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

写入 `projects/$0/.novel/state.yaml`：

```yaml
project:
  name: $0
  genre: $1
  created: {{今天日期}}
  updated: {{今天日期}}

characters: []
timeline:
  start: ""
  end: ""
  events_count: 0
plot:
  structure: ""
  chapters: 0
current_focus: ""
```

### 4. 更新项目列表

更新 `.projects.yaml`：

```yaml
projects:
  - name: $0
    path: projects/$0
    genre: $1
    created: {{今天日期}}
    status: active
```

### 5. 设置为当前项目

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
   /character-add [姓名] [定位] [年龄]...  创建角色
   /plot-init [结构]                       初始化大纲

素材管理见 ../novel-material/ 项目

当前工作项目已切换为《$0》
```

## 注意事项

- 书名中的特殊字符自动替换为下划线
- 类型可后续修改
- 如需创建示例内容，可加 `--with-examples` 参数