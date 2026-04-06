---
name: pipeline-draft-polish
description: 对章节草稿执行结构审查、人物声音检查与去 AI 感处理，产出可进入修订阶段的章节。用于用户写完草稿后，想集中完成一轮高收益打磨时。
when_to_use: 用户完成章节草稿，想把它推进到 revise 阶段
argument-hint: "[章节ID]"
arguments: chapter_id
---

# 任务

把章节从 `draft` 推进到 `可修订草稿`。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/chapters/$0.md`
3. 读取 `{current_path}/chapters/index.yaml`
4. 若能确定 POV 或关键角色，读取对应 `{current_path}/characters/*.yaml` 角色卡（优先对照 `fatal_flaw`、`obsession`、`soft_spot`、`misbelief`、`contrast_habit`）
5. 若本章涉及双人或多人关系戏，读取 `{current_path}/characters/relations.yaml` 与相关 `relation_events.yaml` 片段，核对本章行为是否与快照和近期事件一致

## 输入参数

- `$0` (chapter_id): 章节 ID
- `--rewrite-level`: 可选改写强度，默认 `2`

## 执行步骤

### 1. 做章节审查

按 `/chapter-review` 的维度检查：

- 结构完整性
- 节奏与转折
- 角色行为是否成立
- 伏笔是否有效

### 2. 做人物声音检查

按 `/voice-check` 的方法检查本章关键角色对白：

- 是否有明显同质化
- 是否偏离人物设定
- 对白是否体现缺陷、执念或误判，而不只是推进剧情的功能句

### 3. 做去 AI 感检查与定向改写

按 `/anti-ai-check` 识别高风险片段。

若风险明显：

- 按 `/anti-ai-rewrite` 的方式给出可替换段落
- 默认做针对高风险片段的 `level 2` 处理
- 不默认重写整章

### 4. 推进章节状态

若本章已具备完整草稿，按 `/chapter-update` 将状态推进到 `revise`。

## 输出格式

```markdown
## CurrentState
- 阶段：可修订草稿
- 章节：{{chapter_id}}
- 已完成结构审查、对白检查、去 AI 感处理

## Risks
- {{risk_1}}
- {{risk_2}}

## NextTasks
1. 先修最高收益的 1-2 个结构问题
2. 替换高风险的 AI 痕迹片段
3. 回看结尾钩子与本章目标是否一致

## RecommendedCommands
- /chapter-update {{chapter_id}} --status revise
- /character-edit {{name}} 补充或修正缺陷/执念/误判
- /relationship-log {{a}} {{b}} {{change}} --chapter {{chapter_id}}
- /anti-ai-check {{chapter_id}}
- /consistency-check
```

## 注意事项

- 以“高收益修订”优先，不做整章大换血
- 若本章尚未形成完整草稿，不应强推到 `revise`
- 若用户要求整章重写，再转向更重的改写流程
