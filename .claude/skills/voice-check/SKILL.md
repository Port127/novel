---
name: voice-check
description: 检查角色对白是否具有稳定且可区分的人物声音
when_to_use: 用户担心角色说话同质化，或想强化角色个性表达
argument-hint: "[角色名] [章节范围]"
arguments: character range
---

# 任务

检查指定角色在章节范围内的对白一致性与辨识度。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. **角色自动推断**：如果 `$0`（角色名）未提供——检查用户当前打开/引用的文件是否为 `characters/*.yaml`，若是则提取角色名；否则提示用户指定
3. **章节范围自动推断**：如果 `$1`（范围）未提供——按 [章节自动推断协议](_protocols/chapter-auto-inference.md) 确定检查范围
4. 读取角色卡 `{current_path}/characters/$0.yaml`，重点提取 `speech_pattern` 和 `traits`
5. 读取章节内容（按 `$1` 范围）
6. 读取 `shared/styles/anti_ai_rules.yaml` 中的 `dialogue` 规则

## 输入参数

- `$0` (character): 角色名
- `$1` (range): 章节范围，如 `ch001-ch010`（可选）

## 执行步骤

### 1. 提取对白样本

抽取该角色全部对白，统计：
- 常用句法结构（短句/长句/反问/祈使）
- 语气词分布
- 口头禅出现频率
- 粗话使用频率
- 平均句长

### 2. 对比角色语言画像

如果角色卡有 `speech_pattern`，逐字段对比：

| speech_pattern 字段 | 检查项 |
|---------------------|--------|
| `tone` | 实际对白语气是否符合设定基调 |
| `sentence_style` | 句式偏好是否一致（如设定"短句多"但实际对白全是长句） |
| `catchphrase` | 口头禅是否在对白中出现过（出现率过低则提醒） |
| `profanity_level` | 粗话频率是否匹配（设定"满嘴脏话"但对白很文雅就有问题） |
| `education_voice` | 用词水平是否匹配角色教育背景 |
| `verbal_tics` | 语言小癖好是否体现 |
| `taboo_words` | 是否出现了角色不该说的词 |
| `sample_lines` | 实际对白与典型台词的风格是否一致 |

如果角色卡没有 `speech_pattern`，输出警告并建议补充。

### 3. 对比角色性格

检查对白是否符合角色卡中的 `traits`、`moral_spectrum` 和身份设定：
- 粗犷角色是否说了过于文雅的话
- 阴险角色是否太直白
- 少年角色是否说了老气横秋的话

### 4. 横向对比其他角色

提取同场景中其他主要角色的对白，做风格区分度检测：
- 如果遮住角色名，能否通过对白内容猜出是谁说的？
- 两个角色的句式、语气、用词是否过度重合
- 量化区分度分数

### 5. 通用句式检测

检查是否命中 `anti_ai_rules.yaml` 的 `dialogue.generic_dialogue_patterns`：
- "我明白了""你说得对""这不可能"等通用句式占比
- 超过阈值则标记为同质化风险

### 6. 写入评估结果

按 [评估闸门协议](_protocols/eval-gate.md)，将检查结果追加到 `{current_path}/chapters/{chapter_id}_review.yaml`（若检查范围为单章）。

写入 `voice-check` 条目，包含：
- `profile_match`：语言画像匹配度（0-100）
- `distinctiveness`：横向区分度（0-100）
- suggestions 列表（含 character/issue/fix_direction）

若检查范围跨多章，不写入 review 文件，仅输出报告。

### 7. 生成修复建议

针对每个发现的问题，给出**具体可操作**的修复建议：

**不要说**：
- "增加角色个性"（太笼统）
- "让对白更有特色"（没有操作性）

**要说**：
- "张三设定 profanity_level=常见，但 ch003 的 8 句对白中 0 句粗话。建议把'你别这样做'改为'你他妈能不能消停点'"
- "李四设定 tone=阴阳怪气，但对白都是直述句。建议把'我不同意'改为'哦？你觉得呢？'"
- "张三和李四在 ch005 的对白句式高度重合（区分度 23%）。张三应多用短句反问，李四应多用长句铺垫"

## 输出格式

```
人物声音检查：$0

语言画像匹配：{{match_score}}/100
区分度：{{distinctiveness}}/100
━━━━━━━━━━━━━━━━━━━━

画像对比：
  语气基调    设定：{{tone}}       实际：{{actual_tone}}       {{match}}
  句式偏好    设定：{{style}}      实际：{{actual_style}}      {{match}}
  粗话程度    设定：{{level}}      实际：{{actual_level}}      {{match}}
  口头禅      设定：{{phrases}}    出现率：{{rate}}            {{match}}

{{#if no_speech_pattern}}
⚠️ 该角色尚未设置 speech_pattern，建议运行：
   /character-edit $0 补充语言画像
{{/if}}

问题与修复建议：
1. {{具体问题}} → {{具体改写建议，带原句和改后句}}
2. ...

横向对比：
  vs {{角色B}}  区分度 {{score}}%  {{评价}}
  vs {{角色C}}  区分度 {{score}}%  {{评价}}

下一步：
   /character-edit $0 补充/修正 speech_pattern
   /anti-ai-rewrite $chapter --level 2   改写对白
```

## 注意事项

- 建议同时检查 2-3 个关键角色做横向对比
- 不以"口癖堆砌"替代人物声音——口头禅是辅助手段，核心是句式、语气和用词层次的差异
- 修复建议必须带原句和改后句示例，不要只给方向
- 如果角色没有 `speech_pattern`，从其 `traits` 和 `profile` 推断一个建议画像，提示用户确认
