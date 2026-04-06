---
name: pipeline-outline-bootstrap
description: 从一句话故事想法出发，编排大纲初始化、关键节点补全与基础一致性校验，产出可继续写作的初版大纲。用于用户想从零开始搭建大纲，或只有一个粗略 premise 时快速落地。
when_to_use: 用户想创建大纲，且当前项目只有零散想法或空白剧情骨架
argument-hint: "[一句话故事] [--structure 结构]"
arguments: premise
---

# 任务

把一句话 premise 变成“可写大纲”，并输出最小下一步任务。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/plot/outline.md`
3. 若存在，读取 `{current_path}/plot/outline.yaml`
4. 若存在，读取 `{current_path}/worldbuilding/setting.md`
5. 若存在，读取 `{current_path}/timeline/main.yaml`

## 输入参数

- `$0+` (premise): 一句话故事想法
- `--structure`: `三幕式|英雄之旅|五段式|自定义`，默认 `三幕式`

## 执行步骤

### 1. 判断是否适合启动型流程

如果 `plot/outline.md` 已有较完整内容：

- 先概述现状
- 询问用户是否要覆盖
- 若用户更想“补强而不是重建”，引导到 `/pipeline-outline-polish`

### 2. 初始化结构骨架

按 `/plot-init` 的契约生成基础结构，并确保：

- `outline.md` 有可阅读的幕次或节点骨架
- `outline.yaml` 至少包含 premise、structure、foreshadowing、pacing_curve 的初始框架

### 3. 补足关键剧情节点

按 `/plot-suggest` 的方式补出最小可写骨架，至少覆盖：

- 开场处境
- 引发事件
- 中段升级或中点
- 危机或最低谷
- 高潮与结局方向

必要时可将关键节点直接写入 `outline.md`，并同步摘要到 `outline.yaml`。

### 4. 做一次轻量一致性校验

按 `/timeline-check` 的标准检查：

- 世界规则是否与关键事件矛盾
- 时间顺序是否明显冲突
- 是否有依赖世界观但尚未说明的关键设定

### 5. 输出止点与下一步

将本次落点明确为 `可写大纲`，并只保留最小必要任务。

## 输出格式

```markdown
## CurrentState
- 阶段：可写大纲
- premise：{{premise}}
- 结构：{{structure}}
- 已补全开场、引发事件、中段升级、高潮方向

## Risks
- {{risk_1}}
- {{risk_2}}

## NextTasks
1. 细化第一个关键章节或幕次节点
2. 补一条最重要的世界规则或时间线约束
3. 决定第一章的 POV 与章节目标

## RecommendedCommands
- /pipeline-chapter-kickoff ch001 {{goal}}
- /plot-add {{node}} {{content}}
- /timeline-add {{time}} {{event}}
```

## 注意事项

- 这是“启动型”流程，优先让用户尽快进入可写状态
- 不追求一次性把全书细节补满
- 若结构将发生大重排，先给预览再执行
