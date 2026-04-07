---
name: scene-add
description: 创建场景档案，记录场景的空间、氛围、感官细节和叙事功能。用于需要反复出现的重要场景，或为写作提供环境锚点。
when_to_use: 用户想建立可复用的场景档案（如宗门大殿、市场、密室），或在写作前为章节规划具体场景
argument-hint: "[场景名称] [--location 地点] [--category 类别]"
arguments: name
---

# 任务

创建一份结构化场景档案，写入 `scenes/` 目录。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 确认 `{current_path}/scenes/` 目录存在，不存在则创建

## 输入参数

- `$0` (name): 场景名称（必需）
- `--location`: 所属地点（如"青云宗"、"北城废矿"）
- `--category`: 场景类别：
  - `interior`：室内
  - `exterior`：室外
  - `transitional`：过渡空间（走廊、门口、路上）
  - `symbolic`：具有象征意义的场景
- `--mood`: 基调氛围
- `--from`: 从章节或笔记中提取场景描写

## 执行步骤

### 1. 确定场景内容

如果用户提供了详细描述，直接使用。

如果只提供了名称：
- 检查 `worldbuilding/setting.md` 中是否有相关地点描述
- 检查已有章节中是否出现过此场景
- 若都没有，向用户询问核心要素

### 2. 构造场景档案

写入 `{current_path}/scenes/{slug}.yaml`：

```yaml
name: "$0"
slug: "{{name_slug}}"
location: ""
category: ""

spatial:
  layout: ""
  scale: ""
  key_objects: []

sensory:
  visual: ""
  auditory: ""
  olfactory: ""
  tactile: ""
  temperature: ""

atmosphere:
  default_mood: ""
  time_variants:
    - time: "白天"
      mood_shift: ""
    - time: "夜晚"
      mood_shift: ""

narrative:
  function: ""
  associated_characters: []
  associated_events: []
  symbolic_meaning: ""

appearances:
  - chapter: ""
    context: ""

notes: ""
created: "{{今天日期}}"
updated: "{{今天日期}}"
```

### 3. 更新状态

更新 `{current_path}/.novel/state.yaml`：
- `project.updated`：今天日期

## 输出格式

```
✅ 场景档案已创建

🏛️ 场景：$0
📍 地点：{{location}}
🎭 氛围：{{mood}}
📄 文件：scenes/{{slug}}.yaml

下一步：
   /scene-add [另一个场景]          继续创建
   /chapter-draft $chapter_id       写章节时引用此场景
```

## 注意事项

- 场景档案是写作辅助工具，重在提供环境锚点和感官细节
- 不是每个出现的地点都需要场景档案，只为反复出现或具有叙事功能的场景建档
- 感官细节优先写视觉和听觉，其他维度按需补充
- `appearances` 列表在章节引用场景时自动更新
