---
name: generate-outline
description: 此技能仅在用户明确调用"/generate-outline"或直接提及技能名称时使用。
---

# 生成小说大纲

交互式生成小说大纲设定。

## 工作流程

### 1. 确认项目

运行 `python scripts/project.py list` 查看项目列表。如果用户未指定项目，询问选择。

### 2. 检查草稿来源

优先使用用户提供的素材：用户描述、`settings/notes.yaml` 的 `outline_draft`、或指定草稿文件。

### 3. 交互式询问

按以下顺序逐步确认：

**核心设定**：一句话概括故事核心
**主角设定**：名字、特点、起点、终点
**冲突设计**：外部冲突、内部冲突、核心障碍
**结构规划**：章数、幕数（建议三幕式）
**确认生成**：汇总后请用户确认

### 4. 生成大纲

```bash
python scripts/generate.py outline {project_id} --chapters {章数} --from-draft "{想法}"
```

### 5. 展示与调整

展示大纲结构和转折点，询问是否需要调整。

可选：生成钩子（伏笔→回收）和节奏曲线。

## 参考

- Schema: `data/schemas/outline.schema.yaml`
- 注意：尊重已有世界观/人物设定，逐步细化让用户确认