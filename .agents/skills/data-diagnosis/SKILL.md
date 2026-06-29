---
name: data-diagnosis
description: 数据诊断。导入平台数据，分析追读率/互动率，定位问题章节。
---

# data-diagnosis（数据诊断）

> **用途**：导入平台后台数据，分析追读率、互动率，定位问题章节并给出改进建议。
> **前置条件**：
> - CSV 数据文件存在（从平台后台导出）
> **输出文件**：`data_diagnosis_report.yaml`

---

## 核心原则

1. **数据驱动**：基于真实数据分析，不凭感觉判断。
2. **异常定位**：快速定位数据异常的章节。
3. **原因分析**：结合剧情内容分析数据异常的原因。
4. **可执行建议**：给出具体的改进建议，而非笼统描述。
5. **趋势分析**：关注数据趋势，不仅看单章。

---

## Phase 定义

### Phase 1：数据导入

**入口条件**：CSV 文件存在
**目标**：解析平台数据

**步骤**：
1. 用户从平台后台导出数据 CSV
2. 读取 CSV 文件
3. 运行 `scripts/analyze-metrics.js` 解析数据
4. 展示数据概览（总章数、时间范围、关键指标）

**出口条件**：数据已解析
**加载 References**：无

---

### Phase 2：指标计算

**入口条件**：数据已解析
**目标**：计算各项关键指标

**步骤**：
1. 读取 `references/metrics-guide.md`，加载指标体系
2. 计算核心指标：
   - 追读率（留存率）
   - 完读率
   - 互动率（评论/点赞/收藏）
   - 打赏率
3. 计算趋势数据（滑动平均、异常点标记）
4. 展示指标概览

**出口条件**：指标已计算
**加载 References**：`metrics-guide.md`

---

### Phase 3：异常定位

**入口条件**：指标已计算
**目标**：定位数据异常章节

**步骤**：
1. 读取 `references/diagnosis-method.md`，加载诊断方法论
2. 检测异常：
   - 追读率骤降（>15% 下降）
   - 完读率偏低（<60%）
   - 互动率偏低（低于均值 50%）
   - 趋势下滑（连续 3+ 章下降）
3. 标记问题章节列表
4. 展示异常概览

**出口条件**：问题章节已定位
**加载 References**：`diagnosis-method.md`

---

### Phase 4：原因分析

**入口条件**：问题章节已定位
**目标**：分析数据异常的原因

**步骤**：
1. 读取 `references/chapter-problem-patterns.md`，加载问题模式库
2. 读取问题章节的摘要和节拍（如有 chapters_index.yaml）
3. 匹配问题模式：
   - 节奏问题（太平淡/太拖沓）
   - 剧情问题（逻辑硬伤/人设崩塌）
   - 钩子问题（无悬念/悬念弱）
   - 品类问题（不符合读者预期）
4. 为每个问题章节生成原因分析

**出口条件**：原因分析已完成
**加载 References**：`chapter-problem-patterns.md`

---

### Phase 5：报告输出

**入口条件**：分析已完成
**目标**：生成诊断报告

**步骤**：
1. 读取 `references/report-template.md`，加载报告模板
2. 按模板生成报告：
   - 总体数据概览
   - 问题章节列表（含原因分析）
   - 改进建议
   - 趋势预测
3. 写入 `data_diagnosis_report.yaml`
4. 展示报告摘要

**出口条件**：报告已生成
**加载 References**：`report-template.md`

---

## 质量门禁

- analyze-metrics.js：验证数据格式正确，指标计算无异常

---

## 输出文件

- `data_diagnosis_report.yaml`

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | — | 数据导入 |
| 2 | metrics-guide.md | 指标体系 |
| 3 | diagnosis-method.md | 诊断方法论 |
| 4 | chapter-problem-patterns.md | 问题模式库 |
| 5 | report-template.md | 报告模板 |

---

## 下一步

诊断报告生成后：
- 根据建议修改问题章节
- `/daily-write`：后续章节注意避免同类问题
