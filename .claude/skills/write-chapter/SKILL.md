---
name: write-chapter
description: 此技能仅在用户明确调用"/write-chapter"或直接提及技能名称时使用。
---

# 写作章节正文

交互式写作章节正文。

## 前提条件

章节已规划（`chapters/_index.yaml` 中有摘要）。未规划则引导使用 generate-chapter。

## 工作流程

### 1. 确认章节

展示章节标题、摘要、张力、出场人物。

### 2. 检查草稿

读取 `drafts/chapter_{num}_draft.md` 或询问写作方向（情节推进/人物展示/环境氛围/对话为主）。

### 3. 检查衔接

展示前章结尾片段和下章摘要，确认衔接点。

### 4. 生成正文

```bash
python scripts/write.py new {project_id} {num} --prompt "{方向}"
```

### 5. 展示正文

展示开头 500 字和结尾 300 字，汇总字数、情节覆盖度、出场人物。

### 6. 续写/改写选项

不满意时可选：续写（500/1000字）、改写（润色/扩充/精简/重写）。

## 调用脚本

```bash
python scripts/write.py new {project_id} {num} --prompt "方向"
python scripts/write.py continue {project_id} {num} --length 1000
python scripts/write.py revise {project_id} {num} --mode polish
```

## 参考

- Schema: `data/schemas/chapters.schema.yaml`
- 注意：风格一致性、人物性格匹配、张力匹配（建议 2000-3000 字/章）