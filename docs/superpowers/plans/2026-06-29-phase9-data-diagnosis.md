# Phase 9 执行计划：data-diagnosis（数据诊断）

> **执行目标**：完整重写 data-diagnosis skill，包含 SKILL.md + 4 references + 1 script

---

## 文件清单

| 文件 | 行数估计 | 职责 |
|------|---------|------|
| `.agents/skills/data-diagnosis/SKILL.md` | ~150 行 | 主流程：5 Phase + 数据导入 + 问题诊断 |
| `.agents/skills/data-diagnosis/references/metrics-guide.md` | ~150 行 | 指标体系（读完率/互动率/追读率/打赏率） |
| `.agents/skills/data-diagnosis/references/diagnosis-method.md` | ~150 行 | 诊断方法论（异常→定位→原因→建议） |
| `.agents/skills/data-diagnosis/references/chapter-problem-patterns.md` | ~200 行 | 章节问题模式库（数据特征映射） |
| `.agents/skills/data-diagnosis/references/report-template.md` | ~100 行 | 诊断报告模板 |
| `.agents/skills/data-diagnosis/scripts/analyze-metrics.js` | ~200 行 | CSV 指标计算 + 异常标记 + 趋势数据 |

---

## 任务 9.1：创建目录结构

```bash
mkdir -p .agents/skills/data-diagnosis/references
mkdir -p .agents/skills/data-diagnosis/scripts
```

---

## 任务 9.2：编写 SKILL.md

### 完整内容

```markdown
---
name: data-diagnosis
description: 数据诊断。导入平台数据，分析章节问题，输出诊断报告。
---

# data-diagnosis（数据诊断）

> **用途**：发布 5-10 章后，导入平台数据，诊断问题章节，给出改进建议。
> **前置条件**：有平台导出的 CSV 数据文件。
> **输出文件**：`data_diagnosis_report.yaml`

---

## 核心原则

1. **数据说话**：基于实际数据诊断，不凭感觉。
2. **定位到章节**：每个问题都要定位到具体章节。
3. **原因+建议**：不只报告问题，还要分析原因、给出建议。
4. **趋势分析**：不只看单章，要看整体趋势。

---

## Phase 定义

### Phase 1：数据导入

**入口条件**：CSV 文件存在
**目标**：解析平台数据

**步骤**：
1. 询问用户 CSV 文件路径
2. 读取 CSV 文件，解析字段（章节号、阅读数、读完率、互动数、点赞数、追读数等）
3. 展示数据概览（总章数、时间范围、核心指标均值）
4. 确认数据完整

**出口条件**：数据解析完成
**加载 References**：无

---

### Phase 2：指标计算

**入口条件**：数据已解析
**目标**：计算核心指标

**步骤**：
1. 运行 `scripts/analyze-metrics.js` 计算指标
2. 展示指标结果：
   - 每章的读完率、互动率、追读率
   - 异常标记（掉读率 > 15%、互动 < 均值 30%）
   - 趋势图（ASCII 或描述性）
3. 确认指标计算正确

**出口条件**：指标数据就绪
**加载 References**：无

---

### Phase 3：异常定位

**入口条件**：指标已计算
**目标**：从数据异常定位到具体章节

**步骤**：
1. 读取 `references/diagnosis-method.md`
2. 按方法论分析异常章节：
   - 掉读率突增的章节
   - 互动率异常低的章节
   - 追读数下降的章节
3. 输出问题章节列表

**出口条件**：问题章节列表确定
**加载 References**：`diagnosis-method.md`

---

### Phase 4：原因分析

**入口条件**：问题章节已定位
**目标**：分析每个问题章节的原因

**步骤**：
1. 读取 `references/chapter-problem-patterns.md`
2. 对每个问题章节，匹配问题模式：
   - 开篇拖沓（前 500 字无冲突）
   - 高潮乏力（高潮段落太短/太弱）
   - 转场生硬（场景切换不自然）
   - 人设崩坏（角色行为不符合设定）
   - 水字数（无信息增量的段落）
3. 输出原因分析报告

**出口条件**：原因分析完成
**加载 References**：`chapter-problem-patterns.md`

---

### Phase 5：报告输出

**入口条件**：分析完成
**目标**：生成诊断报告

**步骤**：
1. 读取 `references/report-template.md`
2. 按模板生成报告，包含：
   - 数据概览
   - 异常章节列表 + 原因 + 建议
   - 整体趋势分析
   - 改进优先级
3. 写入 `data_diagnosis_report.yaml`
4. 展示报告摘要给用户

**出口条件**：报告已生成
**加载 References**：`report-template.md`, `metrics-guide.md`

---

## 质量门禁

本 skill 无自动化脚本门禁，但要求：
- 每个问题章节必须有原因分析
- 每个原因必须有改进建议
- 报告必须包含数据概览和趋势分析

---

## 断点恢复

**状态文件**：`_progress.md`
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

---

## 输出文件

- `data_diagnosis_report.yaml`：诊断报告

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1-2 | — | 数据导入和指标计算 |
| 3 | diagnosis-method.md | 诊断方法论 |
| 4 | chapter-problem-patterns.md | 问题模式匹配 |
| 5 | report-template.md, metrics-guide.md | 报告生成 |

---

## 下一步

诊断报告生成后，可回到 `/daily-write` 针对性修改问题章节。
```

