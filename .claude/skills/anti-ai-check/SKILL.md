---
name: anti-ai-check
description: 检测章节中的AI痕迹并输出量化评分（七维：套话/句式/比喻/描写/对白/转折/心理）
when_to_use: 用户想降低AI感，或在发布前做文本质检
argument-hint: "[章节ID]"
arguments: chapter_id
---

# 任务

对指定章节进行去 AI 感检查。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 按 [章节自动推断协议](_protocols/chapter-auto-inference.md) 确定目标章节
3. 读取 `{current_path}/chapters/$0.md`
4. 读取 `shared/styles/anti_ai_rules.yaml`（若存在）
5. 读取本章出场角色的 `speech_pattern`（用于对白同质化检测）

## 执行步骤

### 1. 六维指标分析

按 `anti_ai_rules.yaml` 的 `scoring.dimensions` 逐项检测：

**A. 套话密度（权重 18%）**
- 扫描全文，统计命中 `phrase_watchlist` 的次数
- 计算每千字命中率

**B. 句式重复（权重 15%）**
- 短句重复率是否超过 `repeated_short_sentence_ratio`
- 排比/并列结构占比是否超过 `parallel_structure_ratio`
- 连续相同句首是否超过 `consecutive_same_opener`

**C. 比喻过载（权重 17%）**
- 统计全文比喻句数量（含明喻、暗喻），计算每千字密度
- 超过 `metaphor.max_per_1000_chars` 即报警
- 检测连续比喻（比喻叠比喻）
- 标记命中 `metaphor.watchlist_patterns` 的具体位置

**D. 描写堆砌（权重 15%）**
- 识别纯描写段落（无对白、无动作、无心理的环境/外貌/氛围段）
- 计算纯描写占全文比例，超过 `description_ratio.max_pure_description_ratio` 即报警
- 检测连续纯描写段落数，超过 `max_consecutive_desc_paragraphs` 即报警

**E. 对白同质化（权重 17%）**
- 提取所有对白，检查是否命中 `dialogue.generic_dialogue_patterns`
- 计算通用对白占比，超过 `max_generic_ratio` 即报警
- 对比不同角色的对白，检测说话风格是否可区分
- 如果角色有 `speech_pattern`，检查对白是否符合其语言画像

**F. 机械转折（权重 8%）**
- 统计"然而""却不曾想""殊不知"等转折词频率
- 检测是否存在模板化叙事结构（如"正当...时""就在这时"）

**G. 心理描写质量（权重 12%）**
- **Show vs Tell 比例**：统计直接告知情绪的句子（"他很愤怒""她感到悲伤"）vs 通过动作/细节/生理反应展现情绪的句子（"指甲掐进掌心""喉咙像被什么堵住"），Tell 占比超过 60% 即报警
- **内心独白套路化**：检测模板化心理描写（"心如刀绞""瞳孔一缩""不由得握紧了拳头""心中暗道"），命中 `phrase_watchlist` 的心理描写类词条
- **情绪层次数**：单个情绪场景中是否只有一层情绪（如纯愤怒），还是有矛盾/混合情绪（愤怒中带自责、恐惧下的倔强）——单层情绪场景占比超过 80% 即标记「情绪扁平」
- **身体感受密度**：情绪高潮段落中是否有具体的生理反应描写（心跳/呼吸/肌肉/温度/疼痛），纯抽象情绪无身体锚点即扣分

### 2. 加权评分

每个维度 0-100 分，按权重加权得出总分。

| 等级 | 分数区间 | 含义 |
|------|---------|------|
| 低风险 | 80-100 | 人味充足 |
| 中风险 | 60-79 | 有 AI 痕迹，建议修 |
| 高风险 | 0-59 | AI 味重，必须改 |

### 3. 定位问题段落

按严重度排序，列出 Top-10 问题段落，每条标注：
- 段落位置（行号或段序）
- 命中的维度
- 具体问题描述
- 修复方向（一句话）

### 4. 写入检测报告

将本次检测结果追加到 `{current_path}/quality/ai_trace_report.yaml`（原有行为不变），**同时**按 [评估闸门协议](_protocols/eval-gate.md) 追加到 `{current_path}/chapters/{chapter_id}_review.yaml`，写入 `anti-ai-check` 条目（含各维度分数、overall、level、top_issues）。

追加到 `quality/ai_trace_report.yaml`：

```yaml
reports:
  - chapter: $0
    score: {{score}}
    level: {{level}}
    dimensions:
      套话密度: {{score_A}}
      句式重复: {{score_B}}
      比喻过载: {{score_C}}
      描写堆砌: {{score_D}}
      对白同质化: {{score_E}}
      机械转折: {{score_F}}
      心理描写: {{score_G}}
    top_issues:
      - location: "段落X"
        dimension: "比喻过载"
        detail: "连续3个明喻"
    date: {{今天日期}}
```

## 输出格式

```
去AI感检测：$0

总分：{{score}}/100 {{level}}
━━━━━━━━━━━━━━━━━━━━

维度明细：
  套话密度    {{score_A}}/100
  句式重复    {{score_B}}/100
  比喻过载    {{score_C}}/100
  描写堆砌    {{score_D}}/100
  对白同质化  {{score_E}}/100
  机械转折    {{score_F}}/100
  心理描写    {{score_G}}/100

重点问题（按严重度排序）：
1. [{{dimension}}] 段落{{N}}：{{具体问题}} → {{修复方向}}
2. ...

下一步：
   /anti-ai-rewrite $0 --level 2    执行改写
   /voice-check [角色名] $0         单独检查对白
```

## 注意事项

- 不改变核心剧情事实
- 优先修复高风险片段
- 比喻不是越少越好——问题是"AI式比喻"（空泛、模板化），精准的比喻应保留
- 描写不是越少越好——问题是"不推进叙事的纯描写堆砌"
