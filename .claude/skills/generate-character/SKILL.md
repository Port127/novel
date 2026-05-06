---
name: generate-character
description: 此技能仅在用户明确调用"/generate-character"或直接提及技能名称时使用。
---

# 生成小说人物

交互式生成小说人物设定。

## 工作流程

### 1. 确认项目

同 generate-outline 技能。

### 2. 检查草稿来源

用户描述、`settings/notes.yaml` 的 `character_draft`、或指定草稿文件。

### 3. 分层次询问

**主角**：基本信息 → 性格特点 → 心理维度（fatal_flaw/obsession/soft_spot/misbelief）→ 人物弧线

**反派**：基本信息 → 动机 → 心理维度

**配角**：名字、角色类型、一句话描述、与主角关系

### 4. 生成人物

```bash
python scripts/generate.py character {project_id} --from-draft "{想法}"
```

### 5. 展示与调整

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