---

## 任务 9.3：编写 references/metrics-guide.md

### 完整内容

```markdown
# 指标体系

> **用途**：Phase 1-2 数据导入和指标计算时对照使用。

---

## 核心指标

### 阅读指标
| 指标 | 定义 | 健康值 | 异常阈值 |
|------|------|--------|---------|
| 阅读数 | 本章阅读人次 | — | — |
| 读完率 | 读完全章的比例 | ≥ 70% | < 50% |
| 掉读率 | 中途放弃的比例 | ≤ 20% | > 30% |

### 互动指标
| 指标 | 定义 | 健康值 | 异常阈值 |
|------|------|--------|---------|
| 评论数 | 本章评论数 | ≥ 均值 50% | < 均值 30% |
| 点赞数 | 本章点赞数 | ≥ 均值 50% | < 均值 30% |
| 打赏数 | 本章打赏数 | — | — |
| 互动率 | (评论+点赞+打赏) / 阅读数 | ≥ 5% | < 2% |

### 追读指标
| 指标 | 定义 | 健康值 | 异常阈值 |
|------|------|--------|---------|
| 追读数 | 持续追读的读者数 | 稳定或增长 | 连续 3 章下降 |
| 追读率 | 追读数 / 阅读数 | ≥ 30% | < 20% |
| 追读跌幅 | 本章追读 / 上章追读 | ≥ 90% | < 85% |

---

## 指标计算方法

### 读完率
```
读完率 = 读完全章的人数 / 打开本章的人数 × 100%
```

### 互动率
```
互动率 = (评论数 + 点赞数 + 打赏数) / 阅读数 × 100%
```

### 追读率
```
追读率 = 追读数 / 阅读数 × 100%
```

### 掉读率
```
掉读率 = 1 - 读完率
```

---

## 异常检测规则

### 掉读异常
```
如果 本章掉读率 - 上章掉读率 > 15%
则标记为「掉读异常」
```

### 互动异常
```
如果 本章互动数 < 近 10 章均值 × 30%
则标记为「互动异常」
```

### 追读异常
```
如果 连续 3 章追读数下降
则标记为「追读异常」
```

---

## 数据可视化

### ASCII 趋势图示例
```
读完率趋势：
第10章: ████████░░ 80%
第11章: ███████░░░ 70%  ← 下降
第12章: ██████░░░░ 60%  ← 异常
第13章: ███████░░░ 72%  ← 回升
```

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 指标完整 | 读完率、互动率、追读率都有 |
| 2 | 异常标记 | 异常章节都已标记 |
| 3 | 趋势可视 | 有 ASCII 趋势图或描述性趋势 |
```

---

## 任务 9.4：编写 references/diagnosis-method.md

### 完整内容

