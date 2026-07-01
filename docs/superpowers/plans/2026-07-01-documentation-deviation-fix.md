# 文档偏差修复与 P2/P3 缺口关闭 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复文档偏差 + 关闭 SKILL_CONTRACT_AUDIT 全部 P2/P3 缺口，全量验证通过。

**Architecture:** 4 批交付——文档修复 → Schema/模板 → JS 门禁脚本 → 全量验证。纯文档/Schema/脚本修改，无 Python 代码变更。

**Tech Stack:** Markdown, YAML, Node.js (纯内建模块)

**Spec:** `docs/superpowers/specs/2026-07-01-documentation-deviation-fix-design.md`

---

## Batch 1: 文档修复

### Task 1: 归档 superpowers 历史文档

**Files:**
- Move: `docs/superpowers/` → `docs/archive/superpowers/`
- Modify: `docs/README.md`

- [ ] **Step 1: 创建 archive 目录并移动 superpowers**

```bash
mkdir -p docs/archive
git mv docs/superpowers docs/archive/superpowers
```

- [ ] **Step 2: 更新 docs/README.md**

将 `docs/README.md` 中从"## 工作流产出"到文件末尾（含"## 归档"段落）整体替换为：

```markdown
## 归档

以下内容均为历史产物，**不代表当前主流程**。若与 `.agents/skills/` 或正式文档冲突，以正式文档和 Skill 文件为准。

| 路径 | 说明 |
|------|------|
| `archive/superpowers/specs/` | 历史设计规格文档（含已放弃的 CLI 自动化方向） |
| `archive/superpowers/plans/` | 历史实施计划文档 |
| `archive/superpowers/verification/` | 历史验证报告 |
| `feedback/archive/` | 历史反馈和分析报告 |
```

- [ ] **Step 3: 验证**

```bash
ls docs/archive/superpowers/
# Expected: plans  specs  verification
ls docs/ | grep superpowers
# Expected: 无输出
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "docs(archive): 将 superpowers 历史文档移入 archive 隔离"
```

---

### Task 2: 精简 analysis_report.md

**Files:**
- Modify: `docs/feedback/archive/analysis_report.md`

- [ ] **Step 1: 将文件内容替换为精简版**

用以下内容覆写 `docs/feedback/archive/analysis_report.md`：

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
- [用户手册](../USER_MANUAL.md)
- [需求文档](../REQUIREMENTS.md)
```

- [ ] **Step 2: Commit**

```bash
git add docs/feedback/archive/analysis_report.md
git commit -m "docs(archive): 精简过时的 analysis_report.md"
```

---

### Task 3: 补充 scout_report.yaml 模板

**Files:**
- Create: `templates/default/settings/scout_report.yaml`

- [ ] **Step 1: 创建模板文件**

```yaml
# 选题侦察报告模板
# [R] = 必填字段，[O] = 可选字段
# 由 /scout-topic 生成，后续 Skill 根据 required_elements 动态检查
# 对齐 data/schemas/scout_report.schema.yaml

platform: ""                    # [R] 目标平台（番茄小说、起点、晋江等）
channel: ""                     # [O] 频道（男频/女频）
genre: ""                       # [R] 品类（都市、玄幻、系统、言情等）
target_audience: ""             # [R] 目标读者群体

premise: ""                     # [R] 一句话前提（50字以上的故事概述）
core_hooks: []                  # [O] 核心钩子列表
# 每个钩子包含：
#   name, description, hook_type

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
    type: ""                    # golden_finger / reborn_advantage / meet_cute / conflict / mystery_hook
    description: ""
  structure:
    type: ""                    # 三幕式 / 起承转合 / 英雄之旅
    target_arcs: 1

