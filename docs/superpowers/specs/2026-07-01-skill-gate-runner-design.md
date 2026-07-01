# Skill Gate Runner Design

## 背景

本项目已经完成 Skill 合约审计和 schema 合约补强，当前主流程的路径、schema、模板和高影响 JS 门禁已经基本收束。剩余的核心风险是：执行仍然依赖 Agent 按 `SKILL.md` 自觉读取 schema、更新 `_progress.md`、调用脚本并解释门禁结果。

本设计不恢复旧 Python CLI，也不把创造性写作交给自动 runtime。它只为当前 Skill 驱动工作流补一个轻量执行层：统一发现门禁、运行确定性脚本、汇总 blocking/advisory、记录报告，并把后续完整 Skill Runner 的接口留出来。

## 目标

本轮目标是设计 **Skill Gate Runner**，先解决“质量门禁是否被正确执行和记录”的问题。

具体目标：

1. 为高影响 Skills 建立统一的 gate registry，声明每个 Skill 的输入、schema、脚本门禁和报告产物。
2. 提供一个 Node.js 入口脚本，按 registry 运行现有 JS 门禁，而不是重写各 Skill 的业务检查。
3. 统一 blocking、advisory、usage error 和 internal error 的退出码与报告格式。
4. 读取并报告 `_progress.md` 状态，避免长任务恢复信息被执行者忽略。
5. 将每次 gate 运行结果写入单本小说项目的 `history/gate_reports/`，便于审查和恢复。
6. 保持作者主导：Runner 不自动生成小说正文、不替用户确认、不跨 Phase 推进创作。

## 非目标

- 不实现完整 Skill Runner，不自动执行 `SKILL.md` 的所有 Phase。
- 不调用 LLM，不生成或改写小说正文。
- 不替代 `daily-write` 的人工确认、风格审查和语义评估。
- 不恢复 `src/novel/`、根目录 `scripts/` 或 `novel` CLI。
- 不在本轮引入 npm 依赖或 YAML 解析库。
- 不试图从自然语言 `SKILL.md` 中自动解析所有门禁；v1 使用显式 registry。

## 方案比较

### 方案 A：只保留人工执行脚本

优点是没有新增代码，继续沿用当前流程。缺点是核心问题没有解决：Agent 仍可能漏读 schema、漏跑脚本、漏记录门禁结果，后续维护也无法快速知道某个 Skill 的 gates 是什么。

### 方案 B：轻量 Gate Runner

优点是范围小，复用现有 JS 检查脚本，能把 schema、输入、脚本和报告统一到一个可执行入口。它不会碰创造性生成，也不会改变当前 Skill 的交互节奏。

这是推荐方案。

### 方案 C：完整 Skill Runner

优点是约束最强，可以统一 Phase、`_progress.md`、用户确认点、脚本调用和恢复逻辑。缺点是范围过大，会把当前需求扩大为运行框架重建；在 Skill 合约仍有辅助产物缺口时，完整 Runner 容易把不稳定口径固化。

## 推荐设计

采用方案 B：先实现 `Skill Gate Runner`，为未来完整 Runner 留接口。

### 核心形态

新增共享脚本入口：

```text
.agents/skills/_shared/scripts/run-gates.js
```

新增机器可读 registry：

```text
.agents/skills/_shared/gate-registry.json
```

选择 JSON 而不是 YAML 的原因：这是 runner 内部机器配置，不是小说项目数据；Node.js 内建模块即可解析，避免本轮引入依赖。小说设定和产物仍然继续使用 YAML。

### 命令接口

基础命令：

```bash
node .agents/skills/_shared/scripts/run-gates.js <skill> --project <novels/project_id>
```

示例：

```bash
node .agents/skills/_shared/scripts/run-gates.js design-chapters --project novels/nv_20260701_abcd
node .agents/skills/_shared/scripts/run-gates.js paywall-design --project novels/nv_20260701_abcd
node .agents/skills/_shared/scripts/run-gates.js daily-write --project novels/nv_20260701_abcd --target content/chapter_001.md
```

参数规则：

- `<skill>` 必须存在于 `gate-registry.json`。
- `--project` 指向单本小说项目目录；该目录应包含 `settings/`、`content/` 或 `project.yaml`。
- `--target` 用于正文类门禁，例如 `daily-write`、`golden-chapters`。
- `--report-only` 只输出报告到 stdout，不写入 `history/gate_reports/`。
- `--strict-advisory` 将 advisory 也视为失败，供发布前审查使用。
- `--fix` 允许执行会修改文件的修复类 gate；默认不执行任何会改写项目文件的命令。

