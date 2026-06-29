---
name: paywall-design
description: 付费卡点设计。分析大纲找最优切割点，设计过渡章节奏。
---

# paywall-design（付费卡点设计）

> **用途**：分析大纲和张力曲线，找到最优付费切割点，设计过渡章节奏。
> **前置条件**：
> - `settings/outline.yaml` 存在（大纲已完成）
> - `settings/chapters_index.yaml` 存在（细纲已完成）
> - 黄金三章已完成（可选但推荐）
> **输出文件**：`paywall_report.yaml`

---

## 核心原则

1. **爽点兑现**：付费切割点必须在爽点兑现之后，不在低谷期切。
2. **双重保险**：免费末章必须做到"爽点兑现 + 致命悬念"。
3. **即时反馈**：付费首章 200 字内必须给出爽感反馈。
4. **平台适配**：不同平台的付费模式影响切割策略。
5. **读者心理**：利用损失厌恶和沉没成本设计付费动机。

---

## Phase 定义

### Phase 1：大纲分析

**入口条件**：outline.yaml + chapters_index.yaml 存在
**目标**：分析张力曲线，标记候选切点

**步骤**：
1. 读取 `outline.yaml` 和 `chapters_index.yaml`
2. 提取张力曲线数据
3. 读取 `references/cut-point-method.md`，加载切点选择方法论
4. 标记候选切点（张力 ≥ 4 的章节后）
5. 排除不适合的切点（主角低谷期、无悬念章节）
6. 展示候选切点列表

**出口条件**：候选切点列表已生成
**加载 References**：`cut-point-method.md`

---

### Phase 2：切点决策

**入口条件**：候选切点列表已生成
**目标**：评估候选切点，确定最优切点

**步骤**：
1. 读取 `references/paywall-psychology.md`，加载付费心理分析
2. 按评估维度打分每个候选切点：
   - 爽点兑现度（前章是否有爽点）
   - 悬念强度（切割后的悬念是否足够）
   - 读者情感（切割时读者的情感状态）
   - 平台适配（是否符合目标平台模式）
3. 推荐最优切点，展示评估理由
4. 用户确认或调整

**出口条件**：最优切点已确定
**加载 References**：`paywall-psychology.md`

---

### Phase 3：过渡设计

**入口条件**：切点已确定
**目标**：设计免费末章和付费首章的节奏

**步骤**：
1. 读取 `references/transition-guide.md`，加载过渡章设计指南
2. 设计免费末章：
   - 爽点兑现（让读者满足）
   - 致命悬念（让读者不花钱就难受）
3. 设计付费首章：
   - 200 字内爽感反馈
   - 展开新弧线/新悬念
4. 展示过渡章设计方案

**出口条件**：过渡章设计方案已确认
**加载 References**：`transition-guide.md`

---

### Phase 4：平台适配

**入口条件**：过渡章设计已确认
**目标**：根据目标平台调整付费策略

**步骤**：
1. 读取 `references/platform-paywall.md`，加载各平台付费模式
2. 根据 `scout_report.yaml` 的 `platform` 字段调整策略：
   - 番茄（免费+广告）：不需要付费切割，但需要设计广告插入点
   - 起点（千字付费）：优化切割点，确保读者愿意付费
   - 晋江（VIP付费）：考虑女性读者偏好
3. 生成平台适配方案

**出口条件**：平台适配完成
**加载 References**：`platform-paywall.md`

---

### Phase 5：落盘验证

**入口条件**：所有设计已完成
**目标**：生成 paywall_report.yaml

**步骤**：
1. 汇总所有设计数据
2. 运行 `scripts/check-paywall.js` 验证切点合理性
3. 写入 `paywall_report.yaml`
4. 展示最终报告

**出口条件**：paywall_report.yaml 已生成
**加载 References**：无

---

## 质量门禁

- check-paywall.js：验证切点章张力值 > 全章均值，前后悬念密度达标

---

## 输出文件

- `paywall_report.yaml`

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | cut-point-method.md | 切点选择方法论 |
| 2 | paywall-psychology.md | 付费心理分析 |
| 3 | transition-guide.md | 过渡章设计 |
| 4 | platform-paywall.md | 平台付费模式 |
| 5 | — | 落盘验证 |

---

## 下一步

付费卡点设计完成后：
- `/daily-write`：开始日更写作
- 从切割点开始写作
