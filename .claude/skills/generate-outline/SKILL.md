---
name: generate-outline
description: 此技能仅在用户明确调用"/generate-outline"或直接提及技能名称时使用。
---

# 生成小说大纲

交互式生成小说大纲设定。

## 工作流程

### 1. 确认项目

运行 `python scripts/project.py list` 查看项目列表。如果用户未指定项目，询问选择。

### 2. 检查前置完善度（强制）

**前置依赖**：世界观 + 人物设定必须完善。

调用完善度检查：
```bash
python scripts/utils/completeness_check.py {project_id} worldbuilding
python scripts/utils/completeness_check.py {project_id} characters
```

检查结果处理：

| 状态 | 处理 |
|------|------|
| worldbuilding ≥ 80%, characters ≥ 70% | 继续生成大纲 |
| worldbuilding < 80% | 提示缺失字段，引导先完成世界观设定 |
| characters < 70% | 提示缺失字段，引导先完成人物设定 |

完善度标准定义：`data/schemas/completeness.schema.yaml`

### 3. 检查草稿来源

优先使用用户提供的素材：用户描述、`settings/notes.yaml` 的 `outline_draft`、或指定草稿文件。

### 4. 交互式询问

按以下顺序逐步确认：

**核心设定**：一句话概括故事核心
**主角设定**：名字、特点、起点、终点
**冲突设计**：外部冲突、内部冲突、核心障碍
**结构规划**：章数、幕数（建议三幕式）
**确认生成**：汇总后请用户确认

### 5. 生成大纲

**Agent 直接生成**（不调用脚本）：

1. 基于用户确认的内容，直接编写 `settings/outline.yaml`
2. 包含：premise、acts、sequences、beats
3. 每个节拍有：chapter（章节号）、title、description、tension（张力值）

**生成方式**：
- Agent 使用 Write/Edit 工具直接写入 YAML 文件
- 不调用任何脚本，Agent 已连接 LLM

**结构要求**：
- premise：一句话概括故事核心
- acts：至少 3 幕
- sequences：每幕至少 2 序列
- beats：每序列至少 5 节拍

### 6. 展示与调整

展示大纲结构和转折点，询问是否需要调整。

可选：生成钩子（伏笔→回收）和节奏曲线。

## 参考

- Schema: `data/schemas/outline.schema.yaml`
- 注意：尊重已有世界观/人物设定，逐步细化让用户确认