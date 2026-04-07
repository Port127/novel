---
name: chapter-update
description: 更新章节元数据与状态
when_to_use: 用户要推进章节状态、补充视角、字数、标题等信息
argument-hint: "[章节ID] --status [状态]"
arguments: chapter_id
---

# 任务

更新章节索引中的元数据。

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

### 5. 更新状态

更新 `{current_path}/.novel/state.yaml`：
- `project.updated`：今天日期

## 输出格式

```
✅ 章节信息已更新

🧩 章节ID：$0
📌 状态：{{status}}
👁️ 视角：{{pov}}
📝 字数：{{word_actual}} / {{word_target}}
```

## 注意事项

- 状态只能在定义集合内
- 建议状态按流程推进，避免跳过 `draft`
