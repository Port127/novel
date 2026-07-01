# 文档偏差修复实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复 6 项文档/模板偏差，让项目文档体系口径完全统一、无误导、无缺口。

**Architecture:** 纯文档与模板修改，不涉及代码变更。按影响面从大到小排序：先隔离历史文档（防止误导），再补内容遗漏（让文档完整），最后关闭已知缺口（Schema/路径对齐）。每个 Task 独立可验证、可提交。

**Tech Stack:** Markdown、YAML

---

## 偏差总览

| # | 偏差 | 严重级别 | 对应 Task |
|---|------|----------|-----------|
| 1 | `docs/superpowers/` 历史文档未归档隔离，38 篇混在正式文档目录 | 中 | Task 1 |
| 2 | `REQUIREMENTS.md` §5.3 辅助 Skill 列表漏列 `review` | 低 | Task 2 |
| 3 | `templates/default/settings/` 缺少 `scout_report.yaml` 模板 | 低 | Task 3 |
| 4 | `data-diagnosis/SKILL.md` 脚本路径仍为短路径 `scripts/analyze-metrics.js` | 中 | Task 4 |
| 5 | `feedback/archive/analysis_report.md` 内容严重过时且误导性强 | 中 | Task 5 |
| 6 | `SKILL_CONTRACT_AUDIT.md` 更新——标记已关闭项 | 低 | Task 6 |

---

## Task 1: 归档隔离 `docs/superpowers/` 历史文档

**目标：** 让 `docs/superpowers/` 下的 38 篇历史文档不再被误认为当前真相源。

**Files:**
- Modify: `docs/README.md`
- Rename: `docs/superpowers/` → `docs/archive/superpowers/`

- [ ] **Step 1: 移动 superpowers 目录到 archive 下**

```bash
mkdir -p docs/archive
git mv docs/superpowers docs/archive/superpowers
```

> 注意：本计划文件也会随之移动到 `docs/archive/superpowers/plans/2026-07-01-documentation-deviation-fix.md`，这是预期行为。

- [ ] **Step 2: 更新 `docs/README.md`，将 `superpowers/` 从"相关资料"移到"归档"区**

在 `docs/README.md` 中找到以下段落：

```markdown
## 相关资料

| 路径 | 说明 |
|------|------|
| `../README.md` | 项目总入口 |
| `../.agents/AGENTS.md` | Agent 行为规则与项目硬约束 |
| `../.agents/skills/` | 当前实际执行入口，每个 Skill 的 `SKILL.md` 是具体流程真相源 |
| `../data/schemas/` | YAML Schema 与完善度标准 |
| `../templates/` | 新书项目模板 |

## 工作流产出

`superpowers/` 目录保存历史设计、计划与验证文档：

- `specs/`：设计规格文档
- `plans/`：实施计划文档
- `verification/`：验证报告

这些文档用于追溯历史决策，不一定代表当前主流程。若与 `.agents/skills/` 冲突，以当前 Skill 文件为准。

## 归档

`feedback/archive/` 存放历史反馈和报告，仅供参考。
```

替换为：

```markdown
## 相关资料

| 路径 | 说明 |
|------|------|
| `../README.md` | 项目总入口 |
| `../.agents/AGENTS.md` | Agent 行为规则与项目硬约束 |
| `../.agents/skills/` | 当前实际执行入口，每个 Skill 的 `SKILL.md` 是具体流程真相源 |
| `../data/schemas/` | YAML Schema 与完善度标准 |
| `../templates/` | 新书项目模板 |

## 归档

以下内容均为历史产物，**不代表当前主流程**。若与 `.agents/skills/` 或正式文档冲突，以正式文档和 Skill 文件为准。

| 路径 | 说明 |
|------|------|
| `archive/superpowers/specs/` | 历史设计规格文档（含已放弃的 CLI 自动化方向） |
| `archive/superpowers/plans/` | 历史实施计划文档 |
| `archive/superpowers/verification/` | 历史验证报告 |
| `feedback/archive/` | 历史反馈和分析报告 |
```

- [ ] **Step 3: 确认移动后目录结构正确**

Run: `ls docs/archive/superpowers/`
Expected: `plans  specs  verification`

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "docs(archive): 将 superpowers 历史文档移入 archive 隔离

