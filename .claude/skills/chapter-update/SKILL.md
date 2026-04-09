---
name: chapter-update
description: 更新章节元数据与状态
when_to_use: 用户要推进章节状态、补充视角、字数、标题等信息
argument-hint: "[章节ID] --status [状态]"
arguments: chapter_id
---

# 任务

更新章节索引中的元数据。当状态推进到 `draft` 或 `final` 时，自动生成章节摘要并更新出场角色的当前状态快照。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 按 [章节自动推断协议](_protocols/chapter-auto-inference.md) 确定目标章节
3. 校验 `{current_path}/chapters/index.yaml` 存在
4. 校验 `$0` 指定章节存在
5. 按 [预检完整性协议](_protocols/preflight-integrity.md) 检查目标章节引用链完整性

## 输入参数

- `$0` (chapter_id): 章节ID
- `--status`: `idea|outline|draft|revise|final|published`
- `--title`: 章节标题
- `--pov`: 视角角色
- `--word-target`: 目标字数
- `--word-actual`: 实际字数
- `--goal`: 章节目标
- `--promote [版本标识]`: 将指定备选版本提升为主稿（见步骤 3b）

## 执行步骤

### 1. 定位章节条目

从 `{current_path}/chapters/index.yaml` 中找到 `id=$0` 的条目。

### 2. 状态守卫

如果章节当前状态为 `published`：

```
⚠️ 章节 $0 已发布

已发布章节修改需谨慎。允许的操作：
  - 修改元数据（标题、字数统计等）：直接执行
  - 回退状态（如 published → revise）：需要确认

确认修改？(Y/N)
```

状态推进建议顺序：`idea → outline → draft → revise → final → published`。
允许回退，但从 `published` 回退需要用户确认。

### 3. 更新字段

按用户传入参数更新对应字段，并刷新 `updated` 日期。

### 3b. 版本提升（--promote）

当指定 `--promote v{N}` 时：

1. **验证版本存在**：检查 `index.yaml` 的 `versions` 列表中是否存在该 tag，且对应文件存在
2. **确认操作**：
   ```
   ⚠️ 即将提升版本

   当前主稿：{{active_version}}（{{当前主稿文件名}}）
   目标版本：v{N}（{{目标文件名}}）

   操作：
   - 当前主稿 {chapter_id}.md → 重命名为 {chapter_id}_v{old}.md
   - 目标版本 {chapter_id}_v{N}.md → 重命名为 {chapter_id}.md

   确认？(Y/N)
   ```
3. **执行交换**：
   - 将当前主稿文件重命名为 `{chapter_id}_v{old_tag}.md`
   - 将目标版本文件重命名为 `{chapter_id}.md`
   - 更新 `versions` 列表中两个条目的 `file` 字段
   - 更新 `active_version` 为 v{N}
   - 更新章节的 `word_actual` 为新主稿的字数

### 4. 同步正文头部（可选）

如果 `{current_path}/chapters/$0.md` 存在，同步更新头部元数据。

### 5. 章节摘要与角色状态更新

**当状态推进到 `draft` 或 `final` 时**，执行以下额外步骤：

#### 5a. 生成章节摘要

读取 `{current_path}/chapters/$0.md` 正文，生成 2-3 句摘要，写入 `index.yaml` 该章节的 `summary` 字段。

摘要要求：
- 聚焦"发生了什么"而非"感受如何"
- 包含关键事件、决定和转折
- 标注本章揭示了什么信息给读者
- 不超过 100 字

同时从正文中识别本章出场角色，写入 `characters_involved` 字段。

#### 5b. 更新出场角色的状态快照

对每个出场的主要角色（protagonist / supporting / antagonist），读取其角色卡，更新 `current_state` 块：

| 字段 | 更新内容 |
|------|---------|
| `as_of_chapter` | 当前章节 ID |
| `location` | 本章结尾时角色所在位置 |
| `emotional_state` | 本章结尾时的情绪/心理状态 |
| `knows` | 追加本章新获知的关键信息 |
| `secrets_from_reader` | 更新角色对读者的信息差 |
| `active_goal` | 本章结尾时的行动目标（可能因本章事件改变） |
| `condition` | 身体/能力状态变化 |
| `pending_tensions` | 更新未解决的悬念/冲突列表 |

更新原则：
- 只更新有变化的字段，没变的保持不动
- `knows` 列表只追加不删除（角色不会遗忘已知信息）
- minor 角色不更新状态快照（信息量不值得维护）
- 如果无法从正文判断某字段的变化，保持原值

### 5c. 写作风格提炼触发（仅在状态推进到 `draft` 时触发）

按 [风格生命周期协议](_protocols/style-lifecycle.md) 阶段二执行。

**触发条件**（全部满足时触发）：

1. `meta.yaml` 的 `style.template` 为空
2. `chapters/index.yaml` 中状态为 `draft` 及以上的章节数 ≥ 3
3. `state.yaml` 中 `style_prompt_declined` 不为 `true`

**触发行为**：主动向用户提议启动风格提炼（不仅仅是末尾一行提示）：

```
📝 你已完成 {N} 章草稿，从实际写作中提炼你的风格模板吗？

这会分析你写出来的内容，提炼真实的句式、节奏和修辞偏好。
后续改写和生成初稿会更贴近你的写法。

(Y 开始提炼 / N 跳过)
```

- Y → 执行 `style-create --from-chapters` 完整流程；成功后更新 `meta.yaml` 的 `style.extracted_at_chapter`
- N → 记录 `state.yaml` 的 `style_prompt_declined: true`，不再触发

### 6. 更新项目状态

更新 `{current_path}/.novel/state.yaml`：
- `project.updated`：今天日期

## 输出格式

**标准更新：**
```
章节信息已更新

章节ID：$0
状态：{{status}}
视角：{{pov}}
字数：{{word_actual}} / {{word_target}}
```

**推进到 draft/final 时（含摘要）：**
```
章节信息已更新

章节ID：$0
状态：{{old_status}} → {{new_status}}
视角：{{pov}}
字数：{{word_actual}} / {{word_target}}

前情摘要已生成：
  "{{summary}}"

角色状态已更新：
  {{角色1}}：{{关键变化}}
  {{角色2}}：{{关键变化}}
```

## 注意事项

- 状态只能在定义集合内
- 建议状态按流程推进，避免跳过 `draft`
- 摘要生成在推进到 `draft` 时首次写入，推进到 `final` 时可覆盖更新（因为正文可能改过）
- 角色状态快照是"到本章结尾时"的状态，不是过程中的状态
- 如果正文为空或不足以判断，摘要和角色状态更新会跳过并提示