risks: []                       # [O] 风险提示
# 每条风险包含：
#   type, severity（低/低-中/中/中-高/高）, description, mitigation[]
```

- [ ] **Step 2: Commit**

```bash
git add templates/default/settings/scout_report.yaml
git commit -m "templates: 补充 scout_report.yaml 空模板"
```

---

### Task 4: 修正 data-diagnosis 脚本路径

**Files:**
- Modify: `.agents/skills/data-diagnosis/SKILL.md`

- [ ] **Step 1: 替换短路径**

在 `.agents/skills/data-diagnosis/SKILL.md` 中找到：

```
3. 运行 `scripts/analyze-metrics.js` 解析数据
```

替换为：

```
3. 运行 `.agents/skills/data-diagnosis/scripts/analyze-metrics.js` 解析数据
```

- [ ] **Step 2: Commit**

```bash
git add .agents/skills/data-diagnosis/SKILL.md
git commit -m "fix(data-diagnosis): 修正脚本短路径为完整路径"
```

---

## Batch 2: Schema 与模板新增

### Task 5: 新增 data_diagnosis_report.schema.yaml

**Files:**
- Create: `data/schemas/data_diagnosis_report.schema.yaml`

- [ ] **Step 1: 创建 Schema 文件**

```yaml
# data_diagnosis_report.schema.yaml
# 数据诊断报告 schema
# 路径: novels/{project_id}/data_diagnosis_report.yaml
# 生产 Skill: data-diagnosis
# 消费 Skill: daily-write（可选参考）

# R = 必填, O = 可选

report_date: ""                  # R | 报告生成日期 (YYYY-MM-DD)
platform: ""                     # R | 数据来源平台
project_id: ""                   # R | 关联项目 ID

data_source: ""                  # O | 原始 CSV 文件路径

metrics_summary:                 # O | 总体指标
  total_chapters: 0              # 总章数
  avg_retention_rate: ""         # 平均追读率
  avg_completion_rate: ""        # 平均完读率
  avg_engagement_rate: ""        # 平均互动率

chapter_metrics: []              # O | 逐章指标列表
# - chapter: 0                   # R | 章节号
#   reads: 0                     # O | 阅读数
#   retention_rate: ""           # O | 追读率
#   completion_rate: ""          # O | 完读率
#   engagement_rate: ""          # O | 互动率

anomalies: []                    # O | 异常章节列表
# - chapter: 0                   # R | 章节号
#   type: ""                     # R | 异常类型
#   severity: ""                 # R | P0/P1/P2
#   detail: ""                   # R | 详细说明

recommendations: []              # O | 改进建议列表
# - priority: ""                 # R | 优先级
#   chapter_range: ""            # O | 影响章节范围
#   description: ""              # R | 建议说明
```

- [ ] **Step 2: Commit**

```bash
git add data/schemas/data_diagnosis_report.schema.yaml
git commit -m "schemas: 新增 data_diagnosis_report.schema.yaml"
```

---

### Task 6: 新增 export_config.schema.yaml

**Files:**
- Create: `data/schemas/export_config.schema.yaml`

- [ ] **Step 1: 创建 Schema 文件**

```yaml
# export_config.schema.yaml
# 导出配置 schema
# 路径: novels/{project_id}/export_config.yaml（运行时生成）
# 生产 Skill: export-novel

# R = 必填, O = 可选

format: ""                       # R | 导出格式 (txt / markdown / epub)

chapter_range:                   # O | 导出章节范围
  start: 1                       # 起始章节
  end: null                      # 结束章节，null = 全部

include_metadata: true           # O | 是否包含元信息（书名、作者、目录）

output_dir: "exports"            # O | 输出目录

file_naming: "sequential"        # O | 文件命名规则 (sequential / by_title)

encoding: "utf-8"                # O | 文件编码
```

- [ ] **Step 2: Commit**

```bash
git add data/schemas/export_config.schema.yaml
git commit -m "schemas: 新增 export_config.schema.yaml"
```

---

### Task 7: 新增 golden_chapters_report.md 模板

**Files:**
- Create: `templates/default/golden_chapters_report.md`

- [ ] **Step 1: 创建模板文件**

```markdown
# 黄金三章检查报告

> 生成时间：{timestamp}
> 项目：{project_name}

## 逐章评分

| 章节 | 钩子强度 | AI 味 | 退化 | 结构 | 综合 |
|------|----------|--------|------|------|------|
| 第 1 章 | /5 | /5 | /5 | /5 | /5 |
| 第 2 章 | /5 | /5 | /5 | /5 | /5 |
| 第 3 章 | /5 | /5 | /5 | /5 | /5 |

## 综合结论

- **结果**：{通过 / 需修改 / 需重写}
- **最强章节**：第 N 章
- **最弱章节**：第 N 章

## 修改建议

1. {建议 1}
2. {建议 2}

## 详细备注

