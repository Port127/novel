---
name: daily-write
description: 日更写作入口。扩写 → 核查 → 去AI味 → 钩子审查，通过质量门禁后定稿。
---

# daily-write（日更写作）

> **用途**：基于细纲逐章写作正文。通过质量门禁流水线确保输出质量。
> **前置条件**：
> - `settings/chapters_index.yaml` 存在（细纲已设计）
> **输出文件**：
> - `content/chapter_XXX.md`

---

## 核心原则

1. **断点恢复**：通过 `_progress.md` 记录写作进度，崩溃后可从断点续跑。
2. **质量门禁**：每章必须通过 JS 脚本检测 + LLM 评估双重验证。
3. **上下文追踪**：通过状态追踪文件保持章节间连贯性。
4. **反AI味**：生成的正文必须通过 AI 味检测，去除写作指纹。
5. **钩子密度**：每章末尾必须有悬念钩子，保持读者粘性。

---

## Phase 定义

### Phase 1：选题确认

**入口条件**：chapters_index.yaml 存在
**目标**：确定本章写作目标

**步骤**：
1. 读取 `chapters_index.yaml`，展示待写章节列表
2. 检查 `_progress.md`，如有未完成进度则提示续跑
3. 选择目标章节（默认从第1章开始）
4. 展示本章摘要和节拍

**出口条件**：目标章节已确定
**加载 References**：无

---

### Phase 2：上下文加载

**入口条件**：目标章节已确定
**目标**：加载写作所需的上下文信息

**步骤**：
1. 读取前章末 300 字（如有）
2. 读取本章摘要和节拍
3. 读取 `references/state-tracking.md`，加载状态追踪协议
4. 读取追踪文件（如有），了解角色状态、伏笔进度
5. 组装写作上下文

**出口条件**：上下文就绪
**加载 References**：`state-tracking.md`

---

### Phase 3：写作执行

**入口条件**：上下文就绪
**目标**：生成本章正文初稿

**步骤**：
1. 读取 `references/writing-flow.md`，加载写作流程
2. 按 13 步写作流程执行：
   - 确定本章目标
   - 设计开头钩子
   - 展开主要场景
   - 推进剧情线
   - 设计章末悬念
3. 生成 2000-5000 字正文

**出口条件**：初稿生成
**加载 References**：`writing-flow.md`

**可选：素材参考**：如需外部参考，调用 `/nm` 搜索同品类正文片段。

#### Agent 调用：narrative-writer（可选增强）

如果项目已部署 narrative-writer agent（检查 `.agents/agents/narrative-writer.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 执行正文写作：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 章节信息：章节 {N}、字数目标 {X}、目标情绪 {Y}
- 相关文件路径：content/chapter_{N}.md
- 上下文摘要：涉及角色、待回收伏笔、参考技法

如 agent 不可用，由主线程直接写作。

---

### Phase 4：确定性检查

**入口条件**：初稿生成
**目标**：运行 JS 脚本进行确定性检测

**步骤**：
1. 运行 `scripts/check-ai-patterns.js` 检测 AI 模式
2. 运行 `scripts/check-degeneration.js` 检测退化
3. 运行 `scripts/normalize-punctuation.js` 规范化标点
4. 根据检测结果修改正文
5. 重新运行脚本直到 blocking 项归零

**出口条件**：所有脚本检测通过
**加载 References**：无

---

### Phase 5：LLM 评估

**入口条件**：脚本检测通过
**目标**：进行语义层面的质量评估

**步骤**：
1. 读取 `references/anti-ai-writing.md`，按 5 层标准评估：
   - 词汇层：是否有 AI 常用词
   - 句法层：是否有 AI 句式
   - 段落层：是否有 AI 段落结构
   - 叙事层：是否有 AI 叙事模式
   - 情感层：是否有 AI 情感表达
2. 读取 `references/hooks-guide.md`，评估钩子质量：
   - 悬念强度（≥60 通过）
   - 冲突密度（≥60 通过）
3. 读取 `references/quality-checklist.md`，逐项检查
4. 综合分 < 60 → 回到 Phase 3 重写
5. 读取 `references/banned-words.md`，检查禁词

**出口条件**：LLM 评估通过
**加载 References**：`anti-ai-writing.md`、`hooks-guide.md`、`quality-checklist.md`、`banned-words.md`

#### Agent 调用：consistency-checker（可选增强）

如果项目已部署 consistency-checker agent（检查 `.agents/agents/consistency-checker.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 做事实一致性扫描：

- 项目根目录：{当前项目绝对路径}
- 检查范围：content/chapter_{N}.md
- 已知角色：{从 settings/characters.yaml 提取角色名列表}

如 agent 不可用，跳过此步。

---

### Phase 6：定稿

**入口条件**：所有检查通过
**目标**：输出最终文件并更新追踪

**步骤**：
1. 更新状态追踪文件（角色状态、伏笔进度）
2. 写入 `content/chapter_XXX.md`
3. 更新 `_progress.md`，标记本章完成
4. 展示本章开头 500 字 + 结尾 300 字 + 质量报告

**出口条件**：章节完成
**加载 References**：无

---

## 质量门禁

| 门禁 | 工具 | 通过标准 |
|------|------|---------|
| AI模式检测 | check-ai-patterns.js | blocking 项归零 |
| 退化检测 | check-degeneration.js | blocking 项归零 |
| 标点规范 | normalize-punctuation.js | 自动修复 |
| 反AI评分 | LLM 评估 | ≥ 60 分 |
| 钩子评分 | LLM 评估 | ≥ 60 分 |

---

## 断点恢复

**状态文件**：`_progress.md`

**格式**：
```markdown
# daily-write Progress
- current_chapter: 5
- current_phase: 3
- status: in_progress
- last_updated: 2026-06-29T10:00:00Z
```

**恢复逻辑**：
- 启动时检查 `_progress.md`
- 若存在且 status != completed，提示用户是否续跑
- 跳到对应章节和 Phase 继续执行

---

## 输出文件

- `content/chapter_XXX.md`

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | — | 选题确认 |
| 2 | state-tracking.md | 状态追踪协议 |
| 3 | writing-flow.md | 写作流程 |
| 4 | — | 脚本检测 |
| 5 | anti-ai-writing.md, hooks-guide.md, quality-checklist.md, banned-words.md | LLM 评估 |
| 6 | — | 定稿输出 |

---

## 续写/改写

写作过程中可执行：
- **续写**：在已有正文基础上继续
- **改写**：修改已有正文（润色/扩充/精简/重写）
- **重新过审**：修改后重新跑质量门禁

---

## 下一步

本章完成后：
- 继续写下一章（自动进入 Phase 1）
- `/export-novel`：导出正文