退出码：

- `0`：没有 blocking，门禁通过。
- `1`：存在 blocking。
- `2`：参数错误、项目目录错误或 registry 配置错误。
- `3`：脚本执行异常、无法读取文件或 runner 内部错误。

### Registry 合约

`gate-registry.json` 的每个 Skill 条目包含：

```json
{
  "design-chapters": {
    "description": "章节总索引与单章蓝图门禁",
    "schemas": [
      "data/schemas/chapters.schema.yaml",
      "data/schemas/chapter_outline_frontmatter.schema.yaml"
    ],
    "requiredFiles": [
      "settings/chapters_index.yaml"
    ],
    "optionalFiles": [
      "settings/chapter_outlines"
    ],
    "progress": {
      "file": "_progress.md",
      "requiredForLongTask": true
    },
    "gates": [
      {
        "name": "chapters-index",
        "command": [
          "node",
          ".agents/skills/design-chapters/scripts/check-chapters.js",
          "settings/chapters_index.yaml"
        ]
      },
      {
        "name": "chapter-outlines",
        "command": [
          "node",
          ".agents/skills/design-chapters/scripts/check-outlines.js",
          "settings/chapter_outlines"
        ],
        "skipIfMissing": true
      }
    ]
  }
}
```

路径解析规则：

- `command[1]` 中的脚本路径按仓库根目录解析。
- `command` 中的项目产物路径按 `--project` 目录解析。
- `schemas` 按仓库根目录解析，并只检查存在性和可读性。
- `requiredFiles`、`optionalFiles` 按 `--project` 目录解析。

### Report 合约

默认写入：

```text
novels/{project_id}/history/gate_reports/{YYYYMMDD-HHMMSS}-{skill}.yaml
```

报告结构：

```yaml
version: 1
skill: design-chapters
project: novels/nv_20260701_abcd
started_at: "2026-07-01T10:30:00+08:00"
finished_at: "2026-07-01T10:30:02+08:00"
status: pass
summary:
  blocking: 0
  advisory: 1
  skipped: 0
schemas:
  - path: data/schemas/chapters.schema.yaml
    status: present
progress:
  path: _progress.md
  status: present
  current_phase: "5"
gates:
  - name: chapters-index
    command: "node .agents/skills/design-chapters/scripts/check-chapters.js settings/chapters_index.yaml"
    exit_code: 0
    blocking: 0
    advisory: 1
    output:
      - "[advisory] 缺少 stats 字段"
```

报告状态：

- `pass`：所有 gate 无 blocking，且无 runner 内部错误。
- `fail`：至少一个 gate 返回 blocking 或非零业务失败。
- `error`：runner 自身无法完成，例如 registry 无效或项目目录不存在。

### Gate 输出解析

现有 JS 脚本已经统一输出 `[blocking]`、`[advisory]`。Runner v1 不要求脚本改成 JSON 输出，而是按行解析：

- 行以 `[blocking]` 开头，计入 blocking。
- 行以 `[advisory]` 开头，计入 advisory。
- exit code 非 0 但未解析到 blocking 时，记录为 internal gate failure，并计入 blocking。
- exit code 为 0 且解析到 blocking 时，仍视为 blocking，防止脚本退出码与输出不一致。

这样可以复用当前脚本，同时给未来 JSON 输出留出升级空间。

### 只读门禁与修复类门禁

Runner 默认必须是只读的。registry 中每个 gate 可以标记：

- `mode: "check"`：只读检查，默认执行。
- `mode: "fix"`：可能修改文件，例如标点归一化，只有传入 `--fix` 才执行。

如果没有标记，按 `mode: "check"` 处理。这样可以把 `daily-write` 的确定性检查纳入统一入口，同时避免 runner 在用户只想审查时悄悄改写正文。

## v1 支持范围

第一版支持高影响、已有确定性脚本的 Skill：

| Skill | v1 支持方式 | 说明 |
|-------|-------------|------|
| `design-outline` | `check-outline.js`、`check-pacing.js` | 检查大纲和节奏产物。 |
| `design-chapters` | `check-chapters.js`、`check-outlines.js` | 检查章节索引和单章蓝图。 |
| `paywall-design` | `check-paywall.js` | 检查付费切点报告和章节张力。 |
| `golden-chapters` | 显式 `--target` 文件 | 检查前三章结构、AI 味和退化问题。 |
| `daily-write` | 显式 `--target` 文件 | 默认检查单章正文 AI 味和退化问题；标点归一化属于 `--fix` 模式。 |

