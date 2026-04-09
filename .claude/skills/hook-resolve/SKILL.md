---
name: hook-resolve
description: 回收、放弃或延期钩子，更新追踪状态并同步章节索引。
when_to_use: 用户在某章回收了一个伏笔，或决定放弃/延期某个钩子
argument-hint: "[钩子ID] --recover [章节ID] | --abandon [原因] | --extend [新截止]"
arguments: hook_id action
---

# 任务

更新 `plot/outline.yaml` 中指定钩子的状态，并同步到章节索引。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/plot/outline.yaml`
3. 定位目标钩子：按 ID 精确匹配或按名称模糊匹配
4. 若无匹配，列出现有钩子供用户选择

## 输入参数

- `$0` (hook_id): 钩子 ID 或名称（必需）
- 操作（三选一，必需）：
  - `--recover [章节ID]`: 标记在某章回收
  - `--abandon [原因]`: 标记放弃
  - `--extend [新截止]`: 延期截止时间
- `--payoff [描述]`: 回收方式描述（`--recover` 时建议填写）
- `--reason [原因]`: 延期或放弃的原因（`--extend` / `--abandon` 时必需）

## 执行步骤

### 1. 验证操作合法性

| 当前 status | 允许的操作 | 需确认 |
|---|---|---|
| `planted` / `pending` | recover / abandon / extend | 否 |
| `recovered` | abandon（撤销回收） | **是** |
| `abandoned` | recover（重新激活） | **是** |

### 2. 执行回收（--recover）

更新 `outline.yaml` 中该钩子：
- `status` → `recovered`
- `payoff_chapter` → 用户指定的章节
- `payoff_description` → `--payoff` 描述

同步 `chapters/index.yaml`：在回收章节的 `hooks_revealed` 列表中追加钩子 ID。

同步回收章节文件（`chapters/{chapter_id}.md`）的 `## 伏笔` 区：
```markdown
- [f{序号}] {name}（{level}）—— ✅ 已回收：{payoff_description}
```

### 3. 执行放弃（--abandon）

更新 `outline.yaml`：
- `status` → `abandoned`
- 在该钩子条目末尾追加 `abandon_reason` 和 `abandon_date`

如果是 `major` 级别钩子，输出额外警告：
```
⚠️ 这是一个 major 级别的钩子，读者很可能记得它。
放弃后建议在后续章节中自然消解，避免成为"挖坑不填"的硬伤。
确认放弃？(Y/N)
```

### 4. 执行延期（--extend）

更新 `outline.yaml`：
- 修改 `recovery_deadline.value` 为新截止
- 在 `lifecycle`（若无则新建）追加延期记录：

```yaml
deadline_history:
  - from: ch015
    to: ch020
    reason: "主角还未到达凝华阶段，需要更多铺垫"
    date: {今天}
```

### 5. 处理关联钩子

如果该钩子有 `linked_hooks`，检查关联钩子的状态：
- 回收时：提示"关联钩子 [ID] 是否也需要回收？"
- 放弃时：提示"关联钩子 [ID] 可能受影响，请检查"

### 6. 更新项目状态

更新 `{current_path}/.novel/state.yaml` 的 `project.updated`。

## 输出格式

### 回收

```
✅ 钩子已回收

🪝 {{id}}：{{name}}（{{level}}）
📖 埋设：{{plant_chapter}} → 回收：{{payoff_chapter}}
📝 回收方式：{{payoff_description}}

📄 已更新：
   - plot/outline.yaml
   - chapters/{{payoff_chapter}}.md
   - chapters/index.yaml

{{#if linked_hooks}}
🔗 关联钩子提醒：
   {{linked_hook_status}}
{{/if}}
```

### 放弃

```
🗑️ 钩子已放弃

🪝 {{id}}：{{name}}（{{level}}）
📝 原因：{{reason}}

💡 后续建议：
   在 {{建议章节}} 中自然消解此线索，避免悬空
```

### 延期

```
⏰ 钩子截止已延期

🪝 {{id}}：{{name}}（{{level}}）
📝 截止：{{旧截止}} → {{新截止}}
📝 原因：{{reason}}
```

## 注意事项

- 一次只处理一条钩子
- `major` 钩子放弃需要用户确认
- 延期记录保留历史，方便追溯"这个钩子为什么一直拖"
- 回收时如果 `--payoff` 为空，提示填写（不强制）
- 支持按名称模糊匹配钩子，避免用户必须记 ID
