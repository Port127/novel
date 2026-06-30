---
name: golden-chapters
description: 黄金三章锻造。按品类模板和微节拍逐段生成前三章，验证结构。
---

# golden-chapters（黄金三章锻造）

> **用途**：基于细纲生成前三章正文。前三章决定读者留存，必须严格验证结构。
> **前置条件**：
> - `settings/chapters_index.yaml` 存在（细纲已设计）
> - `settings/scout_report.yaml` 存在（品类已确定）
> - `settings/characters.yaml` 存在（人设已完成）
> **输出文件**：
> - `content/chapter_001.md`
> - `content/chapter_002.md`
> - `content/chapter_003.md`

---

## 核心原则

1. **前三章定生死**：读者在前三章决定去留。每章必须有明确的"留客"功能。
2. **品类感知开篇**：根据 `required_elements.opening_hook.type` 选择开篇策略。
3. **微节拍控制**：段落级别的节奏控制，确保阅读流畅。
4. **去AI味**：生成的正文必须通过 AI 味检测。
5. **结构验证**：每章生成后立即验证结构，不合格则重写。
6. **前 100 字事件密度 ≥ 3**：开头必须快速抓住读者，不能慢热。
7. **核心展示**：前三章必须展示金手指/核心优势/核心冲突。
8. **章尾钩子强**：每章结尾必须有强钩子，让读者想看下一章。

---

## Phase 定义

### Phase 1：品类适配

**入口条件**：chapters_index.yaml、scout_report.yaml、characters.yaml 存在
**目标**：根据品类加载黄金三章模板和开篇钩子策略

**步骤**：
1. 读取 `scout_report.yaml`，获取 `genre` 和 `required_elements.opening_hook`
2. 读取 `references/genre-templates.md`，加载品类对应的黄金三章节拍模板
3. 读取 `references/golden-rules.md`，加载核心规则
4. **品类适配检查清单**（参考 `references/opening-design.md`「黄金一章检查清单」）：

| 检查项 | 标准 | 必须 |
|--------|------|------|
| 前 100 字事件密度 | ≥ 3 个事件/动作/信息点 | ✅ |
| 核心冲突是否建立 | 读者知道主角要面对什么 | ✅ |
| 主角人设是否立住 | 至少 1 个鲜明特质展示 | ✅ |
| 金手指/核心优势是否展示 | 读者知道主角靠什么赢 | ✅ |
| 章尾钩子是否强 | 悬念强度 ≥ 60 | ✅ |
| 品类套路是否到位 | 符合品类读者期待 | ✅ |

5. **开篇策略选择决策树**（参考 `references/opening-design.md`「决策路由」）：

```
开篇类型选择：
├─ 玄幻/系统 → golden_finger（废柴受辱 → 金手指觉醒 → 首次反击）
├─ 都市重生 → reborn_advantage（重生节点 → 利用先知优势 → 第一步逆袭）
├─ 都市言情 → meet_cute（尴尬相遇 → 化学反应 → 误会/冲突）
├─ 悬疑 → mystery_hook（异常事件 → 调查深入 → 更大谜团）
└─ 通用 → conflict（冲突爆发 → 主角应对 → 新困境）
```

6. **9 种开头技巧速查**（参考 `references/opening-design.md`）：
   - 冲突前置、信息差钩、反常行为、重生反常、超自然身份、灵魂旁观、悬念句、替嫁被弃、代入式提问
7. 展示品类标准套路，与用户确认

**品类×开篇钩子**：

| 品类 | 开篇钩子类型 | 标准套路 |
|------|------------|---------|
| 玄幻 | golden_finger | 废柴受辱 → 金手指觉醒 → 首次反击 |
| 都市重生 | reborn_advantage | 重生节点 → 利用先知优势 → 第一步逆袭 |
| 都市言情 | meet_cute | 尴尬相遇 → 化学反应 → 误会/冲突 |
| 系统文 | golden_finger | 系统激活 → 首个任务 → 奖励碾压 |
| 悬疑 | mystery_hook | 异常事件 → 调查深入 → 更大谜团 |
| 通用 | conflict | 冲突爆发 → 主角应对 → 新困境 |

**出口条件**：品类模板已加载，开篇策略已确认
**加载 References**：`genre-templates.md`、`golden-rules.md`、`opening-design.md`

---

### Phase 2：第一章锻造

**入口条件**：品类模板已加载
**目标**：生成第一章正文

**步骤**：
1. 读取 `chapters_index.yaml` 第 1 章的摘要和节拍
2. 读取 `references/micro-beat-guide.md`
3. 按品类开篇钩子要求生成第一章：
   - 300 字内出第一个冲突/钩子
   - 立住主角人设
   - 展示主角起点状态
   - 展示金手指/核心优势的苗头
4. **单章锻造检查清单**（每章生成后必检）：

| 检查项 | 标准 | 第一章特殊要求 |
|--------|------|---------------|
| 前 100 字事件密度 | ≥ 3 | 必须快速抓住读者 |
| 核心展示 | 金手指/优势/冲突展示 | 必须有苗头 |
| 章尾钩子 | 悬念强度 ≥ 60 | 必须让读者想看第二章 |
| 主角人设 | 至少 1 个鲜明特质 | 必须立住 |
| 微节拍 | 段落节奏流畅 | 按 micro-beat-guide.md |
| 品类套路 | 符合品类期待 | 按 genre-templates.md |

5. 运行 `scripts/check-golden-structure.js` 验证结构
6. 如不通过，调整后重新生成