{其他需要记录的观察}
```

- [ ] **Step 2: Commit**

```bash
git add templates/default/golden_chapters_report.md
git commit -m "templates: 新增 golden_chapters_report.md 模板"
```

---

### Task 8: 更新 SKILL_CONTRACT_AUDIT.md

**Files:**
- Modify: `docs/SKILL_CONTRACT_AUDIT.md`

- [ ] **Step 1: 更新 data-diagnosis 行的"对齐结论"**

替换为：

```
脚本路径已修正；报告 schema 已新增（`data/schemas/data_diagnosis_report.schema.yaml`）；`check-diagnosis-report.js` 已创建。
```

- [ ] **Step 2: 更新 export-novel 行的"对齐结论"**

替换为：

```
导出配置 schema 已新增（`data/schemas/export_config.schema.yaml`）；`check-export-config.js` 已创建。
```

- [ ] **Step 3: 更新 golden-chapters 行的"对齐结论"**

在现有内容后追加：`golden_chapters_report.md 模板已新增（`templates/default/golden_chapters_report.md`）。`

- [ ] **Step 4: 更新 daily-write 行的门禁脚本**

在门禁脚本列追加：`node .agents/skills/_shared/scripts/check-notes.js settings/notes.yaml`

- [ ] **Step 5: Schema 使用矩阵末尾追加两行**

```markdown
| `data/schemas/data_diagnosis_report.schema.yaml` | `data-diagnosis` | `daily-write`（可选） | 覆盖报告日期、平台、指标、异常、建议 | 已由 `check-diagnosis-report.js` 检查必填字段。 |
| `data/schemas/export_config.schema.yaml` | `export-novel` | 作者、发布平台 | 覆盖格式、章节范围、命名、编码 | 已由 `check-export-config.js` 检查格式枚举和章节范围。 |
```

- [ ] **Step 6: "后续实施建议"末尾追加**

```markdown
6. 已修正 `data-diagnosis` 脚本短路径。
7. 已新增 `data_diagnosis_report.schema.yaml` 和 `check-diagnosis-report.js`。
8. 已新增 `export_config.schema.yaml` 和 `check-export-config.js`。
9. 已新增 `golden_chapters_report.md` 模板。
10. 已新增 `check-notes.js` 共享门禁脚本。
11. 已将 `docs/superpowers/` 移入 `docs/archive/superpowers/`。
12. 已精简 `docs/feedback/archive/analysis_report.md`。
13. 已补充 `templates/default/settings/scout_report.yaml` 模板。
```

- [ ] **Step 7: Commit**

```bash
git add docs/SKILL_CONTRACT_AUDIT.md
git commit -m "docs(audit): 更新 SKILL_CONTRACT_AUDIT 关闭全部 P2/P3 缺口"
```

---

## Batch 3: JS 门禁脚本

### Task 9: 创建 check-notes.js

**Files:**
- Create: `.agents/skills/_shared/scripts/check-notes.js`

- [ ] **Step 1: 创建脚本**

```javascript
#!/usr/bin/env node
'use strict';

