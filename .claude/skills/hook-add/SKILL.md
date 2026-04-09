---
name: hook-add
description: 登记伏笔/钩子到 outline.yaml 并同步章节文件，支持分级、回收截止和关联链。
when_to_use: 用户在写作中埋设了一个伏笔或悬念，想正式登记以便追踪回收
argument-hint: "[名称] --chapter [埋设章节] --level [major/minor/micro]"
arguments: name
---

# 任务

在 `plot/outline.yaml` 的 `foreshadowing` 列表中登记一条钩子，并同步到章节文件。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/plot/outline.yaml`
3. 读取 `{current_path}/chapters/index.yaml`

## 输入参数

- `$0` (name): 钩子名称（必需），如"赵宋手背的疤痕"
- `--chapter`: 埋设章节 ID，如 `ch003`（必需）
- `--level`: `major` / `minor` / `micro`（默认 `minor`）
- `--deadline`: 回收截止，格式灵活：
  - `ch015` → 章节截止
  - `灰域崩塌后` → 事件截止
  - `30万字前` → 字数截止
  - 不填则无硬性截止
- `--hard`: 标记截止为硬截止（必须回收），默认 false
- `--condition`: 回收前提条件，如"主角到达凝华阶段"
- `--link`: 关联的其他钩子 ID，如 `f003`（可多次指定）
- `--description`: 埋设方式描述
- `--payoff-hint`: 预计回收方式提示（可选，帮助后续规划）
- `--confidence`: `high` / `medium` / `low`（默认 `medium`）

## 执行步骤

### 1. 生成钩子 ID

扫描 `outline.yaml` 的 `foreshadowing` 列表，取最大 ID 序号 +1。格式：`f{三位序号}`，如 `f001`、`f012`。

### 2. 解析截止条件

根据 `--deadline` 格式自动推断 `recovery_deadline.type`：

| 用户输入格式 | type | value |
|---|---|---|
| `ch015`、`第15章` | `chapter` | `15` |
| `灰域崩塌后`、`某事件` | `event` | 原文 |
| `30万字前`、`300000` | `word_count` | `300000` |

### 3. 写入 outline.yaml

在 `foreshadowing` 列表末尾追加：

```yaml
- id: f{序号}
  name: "{$0}"
  level: {level}
  status: planted
  plant_chapter: {chapter}
  plant_scene: ""
  plant_description: "{description}"
  payoff_chapter: TBD
  payoff_description: ""
  recovery_deadline:
    type: {type}
    value: {value}
    hard: {hard}
  recovery_conditions: "{condition}"
  linked_hooks: [{link_ids}]
  confidence: {confidence}
```

### 4. 同步章节文件

更新 `{current_path}/chapters/{chapter_id}.md` 的 `## 伏笔` 区，追加：

```markdown
- [f{序号}] {name}（{level}）—— {description}
```

### 5. 同步章节索引

在 `chapters/index.yaml` 对应章节的 `hooks_planted` 列表中追加钩子 ID。

### 6. 更新项目状态

更新 `{current_path}/.novel/state.yaml` 的 `project.updated`。

## 输出格式

```
✅ 钩子已登记

🪝 {{id}}：{{name}}
📊 等级：{{level}}
📖 埋设：{{chapter_id}}
⏰ 截止：{{deadline 描述，无则显示"无截止"}}
🔗 关联：{{linked_hooks，无则显示"无"}}

📄 已更新：
   - plot/outline.yaml
   - chapters/{{chapter_id}}.md
   - chapters/index.yaml

下一步：
   /hook-add [名称] --chapter [章节]    继续登记
   /hook-query --status planted         查看所有已埋钩子
   /hook-resolve {{id}} --recover [章节] 回收此钩子
```

## 注意事项

- 一次只登记一条钩子
- `linked_hooks` 中的 ID 必须已存在于 `foreshadowing` 列表
- 同一章节可以埋设多个钩子
- 如果 `--chapter` 指定的章节不存在于 `chapters/index.yaml`，提示先创建章节
- `major` 级别钩子建议填写 `--deadline`，不填时输出提醒
