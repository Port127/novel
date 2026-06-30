---
name: golden-chapters
description: 黄金三章锻造。按品类模板和微节拍逐段生成前三章，验证结构。
---

# golden-chapters（黄金三章锻造）

> **用途**：基于细纲生成前三章正文。前三章决定读者留存，必须严格验证结构。
> **前置条件**：
> - `settings/outline.yaml` 存在（主线大纲已设计，提供全局悬念与目标）
> - `settings/chapters_index.yaml` 存在（细纲已设计）
> - `settings/scout_report.yaml` 存在（品类已确定）
> - `settings/characters.yaml` 存在（人设已完成）
> **输出文件**：
> - `content/chapter_001.md`
> - `content/chapter_002.md`
> - `content/chapter_003.md`

---

## 1. 架构与行为规范 (System Rules)

> **[系统强制]** 本板块定义 Agent 必须遵守的操作流转规则，绝对不可违背或删减。
1. **防暴走与启发式交互 (UX)**：严禁一次性执行多个 Phase 或连发开放式提问。每个 Phase 结束前必须停下等待用户。提问时必须基于上下文提供 **2-3 个具体预设方案 (Option A/B/C)** 供用户选择或微调。
2. **多智能体编排 (Orchestration)**：在涉及重度脑暴或深度执行的 Phase 中，主 Agent 必须使用 `invoke_subagent` 唤醒对应的专业子 Agent（如 `narrative-writer`）来负责具体的交互与生成，主 Agent 仅负责流程统筹与最终落盘。
3. **上下文闭环 (Context Loop)**：如果在 Phase 中要求读取上游文件，则最终落盘的数据结构中，必须有对应的联动字段进行支撑，不能读而不用。
4. **实时进度保存 (State Persistence)**：进入任何一个新的 Phase，必须立即更新根目录下的 `_progress.md` 文件。

## 2. 创作与业务准则 (Domain Rules)

> **[业务核心]** 本板块定义该 Skill 独有的领域知识、创作契约和设定标准。
1. **商业对齐 (Commercial Alignment)**：必须基于 `scout_report.yaml` 中的品类进行设计，刻意制造差异化。
2. **素材库联动 (Ecosystem)**：当需要寻找灵感时，主动向用户推荐或直接使用 `/nm` 命令查询上游素材库获取原文锚点。
3. **核心原则**：
   - **前三章定生死**：读者在前三章决定去留。每章必须有明确的"留客"功能。
   - **品类感知开篇**：根据 `required_elements.opening_hook.type` 选择开篇策略。
   - **微节拍控制**：段落级别的节奏控制，确保阅读流畅。
   - **去AI味**：生成的正文必须通过 AI 味检测。
   - **结构验证**：每章生成后立即验证结构，不合格则重写。
   - **前 100 字事件密度 ≥ 3**：开头必须快速抓住读者，不能慢热。
   - **核心展示**：前三章必须展示金手指/核心优势/核心冲突。
   - **章尾钩子强**：每章结尾必须有强钩子，让读者想看下一章。

---

## Phase 定义 (Phase State Machine)

> **【架构强制要求】**：
> 1. 生成任何结构化数据前，**必须使用 `view_file` 强制读取对应的 `data/schemas/*.schema.yaml`**。
> 2. 严禁按己意图捏造不在 Schema 中的顶级字段。
> 3. Reference 文件应当按需在具体的 Phase 中加载，不要在 Phase 1 一次性全读完。

### Phase 1：品类适配

**入口条件**：chapters_index.yaml、scout_report.yaml、characters.yaml 存在
**目标**：根据品类加载黄金三章模板和开篇钩子策略

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 1。
2. **强制读取 Schema**：对于需要结构化落盘的报告，必须读取 `data/schemas/*.schema.yaml`。
3. 读取 `scout_report.yaml`，获取 `genre` 和 `required_elements.opening_hook`。
4. 读取 `references/genre-templates.md`，加载品类对应的黄金三章节拍模板。
5. 读取 `references/golden-rules.md`，加载核心规则。
6. **品类适配检查清单**（参考 `references/opening-design.md`「黄金一章检查清单」）：

| 检查项 | 标准 | 必须 |
|--------|------|------|
| 前 100 字事件密度 | ≥ 3 个事件/动作/信息点 | ✅ |
| 核心冲突是否建立 | 读者知道主角要面对什么 | ✅ |
| 主角人设是否立住 | 至少 1 个鲜明特质展示 | ✅ |
| 金手指/核心优势是否展示 | 读者知道主角靠什么赢 | ✅ |
| 章尾钩子是否强 | 悬念强度 ≥ 60 | ✅ |
| 品类套路是否到位 | 符合品类读者期待 | ✅ |

7. **开篇策略选择决策树**（参考 `references/opening-design.md`「决策路由」）：

```
开篇类型选择：
├─ 玄幻/系统 → golden_finger（废柴受辱 → 金手指觉醒 → 首次反击）
├─ 都市重生 → reborn_advantage（重生节点 → 利用先知优势 → 第一步逆袭）
├─ 都市言情 → meet_cute（尴尬相遇 → 化学反应 → 误会/冲突）
├─ 悬疑 → mystery_hook（异常事件 → 调查深入 → 更大谜团）
└─ 通用 → conflict（冲突爆发 → 主角应对 → 新困境）
```