// check-notes.js — notes.yaml 结构验证
// Usage: node check-notes.js <notes.yaml>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const notesFile = process.argv[2];
  if (!notesFile) {
    console.error('Usage: node check-notes.js <notes.yaml>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(notesFile), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  // 跳过纯注释或空文件
  const meaningfulLines = content.split('\n').filter(l => l.trim() && !l.trim().startsWith('#'));
  if (meaningfulLines.length === 0) {
    console.log('[advisory] notes.yaml 为空，无结构化数据');
    console.log('\n共 0 个阻塞，1 个建议');
    process.exit(0);
  }

  const findings = [];

  // 检查 1: version 字段
  if (!/^version:\s*\d+/m.test(content)) {
    findings.push({ severity: 'blocking', message: '缺少 version 字段（必须为整数）' });
  }

  // 检查 2: tracking 节点
  if (!/^tracking:\s*$/m.test(content)) {
    findings.push({ severity: 'blocking', message: '缺少 tracking 节点' });
  } else {
    const trackingFields = ['recent_chapters', 'ten_chapter_summaries', 'volume_overview', 'character_states', 'foreshadowing'];
    for (const field of trackingFields) {
      if (!new RegExp(`^\\s+${field}:\\s*`, 'm').test(content)) {
        findings.push({ severity: 'blocking', message: `tracking 缺少 ${field} 字段` });
      }
    }
  }

  // 检查 3: foreshadowing status 枚举
  const foreshadowingSection = extractSection(content, 'foreshadowing');
  if (foreshadowingSection) {
    const statuses = [];
    const pattern = /^\s+status:\s*["']?(\w+)["']?/gm;
    let m;
    while ((m = pattern.exec(foreshadowingSection)) !== null) statuses.push(m[1]);
    const valid = ['open', 'resolved', 'dropped'];
    for (const s of statuses) {
      if (!valid.includes(s)) {
        findings.push({ severity: 'blocking', message: `foreshadowing.status "${s}" 不在允许值中 (open/resolved/dropped)` });
      }
    }

    // 检查 planted_chapter
    const entries = foreshadowingSection.split(/^\s*-\s+/m).filter(s => s.trim());
    for (let i = 0; i < entries.length; i++) {
      if (!/planted_chapter:\s*\d+/.test(entries[i])) {
        findings.push({ severity: 'blocking', message: `foreshadowing 第 ${i + 1} 项缺少 planted_chapter` });
      }
    }
  }

  // 检查 4: character_states name 非空
  const charSection = extractSection(content, 'character_states');
  if (charSection) {
    const entries = charSection.split(/^\s*-\s+/m).filter(s => s.trim());
    for (let i = 0; i < entries.length; i++) {
      if (!/name:\s*["']?[^\s"']+/.test(entries[i])) {
        findings.push({ severity: 'blocking', message: `character_states 第 ${i + 1} 项缺少 name` });
      }
    }
  }

  // 检查 5: preferences 节点 (advisory)
  if (!/^preferences:\s*$/m.test(content)) {
    findings.push({ severity: 'advisory', message: '缺少 preferences 节点（style_notes / banned_settings / pending_confirmations）' });
  }

  printResults(findings);
}

function extractSection(content, key) {
  const lines = content.split('\n');
  const startIdx = lines.findIndex(l => new RegExp(`^\\s+${key}:\\s*`).test(l));
  if (startIdx === -1) return '';

  const section = [];
  const indent = lines[startIdx].match(/^(\s*)/)[1].length;
  for (let i = startIdx + 1; i < lines.length; i++) {
    if (lines[i].trim() === '' || lines[i].trim().startsWith('#')) continue;
    const currentIndent = lines[i].match(/^(\s*)/)[1].length;
    if (currentIndent <= indent && lines[i].trim()) break;
    section.push(lines[i]);
  }
  return section.join('\n');
}

function printResults(findings) {
  if (findings.length === 0) {
    console.log('✓ notes.yaml 结构检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

main();
```

- [ ] **Step 2: 设置可执行权限并试跑**

```bash
chmod +x .agents/skills/_shared/scripts/check-notes.js
node .agents/skills/_shared/scripts/check-notes.js novels/nv_20260625_00t3/settings/notes.yaml || true
# Expected: 多个 blocking（现有 notes.yaml 用旧格式，缺少 version/tracking/preferences）
```

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/_shared/scripts/check-notes.js
git commit -m "scripts: 新增 check-notes.js 共享门禁脚本"
```

---

### Task 10: 创建 check-diagnosis-report.js

**Files:**
- Create: `.agents/skills/data-diagnosis/scripts/check-diagnosis-report.js`

- [ ] **Step 1: 创建脚本**

```javascript
#!/usr/bin/env node
'use strict';

// check-diagnosis-report.js — 数据诊断报告结构验证
// Usage: node check-diagnosis-report.js <data_diagnosis_report.yaml>

const fs = require('fs');
const path = require('path');

function main() {
  const reportFile = process.argv[2];
  if (!reportFile) {
    console.error('Usage: node check-diagnosis-report.js <data_diagnosis_report.yaml>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(reportFile), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  const meaningfulLines = content.split('\n').filter(l => l.trim() && !l.trim().startsWith('#'));
  if (meaningfulLines.length === 0) {
    console.log('[advisory] 报告文件为空');
    console.log('\n共 0 个阻塞，1 个建议');
    process.exit(0);
  }

  const findings = [];

  if (!/^report_date:\s*["']?\d{4}-\d{2}-\d{2}["']?\s*$/m.test(content))
    findings.push({ severity: 'blocking', message: '缺少 report_date 或格式不正确 (YYYY-MM-DD)' });

  if (!/^platform:\s*["']?[^\s"']+["']?\s*$/m.test(content))
    findings.push({ severity: 'blocking', message: '缺少 platform' });

  if (!/^project_id:\s*["']?[^\s"']+["']?\s*$/m.test(content))
    findings.push({ severity: 'blocking', message: '缺少 project_id' });

  // anomalies severity 枚举
  const anomaliesSection = extractSection(content, 'anomalies');
  if (anomaliesSection) {
    const entries = anomaliesSection.split(/^\s*-\s+/m).filter(s => s.trim());
    const validSeverities = ['P0', 'P1', 'P2'];
    for (let i = 0; i < entries.length; i++) {
      const sevMatch = entries[i].match(/severity:\s*["']?(\w+)["']?/);
      if (sevMatch && !validSeverities.includes(sevMatch[1])) {
        findings.push({ severity: 'advisory', message: `anomalies[${i + 1}] severity "${sevMatch[1]}" 不在允许值中` });
      }
    }
  }

  // recommendations priority
  const recsSection = extractSection(content, 'recommendations');
  if (recsSection) {
    const entries = recsSection.split(/^\s*-\s+/m).filter(s => s.trim());
    for (let i = 0; i < entries.length; i++) {
      if (!/priority:\s*/.test(entries[i])) {
        findings.push({ severity: 'advisory', message: `recommendations[${i + 1}] 缺少 priority` });
      }
    }
  }

  printResults(findings);
}

function extractSection(content, key) {
  const lines = content.split('\n');
  const startIdx = lines.findIndex(l => new RegExp(`^${key}:\\s*`).test(l));
  if (startIdx === -1) return '';
  const section = [];
  for (let i = startIdx + 1; i < lines.length; i++) {
    if (lines[i].trim() === '' || lines[i].trim().startsWith('#')) continue;
    if (/^[A-Za-z_][\w-]*:\s*/.test(lines[i])) break;
    section.push(lines[i]);
  }
  return section.join('\n');
}

function printResults(findings) {
  if (findings.length === 0) {
    console.log('✓ 数据诊断报告结构检查通过');
    process.exit(0);
  }
  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

main();
```

- [ ] **Step 2: 设置权限并试跑**

```bash
chmod +x .agents/skills/data-diagnosis/scripts/check-diagnosis-report.js

# 正常输入
cat > /tmp/test_report.yaml << 'EOF'
report_date: "2026-07-01"
platform: "起点中文网"
project_id: "nv_20260625_00t3"
anomalies:
  - chapter: 12
    type: "追读率骤降"
    severity: P1
    detail: "下降 18%"
recommendations:
  - priority: "高"
    chapter_range: "10-15"
    description: "收紧节奏"
EOF
node .agents/skills/data-diagnosis/scripts/check-diagnosis-report.js /tmp/test_report.yaml
# Expected: ✓ 检查通过

# 异常输入
cat > /tmp/test_bad.yaml << 'EOF'
report_date: "bad"
anomalies:
  - severity: P9
EOF
node .agents/skills/data-diagnosis/scripts/check-diagnosis-report.js /tmp/test_bad.yaml
# Expected: blocking（缺 platform/project_id/date 格式错）+ advisory（P9 不合法）

rm -f /tmp/test_report.yaml /tmp/test_bad.yaml
```

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/data-diagnosis/scripts/check-diagnosis-report.js
git commit -m "scripts: 新增 check-diagnosis-report.js 门禁脚本"
```

---

### Task 11: 创建 check-export-config.js

**Files:**
- Create: `.agents/skills/export-novel/scripts/check-export-config.js`

- [ ] **Step 1: 创建目录和脚本**

```bash
mkdir -p .agents/skills/export-novel/scripts
```

```javascript
#!/usr/bin/env node
'use strict';

// check-export-config.js — 导出配置结构验证
// Usage: node check-export-config.js <export_config.yaml>

const fs = require('fs');
const path = require('path');

function main() {
  const configFile = process.argv[2];
  if (!configFile) {
    console.error('Usage: node check-export-config.js <export_config.yaml>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(configFile), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  const findings = [];

  // format 必填且为枚举值
  const formatMatch = content.match(/^format:\s*["']?(\w+)["']?\s*$/m);
  if (!formatMatch) {
    findings.push({ severity: 'blocking', message: '缺少 format 字段' });
  } else {
    const validFormats = ['txt', 'markdown', 'epub'];
    if (!validFormats.includes(formatMatch[1])) {
      findings.push({ severity: 'blocking', message: `format "${formatMatch[1]}" 不在允许值中 (txt/markdown/epub)` });
    }
  }

  // chapter_range.start >= 1
  const startMatch = content.match(/^\s+start:\s*(\d+)/m);
  if (startMatch && parseInt(startMatch[1]) < 1) {
    findings.push({ severity: 'blocking', message: `chapter_range.start (${startMatch[1]}) 必须 >= 1` });
  }

  // chapter_range.end >= start
  const endMatch = content.match(/^\s+end:\s*(\d+)/m);
  if (startMatch && endMatch) {
    const s = parseInt(startMatch[1]), e = parseInt(endMatch[1]);
    if (e < s) findings.push({ severity: 'blocking', message: `chapter_range.end (${e}) < start (${s})` });
  }

  // encoding (advisory)
  const encMatch = content.match(/^encoding:\s*["']?([\w-]+)["']?\s*$/m);
  if (encMatch && encMatch[1].toLowerCase() !== 'utf-8') {
    findings.push({ severity: 'advisory', message: `encoding "${encMatch[1]}" 非标准，推荐 utf-8` });
  }

  // file_naming (advisory)
  const namingMatch = content.match(/^file_naming:\s*["']?(\w+)["']?\s*$/m);
  if (namingMatch) {
    const valid = ['sequential', 'by_title'];
    if (!valid.includes(namingMatch[1])) {
      findings.push({ severity: 'advisory', message: `file_naming "${namingMatch[1]}" 不在推荐值中 (sequential/by_title)` });
    }
  }

  printResults(findings);
}

function printResults(findings) {
  if (findings.length === 0) {
    console.log('✓ 导出配置检查通过');
    process.exit(0);
  }
  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

main();
```

- [ ] **Step 2: 设置权限并试跑**

```bash
chmod +x .agents/skills/export-novel/scripts/check-export-config.js

# 正常输入
cat > /tmp/test_export.yaml << 'EOF'
format: "epub"
chapter_range:
  start: 1
  end: 50
include_metadata: true
output_dir: "exports"
file_naming: "sequential"
encoding: "utf-8"
EOF
node .agents/skills/export-novel/scripts/check-export-config.js /tmp/test_export.yaml
# Expected: ✓ 检查通过

# 异常输入
cat > /tmp/test_export_bad.yaml << 'EOF'
format: "pdf"
chapter_range:
  start: 10
  end: 5
encoding: "gbk"
file_naming: "random"
EOF
node .agents/skills/export-novel/scripts/check-export-config.js /tmp/test_export_bad.yaml
# Expected: blocking (pdf 不合法, end < start) + advisory (gbk, random)

rm -f /tmp/test_export.yaml /tmp/test_export_bad.yaml
```

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/export-novel/scripts/check-export-config.js
git commit -m "scripts: 新增 check-export-config.js 门禁脚本"
```

---

## Batch 4: 全量验证

### Task 12: 全量验证

- [ ] **Step 1: 目录结构验证**

```bash
echo "=== archive ==="
ls docs/archive/superpowers/
echo "=== templates/settings ==="
ls templates/default/settings/
echo "=== templates 根 ==="
ls templates/default/*.md 2>/dev/null
echo "=== schemas ==="
ls data/schemas/ | grep -E "diagnosis|export"
echo "=== docs 根（无 superpowers）==="
ls docs/ | grep superpowers && echo "FAIL" || echo "OK"
```

- [ ] **Step 2: 脚本试跑**

```bash
echo "=== check-notes.js ==="
node .agents/skills/_shared/scripts/check-notes.js novels/nv_20260625_00t3/settings/notes.yaml || true
echo ""
echo "=== check-diagnosis-report.js (空文件) ==="
echo "# empty" | node .agents/skills/data-diagnosis/scripts/check-diagnosis-report.js /dev/stdin || true
echo ""
echo "=== check-export-config.js (空文件) ==="
echo "format: txt" | node .agents/skills/export-novel/scripts/check-export-config.js /dev/stdin || true
```

- [ ] **Step 3: 路径残留检查**

```bash
grep -rn "^\s*node scripts/" .agents/skills/*/SKILL.md || echo "OK: 无短路径残留"
grep -rn "^\s*scripts/" .agents/skills/*/SKILL.md | grep -v ".agents/skills/" || echo "OK: 无裸短路径"
```

- [ ] **Step 4: analysis_report.md 行数**

```bash
wc -l docs/feedback/archive/analysis_report.md
# Expected: ~20 行
```

- [ ] **Step 5: git log 确认**

```bash
git log --oneline -12
```
