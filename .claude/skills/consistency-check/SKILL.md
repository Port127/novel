---
name: consistency-check
description: 全面一致性检查
when_to_use: 用户想确保小说设定没有矛盾
---

# 任务

全面检查项目一致性。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`

## 执行步骤

### 1. 分阶段收集数据

按 [上下文预算协议](_protocols/context-budget.md) 的"分阶段加载"策略执行，避免一次性读取全部文件导致上下文过载。

**第一轮：索引文件（必读）**
- `{current_path}/.novel/state.yaml`（仅取非推导字段）
- `{current_path}/characters/character_index.yaml`
- `{current_path}/characters/relations.yaml`
- `{current_path}/chapters/index.yaml`
- `{current_path}/plot/outline.yaml`（伏笔和结构）
- `{current_path}/worldbuilding/worldbuilding.yaml`（索引）
- `{current_path}/compliance/inspiration_log.yaml`
- `{current_path}/compliance/risk_report.yaml`
- `{current_path}/quality/ai_trace_report.yaml`

从索引即可完成的检查：文件-索引一致性、状态合法性、钩子统计、借鉴覆盖率

**第二轮：按需深入（仅对可疑项）**
- `{current_path}/characters/*.yaml` — 仅读第一轮中发现可能有问题的角色
- `{current_path}/worldbuilding/entries/*.yaml` — 仅读有效期异常或被引用的条目
- `{current_path}/characters/relation_events.yaml` — 仅在关系检查需要时读取
- `{current_path}/timeline/main.yaml` — 仅在时间线检查需要时读取

**第三轮：语义比对（按需）**
- `{current_path}/plot/outline.md` — 大纲偏离度检测时读取
- `{current_path}/chapters/index.yaml` 的 summary 字段 — 不读章节全文，用 summary 做语义比对
- `{current_path}/worldbuilding/setting.md` — 仅在设定一致性需要叙述版对照时读取
- `{current_path}/ingestion_brief.md` — 仅在素材追溯需要时读取

### 2. 交叉检查

检查维度：

| 类别 | 检查项 |
|------|--------|
| 角色一致性 | 基本信息、关系、年龄与时间线 |
| 时间线一致性 | 顺序、位置、因果关系 |
| 设定一致性 | 世界规则、势力、地点；已过期/被取代设定是否仍在已写章节中使用 |
| 剧情一致性 | 章节匹配、伏笔遗漏 |
| 钩子健康度 | 各级别钩子的埋设/回收/逾期/放弃统计；逾期未处理的 major 钩子标记为错误项 |
| 章节流一致性 | 章节状态推进、字数与目标、POV缺失 |
| 关系演进一致性 | 关系强度跳变、缺桥接事件、关系类型冲突 |
| 借鉴合规一致性 | 借鉴登记是否覆盖、风险章节是否有修复动作 |
| 文风质量一致性 | AI痕迹风险趋势、角色对白区分度 |
| 大纲偏离度 | 已写章节 summary 与 outline 计划的语义比对 |

**钩子健康度检测细则：**

读取 `outline.yaml` 的 `foreshadowing` 列表，统计：

| 指标 | 计算方式 |
|---|---|
| 埋设总数 | status 为 planted + pending + recovered + abandoned 的总数 |
| 回收率 | recovered / (planted + pending + recovered) |
| 逾期数 | planted 且已过 recovery_deadline 的数量 |
| 放弃数 | abandoned 的数量 |

按 level 分级报告：
- `major` 钩子逾期未处理 → **错误项**（读者很可能记得，必须处理）
- `minor` 钩子逾期未处理 → **警告项**（建议尽快处理）
- `micro` 钩子逾期 → 仅计入统计，不标记为问题
- `major` 钩子被放弃 → **警告项**（需确认是否在正文中自然消解）

**设定有效期检测细则：**

扫描 `worldbuilding/entries/*.yaml`，对每条设定检查：
- `superseded_by` 非空但该条目仍被已写章节引用 → 检查引用章节是否在 `valid_until` 之前（正常）还是之后（**警告**）
- `valid_until` 已触发（对应章节已写完或事件已发生），但无后继条目（`superseded_by` 为空）→ **警告**：过期设定没有新版本
- `expiry_trigger` 中的事件已在时间线中发生，但设定 status 仍为 `confirmed` → **提醒**：可能需要演化

**大纲偏离度检测细则：**

遵循 [草稿优先原则](_protocols/draft-primacy.md)：**草稿是真相来源，大纲是辅助材料。** 检测到偏离时，默认方向是大纲需要更新以匹配草稿，而非草稿需要修复。

对每个已有 `summary` 的章节，将其 summary 与 `outline.md` 中对应章节的计划做语义比对：
- **角色偏离**：大纲计划出场的角色未出场，或大纲未提及的角色成为主视角
- **事件偏离**：大纲计划发生的核心事件未发生，或发生了大纲未计划的重大事件
- **目标偏离**：章节实际推进方向与大纲设定的章节目标不一致
- **伏笔偏离**：大纲计划在本章埋设/回收的伏笔未执行

对每章输出偏离等级：`吻合` / `轻微偏离`（1项次要偏差） / `显著偏离`（核心事件不一致） / `严重偏离`（多项核心偏差）

输出汇总偏离率：`显著+严重` 占已写章节比例。超过 30% 时提醒用户主动触发大纲同步，**不自动修改大纲**。

### 3. 生成报告

## 输出格式

```
🔍 一致性检查报告

---

## ✅ 通过项（{{count}}）
- {{通过项1}}
- {{通过项2}}

## ⚠️ 警告项（{{count}}）

### 角色：{{name}}
- {{问题描述}}
  {{详情}}
  建议：{{修复方法}}

## ❌ 错误项（{{count}}）

### 角色：{{name}}
- {{问题描述}}
  {{详情}}
  建议：{{修复方法}}

---

📊 统计：通过 {{pass}} / 警告 {{warn}} / 错误 {{error}}

🔧 修复优先级
   1. [高] {{修复建议}}
   2. [中] {{修复建议}}
   3. [低] {{修复建议}}

💡 修复命令：
   /character-edit {{name}} {{修改}}
   /timeline-add {{修正}}
   /chapter-update {{chapter_id}} --status {{status}}
   /relationship-log {{角色1}} {{角色2}} {{变化}} --chapter {{chapter}}
   /inspiration-log {{chapter_id}} {{material_id}} {{借鉴说明}}
   /anti-ai-rewrite {{chapter_id}} --level 2
   /hook-resolve {{hook_id}} --recover {{chapter}} | --abandon | --extend
   /hook-add {{name}} --chapter {{chapter}} --level {{level}}
```

## 注意事项

- 分级显示问题
- 给出具体修复建议
- 建议定期运行
- 对同一问题链路尽量给出“先修什么再修什么”
- **本 skill 只输出报告，不修改任何文件。** 所有修复动作须由用户主动触发对应命令（见 ）
- 大纲偏离不代表草稿有问题——草稿优先，偏离通常意味着大纲需要跟上草稿，由用户决策