8. **9 种开头技巧速查**（参考 `references/opening-design.md`）：
   - 冲突前置、信息差钩、反常行为、重生反常、超自然身份、灵魂旁观、悬念句、替嫁被弃、代入式提问
9. **强制素材提取（Few-shot 原文锚点）**：
   - 主 Agent 必须调用 `/nm` 工具检索对标：`nm search chapter --genre {当前品类} --type opening`
   - 从检索到的同类爆款第一章中，提取 300-500 字精华片段作为“原文锚点”（Anchor Excerpts）。这用于后续向子 Agent 展示正确的情绪、句长和笔调节奏，**严禁抄袭字句**。
10. **启发式提问**：展示提取的品类标准套路及原文锚点，提供 Option A/B/C 方案供用户选择。
11. **停顿确认**：等待用户确认方案后，再进入下一阶段。

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
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 2。
2. 读取 `chapters_index.yaml` 第 1 章的摘要和节拍
   - 如存在 `settings/chapter_outlines/chapter_001.md` 至 `chapter_003.md`，应优先读取详细蓝图补足微节拍；但章节定位、文件名和状态仍以 `settings/chapters_index.yaml` 为准。
3. 读取 `references/micro-beat-guide.md`
4. 按品类开篇钩子要求生成第一章：
   - 300 字内出第一个冲突/钩子
   - 立住主角人设
   - 展示主角起点状态
   - 展示金手指/核心优势的苗头
5. **单章锻造检查清单**（每章生成后必检）：

| 检查项 | 标准 | 第一章特殊要求 |
|--------|------|---------------|
| 前 100 字事件密度 | ≥ 3 | 必须快速抓住读者 |
| 核心展示 | 金手指/优势/冲突展示 | 必须有苗头 |
| 章尾钩子 | 悬念强度 ≥ 60 | 必须让读者想看第二章 |
| 主角人设 | 至少 1 个鲜明特质 | 必须立住 |
| 微节拍 | 段落节奏流畅 | 按 micro-beat-guide.md |
| 品类套路 | 符合品类期待 | 按 genre-templates.md |

6. 运行门禁：执行 `node .agents/skills/golden-chapters/scripts/check-golden-structure.js settings/scout_report.yaml content/chapter_001.md`
7. 如不通过，调整后重新生成
8. **停顿确认**：第一章验证通过后，将成果与用户确认，直至用户 Accept。

**出口条件**：第一章通过结构验证和锻造检查
**加载 References**：`micro-beat-guide.md`、`opening-design.md`

#### Agent 调用：narrative-writer（可选增强）

如果项目已部署 narrative-writer agent（检查 `.agents/agents/narrative-writer.md` 是否存在），可读取该文件内容，使用 `invoke_subagent` 工具执行第一章正文写作。
**致密上下文组装要求（写前准备）**：必须将以下模块组装为完整的 Prompt 传递给子 Agent：

- **【全局意图】**：提供 `outline.yaml` 中本卷/本篇的核心目的，结合本章意图（例如："快节奏打脸——起因是账单暴露，逻辑线=发现→逼问→公开代价，读者等了三章，这章必须一拳到位"）。
- **【本章节拍】**：直接输入 `chapters_index.yaml` 中第 1 章的详细微节拍（含 密/疏 节奏和目标字数）。
- **【开篇策略与检查单】**：必须指明采用的开篇钩子类型（如：`golden_finger`），并强制其检查本章产出是否满足 `opening-design.md` 中的“黄金一章检查清单”（前100字事件密度≥3，展示金手指等）。
- **【原文锚点 (Few-shot)】**：提供 Phase 1 提取的 300-500 字优秀案例参考片段（作为笔法、标点节奏和悬念设置的参考，禁止照搬情节）。
- **【相关角色】**：提供 `characters.yaml` 中本章涉及人物的核心特质和登场状态。
- **【强制自学指令】**：明确要求子 Agent "必须优先使用系统工具自行去读取并学习 references/opening-design.md（黄金一章检查清单）与 references/micro-beat-guide.md（微观笔法），严禁凭空猜测创作规则！"

如 agent 不可用，由主线程按上述要求直接写作。

---

### Phase 3：第二章锻造

**入口条件**：第一章已完成
**目标**：生成第二章正文

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 3。
2. 读取第 2 章摘要和节拍
3. 按品类要求展示核心优势（金手指/重生优势/相遇等）
4. 生成第二章
5. **单章锻造检查**：
   - 前 100 字是否有新信息/新冲突推进
   - 核心优势是否进一步展示
   - 章尾钩子是否让读者想看第三章
   - 与第一章是否有情绪差异（不能趋同）
6. 运行门禁：执行 `node .agents/skills/golden-chapters/scripts/check-golden-structure.js settings/scout_report.yaml content/chapter_001.md content/chapter_002.md`
7. **停顿确认**：本章验证通过后，与用户确认，直至被 Accept。