```markdown
# 诊断方法论

> **用途**：Phase 3 从数据异常定位到具体章节问题时使用。

---

## 诊断流程

```
数据异常 → 定位章节 → 分析原因 → 给出建议
```

---

## Step 1：数据异常分类

| 异常类型 | 检测方法 | 严重程度 |
|---------|---------|---------|
| 掉读突增 | 掉读率环比 > 15% | 高 |
| 互动低迷 | 互动数 < 均值 30% | 中 |
| 追读下降 | 连续 3 章追读下降 | 高 |
| 完读率低 | 读完率 < 50% | 中 |

---

## Step 2：章节定位

对于每个异常，定位到具体章节：

1. **掉读突增**：掉读率最高的那一章
2. **互动低迷**：互动数最低的那一章
3. **追读下降**：追读开始下降的拐点章节
4. **完读率低**：读完率最低的那一章

---

## Step 3：原因分析框架

对每个问题章节，从以下维度分析：

### 开篇问题
- 前 500 字有无冲突/钩子？
- 是否有大段无信息量的描写？
- 开篇是否承接上章悬念？

### 节奏问题
- 是否有连续多段对话无动作/心理？
- 是否有大段内心独白无推进？
- 高潮段落是否太短/太弱？

### 人物问题
- 角色行为是否符合设定？
- 对话是否符合角色风格？
- 是否有角色突然"降智"？

### 剧情问题
- 本章是否推进了主线？
- 是否有信息增量？
- 结尾是否有钩子？

---

## Step 4：建议生成

根据原因，给出具体建议：

| 原因 | 建议 |
|------|------|
| 开篇无冲突 | 重写前 500 字，加入冲突/悬念 |
| 节奏拖沓 | 删减无信息量段落，加速推进 |
| 高潮太弱 | 扩展高潮段落，增加细节和反应 |
| 人设崩坏 | 回看角色设定，修正行为 |
| 无信息增量 | 删章或合并到上一章 |
| 结尾无钩子 | 增加章末悬念/反转 |

---

## 诊断报告结构

```yaml
diagnosis:
  overview:
    total_chapters: 30
    date_range: 2026-06-01 ~ 2026-06-29
    avg_read_rate: 72%
    avg_engagement_rate: 4.5%
  
  problem_chapters:
    - chapter: 12
      issues:
        - type: 掉读突增
          severity: 高
          cause: 开篇大段环境描写，500字无冲突
          suggestion: 重写开篇，先展示冲突再补环境
    - chapter: 18
      issues:
        - type: 互动低迷
          severity: 中
          cause: 本章纯过渡，无信息增量
          suggestion: 合并到第 17 章，或加入支线冲突
  
  trends:
    read_rate: 稳定（70-75%）
    engagement: 第 12 章后回升
    follow: 整体增长，第 18 章小幅下降
  
  priorities:
    - 高优：重写第 12 章开篇
    - 中优：合并第 17-18 章
    - 低优：优化第 25 章结尾钩子
```
```

---

## 任务 9.5：编写 references/chapter-problem-patterns.md

### 完整内容

```markdown
# 章节问题模式库

> **用途**：Phase 4 匹配问题章节的数据特征时对照使用。

---

## 模式 1：开篇拖沓

### 数据特征
- 掉读率突增（前 20% 内容流失严重）
- 读完率低于均值

### 典型表现
- 前 500 字无冲突/钩子
- 大段环境描写/回忆
- 开篇不承接上章悬念

### 诊断方法
- 检查章节前 500 字是否有冲突/悬念
- 检查是否有无信息量的描写段落

---

## 模式 2：高潮乏力

### 数据特征
- 互动率低于均值（读者无感）
- 评论数少

### 典型表现
- 高潮段落太短（< 200 字）
- 高潮无细节描写
- 缺少围观者反应

### 诊断方法
- 检查本章是否有明确的高潮点
- 检查高潮段落的长度和细节
- 检查是否有围观者反应链

---

## 模式 3：转场生硬

### 数据特征
- 掉读率在章节中段突增
- 读者评论提到"看不懂"/"跳跃"

### 典型表现
- 场景切换无过渡
- 时间跳跃无提示
- 视角切换突兀

### 诊断方法
- 检查场景切换是否有过渡句
- 检查时间/地点/视角变化是否有明确提示

---

## 模式 4：人设崩坏

### 数据特征
- 评论出现负面反馈（"人设崩了"/"OOC"）
- 互动率下降

### 典型表现
- 角色行为不符合设定
- 对话风格突变
- 角色突然"降智"推动剧情

### 诊断方法
- 对比角色设定，检查行为是否合理
- 检查对话风格是否一致

---

## 模式 5：水字数

### 数据特征
- 读完率低
- 互动率低
- 追读下降

### 典型表现
- 大段重复描写
- 无信息量的对话
- 内心独白过多
- 本章无主线推进

### 诊断方法
- 检查本章是否有信息增量
- 检查是否有可删减的段落
- 检查本章是否推进了主线

---

## 模式 6：结尾无钩子

### 数据特征
- 追读率下降（读者不期待下一章）
- 本章读完率正常但下章开读率低

### 典型表现
- 章节在平淡处结束
- 无悬念/反转/期待
- 所有冲突都在本章解决

### 诊断方法
- 检查章末最后 200 字是否有钩子
- 检查是否留有未解决的悬念

---

## 模式匹配表

| 数据特征 | 可能模式 | 验证方法 |
|---------|---------|---------|
| 掉读突增（开头） | 开篇拖沓 | 检查前 500 字 |
| 掉读突增（中段） | 转场生硬 | 检查场景切换 |
| 互动率低 | 高潮乏力 / 水字数 | 检查高潮段落 / 信息增量 |
| 追读下降 | 结尾无钩子 | 检查章末钩子 |
| 评论负面 | 人设崩坏 | 对比角色设定 |
| 读完率低 | 水字数 | 检查信息增量 |

---

## 多模式叠加

一章可能同时有多个问题。优先级：
1. 开篇拖沓（直接影响掉读）
2. 人设崩坏（影响口碑）
3. 水字数（影响追读）
4. 高潮乏力（影响互动）
5. 转场生硬（影响体验）
6. 结尾无钩子（影响追读）
```

