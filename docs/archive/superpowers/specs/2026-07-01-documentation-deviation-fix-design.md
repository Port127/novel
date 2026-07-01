# 文档偏差修复与 P2/P3 缺口关闭 设计文档

> 日期：2026-07-01
> 范围：文档偏差修复 + SKILL_CONTRACT_AUDIT 中 P2/P3 缺口全量关闭
> 方法：方案 A（按类型分 4 批交付）

## 一、问题背景

经全量文档审查，发现以下两类问题：

**A. 文档偏差（6 项，其中 1 项误报）**

| # | 偏差 | 级别 |
|---|------|------|
| 1 | `docs/superpowers/` 38 篇历史文档混在正式文档目录 | 中 |
| 2 | ~~`REQUIREMENTS.md` 漏列 `review`~~ | 误报，已取消 |
| 3 | `templates/default/settings/` 缺 `scout_report.yaml` 模板 | 低 |
| 4 | `data-diagnosis/SKILL.md` 脚本短路径 | 中 |
| 5 | `feedback/archive/analysis_report.md` 过时且误导 | 中 |
| 6 | `SKILL_CONTRACT_AUDIT.md` 需更新关闭项 | 低 |

**B. SKILL_CONTRACT_AUDIT 未关闭的 P2/P3 缺口**

| # | 缺口 | 优先级 | 类型 |
|---|------|--------|------|
| P2-1 | `data-diagnosis` 缺少报告 schema | P2 | Schema |
| P2-2 | `export-novel` 缺少导出配置 schema | P2 | Schema |
| P2-3 | `notes.yaml` 缺少脚本门禁 | P2 | JS 脚本 |
| P3-1 | `golden_chapters_report` 结构不稳定 | P3 | 模板 |
| P3-2 | 辅助 Skill 短脚本路径未统一清理 | P3 | 文档 |

## 二、成功标准

- 所有交付物落盘（文档、Schema、模板、JS 脚本）
- 用现有项目数据 `novels/nv_20260625_00t3/` 试跑所有新 JS 脚本，确认 0 报错（或合理 advisory）
- `SKILL_CONTRACT_AUDIT.md` 中所有 P2/P3 项标记为已关闭

## 三、总体架构

```
Batch 1: 文档修复        ← 无依赖
    ↓
Batch 2: Schema + 模板   ← 依赖 Batch 1（归档后改 README 引用）
    ↓
Batch 3: JS 门禁脚本     ← 依赖 Batch 2（脚本校验新 schema 结构）
    ↓
Batch 4: 全量验证        ← 依赖 Batch 1-3
```

## 四、Batch 1：文档修复

### 4.1 superpowers 归档

**操作**：`docs/superpowers/` → `docs/archive/superpowers/`

**`docs/README.md` 变更**：
- 删除"工作流产出"段落
- 在"归档"段新增 `archive/superpowers/` 条目
- 归档段统一声明："不代表当前主流程，与 `.agents/skills/` 冲突时以 Skill 为准"

### 4.2 analysis_report.md 精简

将原 248 行内容替换为 ~20 行：
- 头部 WARNING 保留
- 正文：摘要（旧方向已放弃）+ 当前文档导航链接
- 不删除文件，保留 git 历史

### 4.3 scout_report.yaml 模板

新建 `templates/default/settings/scout_report.yaml`：
- 字段与 `data/schemas/scout_report.schema.yaml` 的 required 字段对齐：`platform`、`genre`、`target_audience`、`premise`、`recommended_tags`
- 风格与现有模板一致：`[R]`/`[O]` 标注 + 中文注释
- 包含 `required_elements` 空结构（品类感知的必要元素声明）

### 4.4 data-diagnosis 路径修正

`.agents/skills/data-diagnosis/SKILL.md` 第 35 行：
- `scripts/analyze-metrics.js` → `.agents/skills/data-diagnosis/scripts/analyze-metrics.js`

### 4.5 辅助 Skill 短脚本路径统一清理

经检查，仅 `data-diagnosis` 存在短路径问题。其他辅助 Skill（`review`、`stock-check`、`export-novel`、`feature-planning`、`refactor-planning`、`code-review-change`、`commit-msg`）均无 `scripts/` 短路径引用。本项与 4.4 合并处理。

## 五、Batch 2：Schema 与模板新增

### 5.1 `data_diagnosis_report.schema.yaml`

**位置**：`data/schemas/data_diagnosis_report.schema.yaml`
**生产 Skill**：`data-diagnosis`
**消费 Skill**：`daily-write`（可选参考）

核心字段设计：

```yaml
type: object
required: [report_date, platform, project_id]
properties:
  report_date:        # R | 报告生成日期
  platform:           # R | 数据来源平台
  project_id:         # R | 项目 ID
  data_source:        # O | 原始 CSV 文件路径
  metrics_summary:    # O | 总体指标
    total_chapters:       # 总章数
    avg_retention_rate:   # 平均追读率
    avg_completion_rate:  # 平均完读率
    avg_engagement_rate:  # 平均互动率
  chapter_metrics:    # O | 逐章指标列表
    # - chapter, reads, retention_rate, completion_rate, engagement_rate
  anomalies:          # O | 异常章节列表
    # - chapter, type, severity, detail
  recommendations:    # O | 改进建议列表
    # - priority, chapter_range, description
```

### 5.2 `export_config.schema.yaml`

**位置**：`data/schemas/export_config.schema.yaml`
**生产 Skill**：`export-novel`

核心字段设计：

```yaml
type: object
required: [format]
properties:
  format:             # R | 导出格式
    enum: [txt, markdown, epub]
  chapter_range:      # O | 导出章节范围
    start: 1
    end: null         # null = 全部
  include_metadata:   # O | 是否包含元信息
  output_dir:         # O | 输出目录
  file_naming:        # O | 文件命名规则
    enum: [sequential, by_title]
  encoding:           # O | 文件编码
    default: utf-8
```

