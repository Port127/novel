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
6. 按 [预检完整性协议](_protocols/preflight-integrity.md) 检查目标章节引用链完整性（含前序章节 summary 和角色状态）

## 输入参数

- `$0` (chapter_id): 章节 ID
- `--rewrite-level`: 可选改写强度，默认 `2`

## 执行步骤

### 1. 做章节审查

调用 `/chapter-review`，将审查结果（结构完整性、节奏与转折、角色行为、伏笔有效性）用于后续修订。

### 2. 做人物声音检查

调用 `/voice-check`，检查本章关键角色对白的区分度和人设一致性。

### 3. 检查设定依赖状态

检查本章涉及的世界观设定是否可靠：

- 从章节正文和大纲节点中识别引用了哪些设定条目
- 若引用的设定仍为 `tentative`，标记为风险：
  ```
  ⚠️ 本章依赖尚未确认的设定：
     - {{setting_name}}（tentative）— 建议先 /setting-edit {{id}} --status confirmed
  ```
- 若引用的设定已 `deprecated`，标记为错误

### 4. 做去 AI 感检查与定向改写

调用 `/anti-ai-check`，识别高风险片段。

若风险明显：

- 调用 `/anti-ai-rewrite`，对高风险片段给出可替换段落
- 默认做针对高风险片段的 `level 2` 处理
- 不默认重写整章

### 5. 风格漂移检测

按 [风格生命周期协议](_protocols/style-lifecycle.md) 阶段三执行。

若 `meta.yaml` 的 `style.extracted_at_chapter` 非空，且当前章节号 - `extracted_at_chapter` ≥ 10：

```
💡 你的风格模板是在 {extracted_at_chapter} 时提炼的，已过去 {N} 章。
   写作风格可能已经演化。要更新风格模板吗？(Y/N/永不)
```

无风格模板或间隔不足时跳过此步。

### 6. 草稿冲突检测

遵循 [草稿优先原则](_protocols/draft-primacy.md)，对本章草稿与结构化材料做比对：

**检测范围：**

| 材料 | 检测内容 |
|---|---|
| `plot/outline.md` | 草稿实际发生的事件/角色/目标是否与大纲节点一致 |
| `characters/*.yaml` | 草稿中角色行为、台词风格、能力使用是否与档案矛盾 |
| `worldbuilding/entries/*.yaml` | 草稿引用的设定规则是否与条目定义一致 |
| `timeline/main.yaml` | 草稿的时间线位置是否与时间轴吻合 |
| `characters/relations.yaml` | 草稿中关系互动是否与当前关系状态一致 |

**冲突处理规则：**

- 发现冲突 → 按 [冲突报告模板](_protocols/draft-primacy.md) 输出，列出每条冲突的草稿原文、材料原文、冲突类型、严重度
- **不自动更新任何材料**，等待用户显式触发更新命令
- 若无冲突 → 输出"✅ 草稿与结构化材料一致，无冲突"

### 7. 推进章节状态

若本章已具备完整草稿，调用 `/chapter-update`，将状态推进到 `revise`。

## 输出格式

```markdown
## CurrentState
- 阶段：可修订草稿
- 章节：{{chapter_id}}
- 已完成结构审查、对白检查、设定依赖检查、去 AI 感处理

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
- /setting-edit {{id}} --status confirmed
- /consistency-check
```

## 注意事项

- 以“高收益修订”优先，不做整章大换血
- 若本章尚未形成完整草稿，不应强推到 `revise`
- 若用户要求整章重写，再转向更重的改写流程
- **草稿优先**：冲突检测（步骤 5）只输出报告，不自动修改大纲、人物卡、设定或时间线；所有材料更新须由用户主动触发（见 `_protocols/draft-primacy.md`）