---

## 任务 9.6：编写 references/report-template.md

### 完整内容

```markdown
# 诊断报告模板

> **用途**：Phase 5 生成诊断报告时对照使用。

---

## 报告结构

```yaml
# 数据诊断报告
report_date: YYYY-MM-DD
data_source: CSV 文件名
data_range:
  start: YYYY-MM-DD
  end: YYYY-MM-DD
  total_chapters: N

# 数据概览
overview:
  avg_read_rate: XX%
  avg_engagement_rate: XX%
  avg_follow_rate: XX%
  trend: 上升/稳定/下降

# 异常章节
problem_chapters:
  - chapter: N
    position: 第 N 章《章节标题》
    issues:
      - type: 问题类型
        severity: 高/中/低
        data_evidence: 具体数据（如掉读率 45%）
        cause: 原因分析
        suggestion: 改进建议

# 趋势分析
trends:
  read_rate: 描述性趋势
  engagement: 描述性趋势
  follow: 描述性趋势

# 改进优先级
priorities:
  - priority: 高
    action: 具体行动
    target_chapter: N
  - priority: 中
    action: ...
  - priority: 低
    action: ...

# 总结
summary: |
  一段话总结整体情况和主要问题。
```

---

## 报告撰写指南

### 数据概览
- 用 3-5 个核心指标概括整体表现
- 给出趋势判断（上升/稳定/下降）

### 异常章节
- 每个问题章节独立一条
- 必须有数据证据（不能只说"这章不好"）
- 原因要具体（不能只说"写得不好"）
- 建议要可操作（不能只说"改进"）

### 趋势分析
- 用描述性语言，不用复杂图表
- 关注拐点（突然变好/变差的章节）

### 改进优先级
- 高优：直接影响读者留存的问题
- 中优：影响阅读体验的问题
- 低优：锦上添花的优化

---

## 示例片段

```yaml
problem_chapters:
  - chapter: 12
    position: 第 12 章《夜遇》
    issues:
      - type: 开篇拖沓
        severity: 高
        data_evidence: 掉读率 42%（均值 25%），环比 +17%
        cause: 前 500 字全是环境描写，无冲突无钩子，读者大量流失
        suggestion: 重写开篇，先展示男主遭遇袭击的冲突，环境描写挪到后面
```
```

---

## 任务 9.7：编写 scripts/analyze-metrics.js

### 完整内容

