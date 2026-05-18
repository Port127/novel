---
name: generate-chapter
description: 此技能仅在用户明确调用"/generate-chapter"或直接提及技能名称时使用。
---

# 规划章节结构

交互式规划章节结构。

## 前提条件

大纲已生成（`settings/outline.yaml` 非空）。未生成则引导使用 generate-outline。

## 工作流程

### 1. 检查大纲

展示大纲结构，确认转化。

### 2. 确认参数

章节数、每章字数（短章 1500-2000 / 标准 2000-3000 / 长章 3000-5000）。

### 3. 生成章节计划

**Agent 直接生成**（不调用脚本）：

1. 基于大纲的节拍，转化为章节摘要
2. 每章包含：number、title、summary、tension、status
3. 生成 `chapters/_index.yaml`

**生成方式**：
- Agent 使用 Write/Edit 工具直接写入 YAML 文件
- 不调用任何脚本，Agent 已连接 LLM

**转化规则**：
- 每个节拍对应一个章节
- 摘要来自节拍的 description
- 张力值来自节拍的 tension

### 4. 展示与调整

展示前 5-10 章预览和张力曲线。询问是否合并/拆分/调整。

## 章节状态

| 状态 | 含义 |
|------|------|
| planned | 已规划，有摘要，无正文 |
| draft | 有正文草稿 |
| written | 正文完成 |
| revised | 已润色 |

## 参考

- Schema: `data/schemas/chapters.schema.yaml`
- 注意：遵循大纲节拍，检查张力曲线合理性