**出口条件**：第二章通过结构验证和锻造检查
**加载 References**：`micro-beat-guide.md`

**品类差异化要求**：
- 玄幻：首次使用金手指，展示威力
- 都市重生：利用先知优势做出第一个正确决策
- 都市言情：与恋爱对象的第二次互动，化学反应加深
- 悬疑：新线索出现，谜团加深

#### Agent 调用：narrative-writer（可选增强）

如果项目已部署 narrative-writer agent，可使用 `invoke_subagent` 工具执行第二章写作。
**必须组装致密上下文（写前准备）**：

- **【全局意图】**：必须明确与第一章的情绪差异，提炼一句话写作意图（例："承接上一章的情绪点，利用先知优势做出第一个正确决策，展示爽感苗头"）。
- **【本章节拍】**：提供 `chapters_index.yaml` 中第 2 章的详细微节拍。
- **【核心优势展示】**：强调第二章必须进一步展示核心优势或金手指，不能让其隐形。
- **【原文锚点与检查单】**：提供对应的参考片段以及单章锻造检查要求。
- **【强制自学指令】**：明确要求子 Agent "必须优先使用系统工具自行去读取并学习 references/opening-design.md 与 references/micro-beat-guide.md（微观笔法），严禁凭空猜测创作规则！"

如 agent 不可用，由主线程按上述要求直接写作。

---

### Phase 4：第三章锻造

**入口条件**：第二章已完成
**目标**：生成第三章正文（首个小高潮）

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 4。
2. 读取第 3 章摘要和节拍
3. 设计首个小高潮，让读者看到"爽"的可能性
4. 生成第三章
5. **单章锻造检查**：
   - 是否有明确的小高潮/爽点
   - 读者是否看到主角的能力/优势
   - 章尾钩子是否让读者想看第四章（进入正式剧情）
   - 三章连起来是否构成完整的"黄金三章"弧线
6. 运行门禁：执行 `node .agents/skills/golden-chapters/scripts/check-golden-structure.js settings/scout_report.yaml content/chapter_001.md content/chapter_002.md content/chapter_003.md`
7. **停顿确认**：本章验证通过后，与用户确认，直至被 Accept。

**出口条件**：第三章通过结构验证和锻造检查
**加载 References**：`micro-beat-guide.md`

**品类差异化要求**：
- 玄幻：首次打脸，展示金手指威力
- 都市重生：利用先知优势获得第一个重大收益
- 都市言情：关键互动，关系产生质变
- 悬疑：重大线索揭示，谜团升级

#### Agent 调用：narrative-writer（可选增强）

如果项目已部署 narrative-writer agent，可使用 `invoke_subagent` 工具执行第三章写作。
**必须组装致密上下文（写前准备）**：

- **【全局意图】**：提炼一句话写作意图，明确指出本章是“黄金三章”的首个小高潮，必须让读者看到“爽”的可能性。
- **【本章节拍】**：提供 `chapters_index.yaml` 中第 3 章的详细微节拍。
- **【情绪与钩子】**：本章结束必须设置强力钩子，让读者产生购买/追读下一章的强烈欲望，连贯前三章的弧线。
- **【原文锚点与检查单】**：提供对应的参考片段以及单章锻造检查要求。
- **【强制自学指令】**：明确要求子 Agent "必须优先使用系统工具自行去读取并学习 references/opening-design.md 与 references/micro-beat-guide.md（微观笔法），严禁凭空猜测创作规则！"

如 agent 不可用，由主线程按上述要求直接写作。

---

### Phase 5：去AI味处理

**入口条件**：三章初稿已完成
**目标**：去除 AI 写作痕迹

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 5。
2. 运行门禁：执行 `node .agents/skills/golden-chapters/scripts/check-ai-patterns.js content/chapter_001.md content/chapter_002.md content/chapter_003.md`
3. 运行门禁：执行 `node .agents/skills/golden-chapters/scripts/check-degeneration.js content/chapter_001.md content/chapter_002.md content/chapter_003.md`
4. 根据检测结果修改正文
5. 重新运行脚本直到通过
6. **停顿确认**：去味处理完成后，等待用户确认最终版质量。

**出口条件**：所有脚本检测通过
**加载 References**：`anti-ai-writing.md`

---

### Phase 6：定稿输出

**入口条件**：所有章节通过验证
**目标**：输出最终文件

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 6。
2. 最终检查三章连贯性。
3. **写入文件**：生成并写入 `content/chapter_001.md`、`chapter_002.md`、`chapter_003.md` 以及评估报告 `history/golden_chapters_report.md`。
4. **清理状态**：验证通过并落盘后，宣告本技能完成。

**出口条件**：文件已输出
**加载 References**：无

---

## 断点恢复 (Recovery)

**状态文件**：`_progress.md`（位于项目根目录）

**格式范例**：
```markdown
# golden-chapters Progress
- current_phase: <1-6>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`。
- 若状态非 completed，主动询问用户是否继续中断的进度，跳到对应的 current_phase。

---

## 质量门禁 (Quality Gates)

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
- `history/golden_chapters_report.md`

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
