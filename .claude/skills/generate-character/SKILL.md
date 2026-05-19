---
name: generate-character
description: 此技能仅在用户明确调用"/generate-character"或直接提及技能名称时使用。
---

# 生成小说人物

交互式生成小说人物设定。

## Pipeline 位置

此 Skill 属于 Pipeline 流程的一部分：

| 阶段 | Skill |
|------|-------|
| 1 | nm + Agent 交互 |
| 2 | generate-character ← 本 Skill |
| 3 | generate-outline |
| 4 | generate-chapter |
| 5 | write-chapter |

**推荐入口**：使用 `/create-novel` 自动引导 Pipeline 流程。

---

## 工作流程

### 1. 确认项目

同 generate-outline 技能。

### 2. 检查前置完善度（强制）

**前置依赖**：世界观设定必须完善。

调用完善度检查：
```bash
python scripts/utils/completeness_check.py {project_id} worldbuilding
```

检查结果处理：

| 状态 | 处理 |
|------|------|
| worldbuilding ≥ 80% | 继续生成人物 |
| worldbuilding < 80% | 提示缺失字段，引导先完成世界观设定 |

完善度标准定义：`data/schemas/completeness.schema.yaml`

### 3. 检查草稿来源

用户描述、`settings/notes.yaml` 的 `character_draft`、或指定草稿文件。

### 4. 分层次询问

**主角**：基本信息 → 性格特点 → 心理维度（fatal_flaw/obsession/soft_spot/misbelief）→ 人物弧线

**反派**：基本信息 → 动机 → 心理维度

**配角**：名字、角色类型、一句话描述、与主角关系

### 5. 生成人物

**Agent 直接生成**（不调用脚本）：

1. 基于用户确认的内容，直接编写 `settings/characters/` 目录各文件：
   - `protagonist/protagonist.yaml`（主角）
   - `antagonist/antagonist_*.yaml`（反派）
   - `supporting/supporting_*.yaml`（配角）
   - `relationships.yaml`（关系网络）
2. 包含：人物列表、角色类型、性格特征、人物弧线
3. 主角必须有：name、traits、arc

**生成方式**：
- Agent 使用 Write/Edit 工具直接写入 YAML 文件
- 不调用任何脚本，Agent 已连接 LLM

**结构要求**：
- characters：人物列表（至少主角）
- protagonist：必须有 name、traits（至少2个）、arc
- antagonist：必须有 traits、动机

### 6. 展示与调整

展示人物列表和关系网络，询问是否调整。

## 角色深度规则

| 类型 | 必填 |
|------|------|
| protagonist | traits, psychology, arc |
| antagonist | traits, psychology, 动机 |
| supporting | traits, description |
| minor | description |

## 参考

- Schema: `data/schemas/characters.schema.yaml`
- 注意：配合世界观设定，优先确认主角