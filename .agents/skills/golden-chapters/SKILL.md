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

---

## Phase 定义

### Phase 1：品类适配

**入口条件**：chapters_index.yaml、scout_report.yaml、characters.yaml 存在
**目标**：根据品类加载黄金三章模板和开篇钩子策略

**步骤**：
1. 读取 `scout_report.yaml`，获取 `genre` 和 `required_elements.opening_hook`
2. 读取 `references/genre-templates.md`，加载品类对应的黄金三章节拍模板
3. 读取 `references/golden-rules.md`，加载核心规则
4. 展示品类标准套路，与用户确认

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
**加载 References**：`genre-templates.md`、`golden-rules.md`

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
4. 运行 `scripts/check-golden-structure.js` 验证结构
5. 如不通过，调整后重新生成

**出口条件**：第一章通过结构验证
**加载 References**：`micro-beat-guide.md`

---

### Phase 3：第二章锻造

**入口条件**：第一章已完成
**目标**：生成第二章正文

**步骤**：
1. 读取第 2 章摘要和节拍
2. 按品类要求展示核心优势（金手指/重生优势/相遇等）
3. 生成第二章
4. 运行结构验证

**出口条件**：第二章通过结构验证
**加载 References**：无

---

### Phase 4：第三章锻造

**入口条件**：第二章已完成
**目标**：生成第三章正文（首个小高潮）

**步骤**：
1. 读取第 3 章摘要和节拍
2. 设计首个小高潮，让读者看到"爽"的可能性
3. 生成第三章
4. 运行结构验证

**出口条件**：第三章通过结构验证
**加载 References**：无

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
| 1 | genre-templates.md、golden-rules.md | 品类模板 + 核心规则 |
| 2-4 | micro-beat-guide.md | 微节拍设计 |
| 5 | anti-ai-writing.md | 去AI味指南 |

---

## 下一步

黄金三章完成后，可进入：
- `/paywall-design`：付费卡点设计
- `/daily-write`：日更写作
