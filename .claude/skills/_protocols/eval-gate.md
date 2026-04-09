# 评估闸门协议（Eval Gate Protocol）

> 受 Anthropic Generator-Evaluator 架构启发：生成与评估分离，评估结果结构化落盘，低于阈值时阻断状态推进。

## 核心原则

1. **评估结果必须落盘**：`chapter-review`、`voice-check`、`anti-ai-check` 的结论写入 `chapters/{chapter_id}_review.yaml`，不能只输出到终端
2. **阈值阻断**：`pipeline-draft-polish` 在推进状态前检查评估分数，低于阈值时暂停并说明原因
3. **反馈闭环**：`chapter-draft` 在生成前读取已有的 review 文件，避免重犯已知问题

## 评估结果文件格式

文件路径：`{current_path}/chapters/{chapter_id}_review.yaml`

```yaml
chapter: ch001
last_reviewed: "2026-04-09"
reviews:
  - skill: chapter-review
    date: "2026-04-09"
    scores:
      structure: 75        # 结构完整性 0-100
      pacing: 60           # 节奏 0-100
      character: 80        # 角色一致性 0-100
      hook: 70             # 钩子有效性 0-100
      emotion: 65          # 情绪张力 0-100
    overall: 70
    blocking_issues: []     # 必须修复才能推进的问题
    suggestions:            # 建议修复的问题
      - priority: high
        location: "段落3-5"
        issue: "开场缺少异常点，读者无理由继续读"
        fix_direction: "用一个反常细节替代日常铺垫"
      - priority: medium
        location: "段落12"
        issue: "角色做了正确选择但没有代价"
        fix_direction: "让选择导致一个副作用"
  - skill: voice-check
    date: "2026-04-09"
    scores:
      profile_match: 85    # 语言画像匹配度
      distinctiveness: 60  # 横向区分度
    overall: 72
    suggestions:
      - priority: high
        character: "张三"
        issue: "设定 profanity_level=常见，但 8 句对白 0 句粗话"
        fix_direction: "把'你别这样'改为'你他妈消停点'"
  - skill: anti-ai-check
    date: "2026-04-09"
    scores:
      cliche: 80
      sentence_pattern: 70
      metaphor: 65
      description: 75
      dialogue: 60
      transition: 85
      psychology: 70
    overall: 72
    level: "中风险"
    top_issues:
      - location: "段落8"
        dimension: "比喻过载"
        detail: "连续3个明喻"
```

## 闸门阈值

| 评估维度 | 推进阈值 | 阻断行为 |
|----------|---------|---------|
| anti-ai overall | >= 60 | 低于 60 不推进到 revise，提示先改写 |
| voice distinctiveness | >= 40 | 低于 40 警告对白同质化严重 |
| structure | >= 50 | 低于 50 不推进，提示结构问题 |

**阈值是默认值，用户可以覆盖**：
- `pipeline-draft-polish --force`：跳过闸门强制推进
- `pipeline-draft-polish --threshold 50`：降低阈值

## 闸门检查流程（pipeline-draft-polish 执行）

```
1. 执行 chapter-review → 写入 _review.yaml
2. 执行 voice-check → 追加到 _review.yaml
3. 执行 anti-ai-check → 追加到 _review.yaml
4. 读取 _review.yaml 的所有 scores
5. 检查是否有任何分数低于阈值：
   - 有 → 输出阻断报告，不推进状态
     "⛔ 评估未通过，暂不推进到 revise：
      - anti-ai: 55/100（阈值 60）→ 建议先 /anti-ai-rewrite
      - structure: 45/100（阈值 50）→ 建议修复开场和结尾钩子
      使用 --force 可跳过闸门"
   - 无 → 正常推进
```

## 反馈读取流程（chapter-draft 执行）

```
1. 检查 chapters/{chapter_id}_review.yaml 是否存在
2. 若存在，提取所有 blocking_issues 和 high priority suggestions
3. 在写作指令中注入：
   "前次审查发现以下问题，本次生成应避免：
    - [问题列表]"
4. 生成完成后在写作备忘中标注：
   "已参考前次审查反馈（{date}），重点修正了：[...]"
```
