---
name: create-novel
description: Pipeline 流程入口，引导用户按阶段完成创作
---

# Pipeline 流程入口

**核心功能**：组织 Skills 的执行顺序，确保按正确流程创作。

---

## Pipeline 阶段

| 阶段 | 名称 | 前置依赖 | 完善度阈值 | Skills |
|------|------|---------|-----------|--------|
| 1 | 世界观设定 | 无 | 80% | nm + Agent 交互 |
| 2 | 人物设定 | 阶段1完成 | 70% | generate-character |
| 3 | 大纲设定 | 阶段1+2完成 | 85% | generate-outline |
| 4 | 章节规划 | 阶段3完成 | 100% | generate-chapter |
| 5 | 正文写作 | 阶段4完成 | - | write-chapter |

---

## 工作流程

### 1. 检查项目状态

读取 `project.yaml` 的 `pipeline_status`：

```yaml
pipeline_status:
  current_stage: 0                # 当前阶段
  completed_stages: []            # 已完成阶段
```

### 2. 判断当前阶段

| current_stage | 说明 | 下一步 |
|---------------|------|--------|
| 0 | 初始化，无设定 | 开始阶段1 |
| 1 | 世界观进行中 | 继续或完成阶段1 |
| 2 | 人物进行中 | 继续或完成阶段2 |
| 3 | 大纲进行中 | 继续或完成阶段3 |
| 4 | 章节规划进行中 | 继续或完成阶段4 |
| 5 | 写作进行中 | 继续写作 |

### 3. 检查前置依赖

对当前阶段检查前置依赖完善度：

```bash
novel generate (内建检查) {project_id} worldbuilding --modules
novel generate (内建检查) {project_id} characters --modules
novel generate (内建检查) {project_id} outline --modules
```

### 4. 引导执行当前阶段

**阶段1引导**：
```
当前阶段：阶段1 - 世界观设定
前置依赖：无

执行步骤：
  1. 使用 /nm 检索同类题材参考
  2. 与 Agent 讨论确认力量体系、势力、地点
  3. Agent 直接生成 worldbuilding/ 目录各文件
     - power_system.yaml（力量体系）
     - factions/faction_*.yaml（势力档案）
     - locations/location_*.yaml（地点档案）

是否开始世界观设定？
```

**阶段2引导**：
```
当前阶段：阶段2 - 人物设定
前置依赖：
  - 阶段1 完善度 85% ✅

执行步骤：
  1. 使用 /nm 检索同类人物塑造参考
  2. 使用 /generate-character 交互生成人物
  3. Agent 直接生成 characters/ 目录各文件
     - protagonist/protagonist.yaml（主角）
     - antagonist/antagonist_*.yaml（反派）
     - supporting/supporting_*.yaml（配角）
     - relationships.yaml（关系网络）

是否开始人物设定？
```

**阶段3引导**：
```
当前阶段：阶段3 - 大纲设定
前置依赖：
  - 阶段1 完善度 85% ✅
  - 阶段2 完善度 75% ✅

执行步骤：
  1. 使用 /nm 检索同类大纲结构参考
  2. 使用 /generate-outline 交互生成大纲
  3. Agent 直接生成 outline/ 目录各文件
     - premise.yaml（核心设定）
     - acts/act_*.yaml（各幕结构）
     - hooks.yaml（伏笔-回收）
     - pacing.yaml（节奏曲线）

是否开始大纲设定？
```

**跳阶段阻止**：
```
当前阶段：阶段3 - 大纲设定
前置依赖检查：
  - 阶段1 完善度 20% ❌（需 ≥ 80%）
  - 阶段2 完善度 0% ❌（需 ≥ 70%）

阻止原因：前置依赖不满足
引导：请先完成阶段1和阶段2
      是否返回阶段1？
```

### 5. 更新 Pipeline 状态

阶段完成后更新 `project.yaml`：

```yaml
pipeline_status:
  current_stage: 2                # 进入下一阶段
  completed_stages: [1]           # 记录已完成
```

---

## 核心原则

**小说应该"生长和演进"，而非"一次性生成"。**

```
世界观（根基）
    ↓ 生长
人物（在世界观中生根）
    ↓ 生长
大纲（在人物弧线上生长）
    ↓ 生长
章节规划（在大纲中细化）
    ↓ 生长
正文（在所有设定基础上写作）
```

---

## 规模支持

**目标规模**：800章 × 4000字 = 320万字

**模块化设计**：
- 每个势力/人物/地点独立文件
- 每幕独立文件（含序列+节拍）
- 每章独立档案

**分批执行**：
- 阶段4可分批规划（如先规划前100章）
- 阶段5按顺序写作（从第1章开始）

---

## Pipeline 文档

详见 `docs/PIPELINE.md`

---

## 参考

- 完善度标准：`data/schemas/completeness.schema.yaml`
- 模板结构：`templates/default/template.yaml`
- 注意：此 Skill 是推荐入口，引导用户按正确顺序完成创作