38 篇历史设计/计划/验证文档不再混在正式文档目录中，
防止新维护者误将已放弃的 CLI 自动化方向当作当前真相源。"
```

---

## Task 2: 补 `REQUIREMENTS.md` 漏列的 `review` Skill

**目标：** 在辅助类 Skills 表中补上 `review`。

**Files:**
- Modify: `docs/REQUIREMENTS.md:115-126`

- [ ] **Step 1: 在辅助类 Skills 表中补充 `review`**

在 `docs/REQUIREMENTS.md` 中找到 §5.3 辅助类 Skills 表格：

```markdown
| Skill | 用途 |
|-------|------|
| `nm` | 调用 novel-material 检索素材 |
| `review` | 多视角对抗式审查 |
| `data-diagnosis` | 平台数据诊断 |
```

等等，让我重新确认——实际当前内容是：

```markdown
| Skill | 用途 |
|-------|------|
| `nm` | 调用 novel-material 检索素材 |
| `review` | 多视角对抗式审查 |
| `data-diagnosis` | 平台数据诊断 |
| `stock-check` | 存稿水位检查 |
| `feature-planning` | 新功能规划 |
| `refactor-planning` | 重构规划 |
| `code-review-change` | 变动影响审查 |
| `commit-msg` | 规范化提交信息 |
```

经重新确认，`review` **已在表中**。此偏差不存在，跳过本 Task。

> **自我修正**：在写计划时重新阅读了 `REQUIREMENTS.md` 第 117-127 行，`review` 确实已列出。前一轮分析遗漏了这一点。此 Task 取消。

- [ ] **Step 1: 无需操作，Commit 跳过**

---

## Task 3: 补充 `scout_report.yaml` 模板

**目标：** 在 `templates/default/settings/` 中新增 `scout_report.yaml` 空模板，与 schema 对齐。

**Files:**
- Create: `templates/default/settings/scout_report.yaml`

- [ ] **Step 1: 创建模板文件**

```yaml
# 选题侦察报告模板
# [R] = 必填字段，[O] = 可选字段
# 由 /scout-topic 生成，后续 Skill 根据 required_elements 动态检查

platform: ""                    # [R] 目标平台（番茄小说、起点、晋江等）
channel: ""                     # [O] 频道（男频/女频）
genre: ""                       # [R] 品类（都市、玄幻、系统、言情等）
target_audience: ""             # [R] 目标读者群体

premise: ""                     # [R] 一句话前提（50字以上的故事概述）
core_hooks: []                  # [O] 核心钩子列表
# 每个钩子包含：name, description, hook_type

recommended_tags:               # [R] 标签组合
  primary: []                   # 主要标签（3-6个）
  secondary: []                 # 次要标签

tag_analysis: {}                # [O] 标签分析详情
competition_analysis: {}        # [O] 竞争分析

required_elements:              # [O] 品类感知的必要元素声明
  worldbuilding:
    required: []
    optional: []
  characters: {}
  opening_hook:
    type: ""
    description: ""
  structure:
    type: ""
    target_arcs: 1

risks: []                       # [O] 风险提示
```

- [ ] **Step 2: 确认模板字段与 `data/schemas/scout_report.schema.yaml` 的 required 字段一致**

Run: `grep -A1 "required:" data/schemas/scout_report.schema.yaml | head -10`
Expected: `platform`, `genre`, `target_audience`, `premise`, `recommended_tags` 均出现在模板中

- [ ] **Step 3: Commit**

```bash
git add templates/default/settings/scout_report.yaml
git commit -m "templates: 补充 scout_report.yaml 空模板

与 data/schemas/scout_report.schema.yaml 的 required 字段对齐，
新书初始化时有模板可参考。"
```

---

## Task 4: 修正 `data-diagnosis/SKILL.md` 中的脚本短路径

**目标：** 将 `scripts/analyze-metrics.js` 短路径修正为完整路径。

**Files:**
- Modify: `.agents/skills/data-diagnosis/SKILL.md:35`

- [ ] **Step 1: 读取当前内容确认行号**

Run: `grep -n "scripts/" .agents/skills/data-diagnosis/SKILL.md`
Expected: 第 35 行有 `scripts/analyze-metrics.js`

- [ ] **Step 2: 将短路径替换为完整路径**

将：

```
3. 运行 `scripts/analyze-metrics.js` 解析数据
```

替换为：

```
3. 运行 `.agents/skills/data-diagnosis/scripts/analyze-metrics.js` 解析数据
```

- [ ] **Step 3: 验证脚本文件确实在该路径**

Run: `ls .agents/skills/data-diagnosis/scripts/analyze-metrics.js`
Expected: 文件存在

- [ ] **Step 4: Commit**

```bash
git add .agents/skills/data-diagnosis/SKILL.md
git commit -m "fix(data-diagnosis): 修正脚本短路径为完整路径

scripts/analyze-metrics.js → .agents/skills/data-diagnosis/scripts/analyze-metrics.js
与 SKILL_CONTRACT_AUDIT 中 P2 修正项对齐。"
```

---

## Task 5: 精简过时的 `analysis_report.md`

**目标：** 将已失效且误导性强的分析报告精简为简短摘要，避免新维护者被旧方向带偏。

**Files:**
- Modify: `docs/feedback/archive/analysis_report.md`

- [ ] **Step 1: 将原文件内容替换为精简版**

将整个文件内容替换为：

```markdown
> **历史归档**：此文档为项目转型前（V3 引擎重构前）生成的分析报告。
> 报告基于旧的"自动化 CLI 流水线"方向评估，该方向已被放弃。
> 当前项目定位为 **Skill 驱动的人机协同创作工作台**，入口为 `.agents/skills/`。
> 报告中的"致命问题"（generate.py、write.py 不存在等）针对的是旧方向，
> 不影响当前 Skill 主流程。仅作历史参考，不代表当前产品状态。