```javascript
#!/usr/bin/env node
// analyze-metrics.js — CSV 指标计算 + 异常标记
// Usage: node analyze-metrics.js <csv_file>

const fs = require('fs');

function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node analyze-metrics.js <csv_file>');
    process.exit(2);
  }

  const csv = fs.readFileSync(file, 'utf8');
  const lines = csv.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
  
  // 解析数据
  const chapters = [];
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim());
    const row = {};
    headers.forEach((h, idx) => { row[h] = values[idx]; });
    chapters.push(row);
  }

  if (chapters.length === 0) {
    console.error('No data found');
    process.exit(1);
  }

  // 计算均值
  const metrics = ['读完率', '互动率', '追读率', '掉读率'];
  const avgs = {};
  for (const m of metrics) {
    const vals = chapters.map(c => parseFloat(c[m]) || 0).filter(v => v > 0);
    avgs[m] = vals.length > 0 ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
  }

  // 异常检测
  const anomalies = [];
  for (let i = 0; i < chapters.length; i++) {
    const ch = chapters[i];
    const chapterNum = ch['章节'] || ch['chapter'] || (i + 1);
    
    // 掉读突增
    const dropRate = parseFloat(ch['掉读率']) || 0;
    if (i > 0) {
      const prevDrop = parseFloat(chapters[i-1]['掉读率']) || 0;
      if (dropRate - prevDrop > 15) {
        anomalies.push({
          chapter: chapterNum,
          type: '掉读突增',
          severity: '高',
          evidence: `掉读率 ${dropRate}%，环比 +${(dropRate - prevDrop).toFixed(1)}%`,
        });
      }
    }

    // 互动低迷
    const engagement = parseFloat(ch['互动率']) || 0;
    if (engagement > 0 && engagement < avgs['互动率'] * 0.3) {
      anomalies.push({
        chapter: chapterNum,
        type: '互动低迷',
        severity: '中',
        evidence: `互动率 ${engagement}%，低于均值 30%（均值 ${avgs['互动率'].toFixed(1)}%）`,
      });
    }

    // 完读率低
    const readRate = parseFloat(ch['读完率']) || 0;
    if (readRate > 0 && readRate < 50) {
      anomalies.push({
        chapter: chapterNum,
        type: '完读率低',
        severity: '中',
        evidence: `读完率 ${readRate}%，低于 50%`,
      });
    }
  }

  // 追读连续下降检测
  const followRates = chapters.map(c => parseFloat(c['追读数']) || 0);
  for (let i = 2; i < followRates.length; i++) {
    if (followRates[i] < followRates[i-1] && followRates[i-1] < followRates[i-2]) {
      anomalies.push({
        chapter: chapters[i]['章节'] || (i + 1),
        type: '追读连续下降',
        severity: '高',
        evidence: `连续 3 章追读下降：${followRates[i-2]} → ${followRates[i-1]} → ${followRates[i]}`,
      });
    }
  }

  // 输出结果
  const result = {
    total_chapters: chapters.length,
    averages: avgs,
    anomalies: anomalies,
    trend: calculateTrend(followRates),
  };

  console.log(JSON.stringify(result, null, 2));
}

function calculateTrend(values) {
  if (values.length < 3) return '数据不足';
  const recent = values.slice(-5);
  const first = recent[0];
  const last = recent[recent.length - 1];
  if (last > first * 1.1) return '上升';
  if (last < first * 0.9) return '下降';
  return '稳定';
}

main();
```

---

## 执行顺序

1. 创建目录结构
2. 编写 SKILL.md
3. 编写 metrics-guide.md
4. 编写 diagnosis-method.md
5. 编写 chapter-problem-patterns.md
6. 编写 report-template.md
7. 编写 analyze-metrics.js
8. 验证脚本可运行
9. Commit

---

## 下一步

诊断报告生成后，可回到 `/daily-write` 针对性修改问题章节。

---

## 全部 Phase 完成

至此，9 个 skill 的重构计划全部完成：

| Phase | Skill | 状态 |
|-------|-------|------|
| 0 | 基础设施 | ✅ 已执行 |
| 1 | scout-topic | ✅ 计划已写 |
| 2 | worldbuilding | ✅ 计划已写 |
| 3 | design-character | ✅ 计划已写 |
| 4 | design-outline | ✅ 计划已写 |
| 5 | design-chapters | ✅ 计划已写 |
| 6 | golden-chapters | ✅ 计划已写 |
| 7 | daily-write | ✅ 计划已写 |
| 8 | paywall-design | ✅ 计划已写 |
| 9 | data-diagnosis | ✅ 计划已写 |
