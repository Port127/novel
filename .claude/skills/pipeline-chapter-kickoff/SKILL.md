---
name: pipeline-chapter-kickoff
description: 从章节想法出发，编排章节创建、状态推进和对应情节点补全，产出可直接开写的新章节。用于用户准备开始一章正文，不想手动拼接 chapter 和 plot 命令时。
when_to_use: 用户准备开写新章节，想同时创建章节卡、推进状态并补上大纲节点
argument-hint: "[章节ID] [一句话目标]"
arguments: chapter_id goal
---

# 任务

把一个章节想法落地为 `可开写章节`。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/chapters/index.yaml`
3. 读取 `{current_path}/plot/outline.md`
4. 若存在，读取 `{current_path}/plot/outline.yaml`

## 输入参数

- `$0` (chapter_id): 章节 ID，如 `ch012`
- `$1+` (goal): 一句话章节目标
- `--pov`: 可选 POV 角色
- `--after`: 可选插入位置，如 `第11章`

## 执行步骤

### 1. 创建章节卡

按 `/chapter-create` 的契约：

- 创建章节正文文件
- 在 `chapters/index.yaml` 中登记条目

### 2. 推进到 outline 阶段

按 `/chapter-update` 的契约：

- 将章节状态设为 `outline`
- 若用户给出 `--pov`，同步写入 POV
- 必要时补标题、目标字数等最小元数据

### 3. 补齐对应情节点

按 `/plot-add` 的契约，把本章写入现有大纲：

- 章节目标
- 事件推进
- 本章冲突
- 章节结尾钩子

如用户给出 `--after`，优先按指定位置插入。

### 4. 输出开写前清单

至少明确：

- 本章要完成的剧情目标
- POV
- 冲突点
- 结尾钩子

## 输出格式

```markdown
## CurrentState
- 阶段：可开写章节
- 章节：{{chapter_id}}
- 目标：{{goal}}
- 状态已推进到 outline

## Risks
- {{risk_1}}
- {{risk_2}}

## NextTasks
1. 补齐本章开场场景与 POV 进入方式
2. 确认中段冲突升级点
3. 写出结尾钩子或悬念句

## RecommendedCommands
- /chapter-review {{chapter_id}}
- /chapter-update {{chapter_id}} --status draft
- /plot-add {{node}} {{content}}
```

## 注意事项

- 这是开工流程，不负责完整写正文
- 若同 ID 章节已存在，先确认是否覆盖
- 大纲节点应服务章节目标，而不是重复摘要正文
