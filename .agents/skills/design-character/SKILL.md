---
name: design-character
description: 人设设计。设计主角、反派、配角，含爽感维度评估。
---

# 人设设计

交互式设计小说人物，含爽感维度（打脸指数、CP感、反派恶心度）。

---

## 前置依赖

- 品类已选择（`settings/scout_report.yaml` 存在）
- 大纲或细纲已有初步方向

如未完成，提示用户先使用 `/scout-topic`。

---

## 工作流程

### 1. 确认项目

运行 `novel list`，选择项目。

### 2. 检查品类

读取 `settings/scout_report.yaml`，确认品类已设置。

如未设置，提示先使用 `/scout-topic`。

### 3. 分层询问（借鉴旧 generate-character 模式）

**主角**：
- 基本信息（名字、年龄、身份）
- 性格特点
- 起点状态 → 终点状态（人物弧线）
- 金手指设计（系统/传承/血脉等）

**反派**：
- 基本信息
- 动机（为什么与主角对立）
- 恶心度设计（越恶心，打脸越爽）

**配角**：
- 名字、角色类型、一句话描述
- 与主角关系

### 4. 爽感评估

基于用户确认的内容，调用引擎评估：

```python
from novel.core.skills.design_character import DesignCharacterSkill
skill = DesignCharacterSkill()
design = await skill.design_character(
    name="主角名",
    genre_id="genre/xuanhuan",  # 从 scout_report.yaml 读取
    background="主角背景",
    personality="性格特点",
    golden_finger="金手指描述",
    villain_name="反派名",
    villain_background="反派背景",
)
```

输出评估结果：

| 维度 | 评分 | 说明 |
|------|------|------|
| 打脸指数 | 9/10 | 废柴开局+隐藏身份，适合扮猪吃虎 |
| CP感 | 7/10 | 腹黑性格有嗑点 |
| 反派恶心度 | 8/10 | 多次羞辱主角，打脸爽感强 |

如评分偏低，给出调整建议。

### 5. 生成人物文件

Agent 直接生成 `settings/characters.yaml`：

- 主角设定
- 反派设定
- 配角设定
- 关系网络

### 6. 展示与调整

展示人物列表、爽感评估、关系网络。询问是否调整。

---

## 输出文件

- `settings/characters.yaml`

## 参考

- Schema: `data/schemas/characters.schema.yaml`
- 引擎: `src/novel/core/skills/design_character.py`
- 旧模式: 旧 generate-character 的分层询问流程