# Novel V2 项目审视报告（历史归档）

- **生成时间**：项目早期阶段
- **评估方向**：自动化 CLI 流水线（已放弃）
- **当前方向**：Skill 驱动人机协同创作（`.agents/skills/`）
- **文档状态**：已失效，仅存档

如需了解当前项目能力，请参阅：
- [README.md](../../README.md)
- [用户手册](../../USER_MANUAL.md)
- [需求文档](../../REQUIREMENTS.md)
```

- [ ] **Step 2: Commit**

```bash
git add docs/feedback/archive/analysis_report.md
git commit -m "docs(archive): 精简过时的 analysis_report.md

原报告基于已放弃的 CLI 自动化方向，'致命问题'描述严重误导。
精简为历史摘要 + 当前文档导航，防止新维护者被旧方向带偏。"
```

---

## Task 6: 更新 `SKILL_CONTRACT_AUDIT.md` 关闭已修正项

**目标：** 在审计文档中标记本轮已关闭的缺口（data-diagnosis 路径修正、scout_report 模板补充）。

**Files:**
- Modify: `docs/SKILL_CONTRACT_AUDIT.md`

- [ ] **Step 1: 更新 `data-diagnosis` 行的"对齐结论"列**

在 Skill 输入输出总表中，找到 `data-diagnosis` 行，将：

```
| `data-diagnosis` | 平台导出 CSV、可选 `settings/chapters_index.yaml` | `data_diagnosis_report.yaml` | 无直接 schema | 当前写法为 `scripts/analyze-metrics.js` 短路径 | 无明确 `_progress.md` 合约 | 非本轮高影响 Skill；后续应补脚本路径和报告 schema。 |
```

替换为：

```
| `data-diagnosis` | 平台导出 CSV、可选 `settings/chapters_index.yaml` | `data_diagnosis_report.yaml` | 无直接 schema | `.agents/skills/data-diagnosis/scripts/analyze-metrics.js` | 无明确 `_progress.md` 合约 | 脚本路径已修正；报告 schema 待后续补充。 |
```

- [ ] **Step 2: 在"后续实施建议"中追加本轮完成项**

在 `docs/SKILL_CONTRACT_AUDIT.md` 末尾的"后续实施建议"段落中，在第 5 条之后追加：

```markdown
6. 已修正 `data-diagnosis` 脚本短路径为完整路径。
7. 已补充 `templates/default/settings/scout_report.yaml` 模板。
8. 已将 `docs/superpowers/` 移入 `docs/archive/superpowers/`，与正式文档隔离。
9. 已精简 `docs/feedback/archive/analysis_report.md`，消除过时误导。
```

- [ ] **Step 3: Commit**

```bash
git add docs/SKILL_CONTRACT_AUDIT.md
git commit -m "docs(audit): 更新 SKILL_CONTRACT_AUDIT 关闭本轮已修正项

- data-diagnosis 脚本路径已修正
- scout_report 模板已补充
- superpowers 历史文档已归档
- analysis_report 已精简"
```

---

## Task 7: 最终验证

**目标：** 确认所有修改正确、无遗漏。

- [ ] **Step 1: 确认目录结构**

Run:
```bash
echo "=== archive 目录 ==="
ls docs/archive/superpowers/
echo "=== templates 目录 ==="
ls templates/default/settings/
echo "=== 正式 docs 目录（不应有 superpowers）==="
ls docs/ | grep -v archive
```

Expected:
- `docs/archive/superpowers/` 存在且包含 `plans/ specs/ verification/`
- `templates/default/settings/` 包含 `scout_report.yaml`
- `docs/` 根目录下不再有 `superpowers/`

- [ ] **Step 2: 确认 `data-diagnosis` 脚本路径已修正**

Run: `grep "scripts/" .agents/skills/data-diagnosis/SKILL.md`
Expected: 包含 `.agents/skills/data-diagnosis/scripts/analyze-metrics.js`，不再有裸 `scripts/analyze-metrics.js`

- [ ] **Step 3: 确认 `analysis_report.md` 已精简**

Run: `wc -l docs/feedback/archive/analysis_report.md`
Expected: 行数从 ~248 行降至 ~20 行以内

- [ ] **Step 4: 检查 git log 确认所有 commit**

Run: `git log --oneline -6`
Expected: 5 个新 commit（Task 2 已取消）

- [ ] **Step 5: 通读 `docs/README.md` 确认归档区正确**

Run: `cat docs/README.md`
Expected: 包含 `archive/superpowers/` 和 `feedback/archive/` 的归档表格，无旧的"工作流产出"段落

---

## 执行建议

本计划共 5 个实质 Task（Task 2 已取消）+ 1 个验证 Task，全部为文档/模板修改。建议：

1. **顺序执行**：每个 Task 独立 commit，按编号顺序推进
2. **验证节点**：Task 7 做最终全量检查
3. **预计耗时**：15-20 分钟