**出口条件**：第一章通过结构验证和锻造检查
**加载 References**：`micro-beat-guide.md`、`opening-design.md`

#### Agent 调用：narrative-writer（可选增强）

如果项目已部署 narrative-writer agent（检查 `.agents/agents/narrative-writer.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 执行第一章正文写作：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 章节信息：第 1 章、品类 {X}
- 相关文件路径：content/chapter_001.md

如 agent 不可用，由主线程直接写作。

---

### Phase 3：第二章锻造

**入口条件**：第一章已完成
**目标**：生成第二章正文

**步骤**：
1. 读取第 2 章摘要和节拍
2. 按品类要求展示核心优势（金手指/重生优势/相遇等）
3. 生成第二章
4. **单章锻造检查**：
   - 前 100 字是否有新信息/新冲突推进
   - 核心优势是否进一步展示
   - 章尾钩子是否让读者想看第三章
   - 与第一章是否有情绪差异（不能趋同）
5. 运行结构验证

**出口条件**：第二章通过结构验证和锻造检查
**加载 References**：`micro-beat-guide.md`

**品类差异化要求**：
- 玄幻：首次使用金手指，展示威力
- 都市重生：利用先知优势做出第一个正确决策
- 都市言情：与恋爱对象的第二次互动，化学反应加深
- 悬疑：新线索出现，谜团加深

#### Agent 调用：narrative-writer（可选增强）

如果项目已部署 narrative-writer agent（检查 `.agents/agents/narrative-writer.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 执行第二章正文写作：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 章节信息：第 2 章、品类 {X}
- 相关文件路径：content/chapter_002.md

如 agent 不可用，由主线程直接写作。

---

### Phase 4：第三章锻造

**入口条件**：第二章已完成
**目标**：生成第三章正文（首个小高潮）

**步骤**：
1. 读取第 3 章摘要和节拍
2. 设计首个小高潮，让读者看到"爽"的可能性
3. 生成第三章
4. **单章锻造检查**：
   - 是否有明确的小高潮/爽点
   - 读者是否看到主角的能力/优势
   - 章尾钩子是否让读者想看第四章（进入正式剧情）
   - 三章连起来是否构成完整的"黄金三章"弧线
5. 运行结构验证

**出口条件**：第三章通过结构验证和锻造检查
**加载 References**：`micro-beat-guide.md`

**品类差异化要求**：
- 玄幻：首次打脸，展示金手指威力
- 都市重生：利用先知优势获得第一个重大收益
- 都市言情：关键互动，关系产生质变
- 悬疑：重大线索揭示，谜团升级

#### Agent 调用：narrative-writer（可选增强）

如果项目已部署 narrative-writer agent（检查 `.agents/agents/narrative-writer.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 执行第三章正文写作：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 章节信息：第 3 章、品类 {X}
- 相关文件路径：content/chapter_003.md

如 agent 不可用，由主线程直接写作。

---

### Phase 5：去AI味处理

**入口条件**：三章初稿已完成
**目标**：去除 AI 写作痕迹

**步骤**：
1. 运行 `scripts/check-ai-patterns.js` 检测 AI 模式
2. 运行 `scripts/check-degeneration.js` 检测退化
3. 根据检测结果修改正文
4. 重新运行脚本直到通过

**出口条件**：所有脚本检测通过
**加载 References**：`anti-ai-writing.md`

---

### Phase 6：定稿输出

**入口条件**：所有章节通过验证
**目标**：输出最终文件

**步骤**：
1. 最终检查三章连贯性
2. 写入 `content/chapter_001.md`、`chapter_002.md`、`chapter_003.md`
3. 生成评估报告 `golden_chapters_report.yaml`

**出口条件**：文件已输出
**加载 References**：无

---

## 质量门禁

| 检查项 | 工具 | 说明 |
|--------|------|------|
| 结构完整性 | check-golden-structure.js | 按品类检查开篇钩子类型 |
| AI味检测 | check-ai-patterns.js | blocking 项归零 |
| 退化检测 | check-degeneration.js | blocking 项归零 |

---

## 输出文件

- `content/chapter_001.md`
- `content/chapter_002.md`
- `content/chapter_003.md`
- `golden_chapters_report.yaml`

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | genre-templates.md、golden-rules.md、opening-design.md | 品类模板 + 核心规则 + 开篇设计决策树 |
| 2-4 | micro-beat-guide.md、opening-design.md | 微节拍设计 + 单章锻造检查 |
| 5 | anti-ai-writing.md | 去AI味指南 |

---

## 下一步

黄金三章完成后，可进入：
- `/paywall-design`：付费卡点设计
- `/daily-write`：日更写作

---

## 黄金三章常见错误速查

| 错误类型 | 表现 | 修正方法 | 参考 |
|---------|------|---------|------|
| 慢热开头 | 前 100 字无事件，大段描写 | 删减描写，事件前置 | opening-design.md |
| 人设模糊 | 读完三章记不住主角特质 | 增加鲜明特质展示 | golden-rules.md |
| 金手指隐形 | 三章结束读者不知道主角靠什么赢 | 明确展示核心优势 | genre-templates.md |
| 钩子无力 | 章尾无悬念，读者不想看下一章 | 用 13 式钩子设计 | opening-design.md |
| 品类错位 | 不符合品类读者期待 | 按品类模板调整 | genre-templates.md |
| 三章趋同 | 三章情绪/功能相同 | 第一章立人设，第二章展优势，第三章小高潮 | — |
| AI 味重 | 套话/万能比喻/升华收尾 | 按 anti-ai-writing.md 去味 | anti-ai-writing.md |