暂不纳入 v1 的 Skill：

- `scout-topic`、`worldbuilding`、`design-character`：虽然有脚本，但其输入更依赖当前项目阶段；可在 v1.1 补 registry。
- `data-diagnosis`：脚本路径和报告 schema 仍是后续缺口。
- `export-novel`：缺少导出配置 schema 和确定性门禁。
- `review`：主要是 LLM/多视角审查，不适合 v1 以确定性 gate 统一。
- `nm`：外部素材检索，不是项目内产物门禁。

## 与 `_progress.md` 的关系

Runner v1 只读取和报告 `_progress.md`，不自动推进或清理 Phase。

原因：

- 当前各 Skill 的 Phase 仍由用户确认驱动，Runner 无法知道创造性步骤是否真的完成。
- 自动清理 `_progress.md` 可能破坏断点恢复。
- 先报告 progress 状态，就能解决“执行者是否忽略断点”的问题，同时避免过度接管。

未来完整 Skill Runner 可以在 v2 接管：

- `start`：创建 `_progress.md`。
- `phase`：更新 `current_phase`。
- `complete`：在 gate 全部通过后标记完成或清理。

## 错误处理

Runner 遇到以下情况应返回 `2`：

- 未传 `<skill>`。
- `<skill>` 不存在于 registry。
- `--project` 缺失。
- `--project` 目录不存在。
- registry JSON 无法解析。
- registry 中 gate command 为空或格式错误。

Runner 遇到以下情况应返回 `3`：

- 无法读取脚本文件。
- 无法写入报告目录。
- 子进程执行异常。

业务脚本返回 blocking 时，Runner 返回 `1`，并把原始输出完整写入报告。

## 测试策略

实施计划应采用 TDD，小步覆盖：

1. registry 解析：合法 registry 通过，非法 JSON 返回 usage error。
2. 路径解析：仓库脚本路径与项目产物路径分开解析。
3. gate 执行：用现有 schema-contract fixtures 验证正例通过、反例失败。
4. 输出解析：`[blocking]`、`[advisory]`、无标记非零退出码都能被正确统计。
5. 只读默认：未传 `--fix` 时跳过 `mode: "fix"` 的 gate，并在报告中记录 skipped。
6. report 写入：默认写入 `history/gate_reports/`，`--report-only` 不写文件。
7. progress 读取：存在 `_progress.md` 时提取基础字段；不存在时报告 missing 但不阻断，除非 registry 标记必须存在且执行模式要求严格。
8. 回归验证：现有单脚本命令仍可直接运行，Runner 只是统一入口，不破坏原有用法。

## 迁移策略

第一步只新增共享 runner 和 registry，不修改现有 Skill 脚本行为。

第二步在高影响 Skill 的 `SKILL.md` 中补充推荐命令：

```bash
node .agents/skills/_shared/scripts/run-gates.js <skill> --project <project_dir>
```

第三步更新 `.agents/AGENTS.md`，说明 Agent 在完成对应 Skill 的落盘验证时，应优先运行 Gate Runner；如果 runner 不支持该 Skill，再退回 Skill 内声明的脚本命令。

第四步根据使用情况再决定是否扩展到 `data-diagnosis`、`export-novel` 和完整 Skill Runner。

## 成功标准

- 运行一个命令即可执行 `design-chapters`、`paywall-design` 等高影响 Skill 的全部确定性门禁。
- 每次运行都有结构化 gate report，可追踪 blocking/advisory、脚本命令、退出码和原始输出。
- Runner 不生成正文，不自动跨 Phase，不破坏作者确认点。
- 现有单个 JS 检查脚本仍可独立运行。
- 新增测试覆盖正例、反例、报告写入和错误退出码。
- 后续 `writing-plans` 可以把实现拆成小任务，而不需要重新讨论运行模型。

## 风险与约束

- `SKILL.md` 是自然语言文档，v1 不尝试自动解析，避免脆弱正则。
- JSON registry 会产生一个新的维护点；为降低漂移，实施计划应要求 Skill 文档和 registry 同步更新。
- 部分脚本输出不是严格机器格式，v1 只能解析 `[blocking]` 和 `[advisory]` 前缀。
- `daily-write` 与 `golden-chapters` 包含 LLM 语义评估，Runner 只能覆盖确定性脚本部分。
- 修复类脚本可能修改正文，v1 必须默认跳过，只有用户或实施计划显式传入 `--fix` 才能执行。
- `docs/feedback/archive/feedback.md` 是既有未提交修改，不属于本设计和后续实现范围。