### 5.3 `golden_chapters_report.md` 模板

**位置**：`templates/default/golden_chapters_report.md`

结构：
- 标题 + 检查时间
- 逐章评分表（钩子强度 / AI 味 / 退化 / 结构 / 综合）
- 综合结论（通过 / 需修改 / 需重写）
- 修改建议列表

### 5.4 SKILL_CONTRACT_AUDIT 更新

- `data-diagnosis` 行的脚本路径和报告 schema 标记已关闭
- `export-novel` 行的导出配置 schema 标记已关闭
- `golden_chapters_report` 模板标记已关闭
- `notes.yaml` 脚本门禁标记已关闭
- Schema 使用矩阵新增 `data_diagnosis_report.schema.yaml`、`export_config.schema.yaml`
- "后续实施建议"追加本轮完成项

## 六、Batch 3：JS 门禁脚本

### 6.1 `check-notes.js`

**位置**：`.agents/skills/_shared/scripts/check-notes.js`
**输入**：`settings/notes.yaml`
**调用方式**：`node .agents/skills/_shared/scripts/check-notes.js settings/notes.yaml`

检查项：
| 检查 | 级别 | 说明 |
|------|------|------|
| `version` 字段存在 | blocking | 必须为整数 |
| `tracking` 节点存在 | blocking | 必须包含 5 个子字段 |
| `foreshadowing[].status` 枚举 | blocking | 必须为 open/resolved/dropped |
| `foreshadowing[].planted_chapter` 存在 | blocking | 伏笔必须有埋设章节 |
| `character_states[].name` 非空 | blocking | 角色状态必须有角色名 |
| `preferences` 节点存在 | advisory | 可以暂时为空 |

风格与 `check-paywall.js` 一致：纯 Node.js、无外部依赖、stdout 输出 `[blocking]/[advisory]` 格式、exit code 区分通过/失败。

### 6.2 `check-diagnosis-report.js`

**位置**：`.agents/skills/data-diagnosis/scripts/check-diagnosis-report.js`
**输入**：`data_diagnosis_report.yaml`
**调用方式**：`node .agents/skills/data-diagnosis/scripts/check-diagnosis-report.js <report.yaml>`

检查项：
| 检查 | 级别 | 说明 |
|------|------|------|
| `report_date` 存在 | blocking | 必须为日期字符串 |
| `platform` 非空 | blocking | 数据来源平台 |
| `project_id` 非空 | blocking | 关联项目 |
| `anomalies[].severity` 枚举 | advisory | P0/P1/P2 |
| `recommendations[].priority` 存在 | advisory | 建议应有优先级 |

### 6.3 `check-export-config.js`

**位置**：`.agents/skills/export-novel/scripts/check-export-config.js`
**输入**：导出配置 YAML 文件
**调用方式**：`node .agents/skills/export-novel/scripts/check-export-config.js <config.yaml>`

检查项：
| 检查 | 级别 | 说明 |
|------|------|------|
| `format` 存在且为枚举值 | blocking | txt/markdown/epub |
| `chapter_range.start` ≥ 1 | blocking | 起始章节有效 |
| `chapter_range.end` ≥ start | blocking | 结束章节 ≥ 起始 |
| `encoding` 有效 | advisory | 默认 utf-8 |
| `file_naming` 为枚举值 | advisory | sequential/by_title |

## 七、Batch 4：全量验证

验证策略：
1. **目录结构检查**：确认归档目录正确、模板齐全
2. **Schema 一致性**：新 Schema 字段与模板/Skill 引用匹配
3. **脚本试跑**：
   - `check-notes.js`：用 `novels/nv_20260625_00t3/settings/notes.yaml` 试跑（如不存在则用模板生成临时文件）
   - `check-diagnosis-report.js`：用模板生成临时 YAML 试跑
   - `check-export-config.js`：用模板生成临时 YAML 试跑
4. **路径引用检查**：grep 所有 `SKILL.md` 确认无残留短路径
5. **文档交叉验证**：确认 `docs/README.md` 归档段引用正确

## 八、交付物清单

| 批次 | 文件 | 操作 |
|------|------|------|
| 1 | `docs/superpowers/` → `docs/archive/superpowers/` | 移动 |
| 1 | `docs/README.md` | 修改 |
| 1 | `docs/feedback/archive/analysis_report.md` | 精简 |
| 1 | `templates/default/settings/scout_report.yaml` | 新建 |
| 1 | `.agents/skills/data-diagnosis/SKILL.md` | 修改 |
| 2 | `data/schemas/data_diagnosis_report.schema.yaml` | 新建 |
| 2 | `data/schemas/export_config.schema.yaml` | 新建 |
| 2 | `templates/default/golden_chapters_report.md` | 新建 |
| 2 | `docs/SKILL_CONTRACT_AUDIT.md` | 修改 |
| 3 | `.agents/skills/_shared/scripts/check-notes.js` | 新建 |
| 3 | `.agents/skills/data-diagnosis/scripts/check-diagnosis-report.js` | 新建 |
| 3 | `.agents/skills/export-novel/scripts/check-export-config.js` | 新建 |
| 4 | 验证报告 | 生成 |

## 九、风险与约束

- **notes.yaml 门禁**：现有项目可能还没有 `notes.yaml` 数据，脚本需优雅处理文件不存在的情况
- **data-diagnosis 报告**：`data-diagnosis` 主要输出是 CSV 解析结果，YAML 报告是新增能力，脚本需兼容空报告
- **export-novel 脚本目录**：`export-novel` 当前无 `scripts/` 目录，需新建
