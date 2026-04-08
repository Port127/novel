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

## 输入参数

- `$0` (chapter_id): 章节ID
- `--status`: `idea|outline|draft|revise|final|published`
- `--title`: 章节标题
- `--pov`: 视角角色
- `--word-target`: 目标字数
- `--word-actual`: 实际字数
- `--goal`: 章节目标

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
