# Skill 依赖图

> 完整的 skill 间调用关系和数据流向。概览版见 [GUIDE.md](../GUIDE.md) §7。

---

## 1. 全局调用关系图

```mermaid
graph LR
    %% ========== Pipeline 层 ==========
    subgraph Pipelines
        OB["🔄 outline-bootstrap"]
        OP["🔄 outline-polish"]
        SC["🔄 setting-consolidate"]
        CK["🔄 chapter-kickoff"]
        DP["🔄 draft-polish"]
        CG["🔄 compliance-gate"]
        CTG["🔄 continuity-gate"]
        NT["🔄 note-triage"]
    end

    %% ========== 章节领域 ==========
    subgraph 章节
        CC["chapter-create"]
        CU["chapter-update"]
        CD["chapter-draft"]
        CR["chapter-review"]
        CMP["chapter-compare"]
        CE_X["chapter-export"]
        CB["chapter-board"]
    end

    %% ========== 角色领域 ==========
    subgraph 角色
        CA["character-add"]
        CE["character-edit"]
        CQ["character-query"]
    end

    %% ========== 关系领域 ==========
    subgraph 关系
        RA["relationship-add"]
        RL["relationship-log"]
        RC["relationship-check"]
        RE["relationship-evolution"]
        RM["relationship-map"]
    end

    %% ========== 大纲领域 ==========
    subgraph 大纲
        PI["plot-init"]
        PA["plot-add"]
        PE["plot-edit"]
        PQ["plot-query"]
        PR["plot-review"]
        PS["plot-suggest"]
    end

    %% ========== 钩子领域 ==========
    subgraph 钩子
        HA["hook-add"]
        HQ["hook-query"]
        HR["hook-resolve"]
    end

    %% ========== 世界观领域 ==========
    subgraph 世界观
        SA["setting-add"]
        SE["setting-edit"]
        SCA["scene-add"]
        WR["worldbuilding-review"]
    end

    %% ========== 时间线领域 ==========
    subgraph 时间线
        TA["timeline-add"]
        TC["timeline-check"]
        TV["timeline-view"]
    end

    %% ========== 质量领域 ==========
    subgraph 质量
        AAC["anti-ai-check"]
        AAR["anti-ai-rewrite"]
        VC["voice-check"]
        CON["consistency-check"]
        SAU["style-audit"]
        SCR["style-create"]
        SL["style-list"]
        RW["rewrite"]
    end

    %% ========== 素材与合规 ==========
    subgraph 素材合规
        DI["draft-ingest"]
        MS["material-search"]
        MA["material-apply"]
        MM["material-manage"]
        IL["inspiration-log"]
        IC["inspiration-check"]
        IR["inspiration-report"]
    end

    %% ========== 项目管理 ==========
    subgraph 项目管理
        NI["novel-init"]
        NE_S["novel-edit"]
        NLS["novel-list"]
        NSW["novel-switch"]
        NS["novel-status"]
        ND["novel-doctor"]
        NK["novel-kpi"]
        PRI["project-reindex"]
        PWR["project-weekly-report"]
    end

    %% ===== Pipeline → Atomic 调用关系 =====
    OB -->|调用| DI
    OB -->|调用| SA
    OB -->|调用| SC
    OB -->|调用| CA

    OP -->|调用| PR
    OP -->|调用| WR
    OP -->|调用| PE
    OP -->|调用| PA
    OP -->|调用| SE
    OP -->|调用| SA

    SC -->|调用| SE

    CK -->|调用| CC
    CK -->|调用| CU
    CK -->|调用| PA

    DP -->|调用| CR
    DP -->|调用| VC
    DP -->|调用| AAC
    DP -->|调用| AAR
    DP -->|调用| CU

    CG -->|调用| IL
    CG -->|调用| IC
    CG -->|调用| IR

    CTG -->|调用| RC
    CTG -->|调用| TC

    NT -->|调用| SA
    NT -->|调用| CA
    NT -->|调用| CE
    NT -->|调用| PA
    NT -->|调用| TA
    NT -->|调用| RA
    NT -->|调用| RL

    %% ===== Atomic → Atomic 调用关系 =====
    CD -->|调用| CU
    CR -->|提示| HA
    CR -->|提示| HR
    SE -->|evolve| SA
    IC -->|提示| IL
```

---

## 2. 协议嵌入关系

哪些 skill 内嵌了哪些协议：

```mermaid
graph TD
    subgraph "协议 Protocols"
        P_DP["draft-primacy<br/>草稿优先"]
        P_NR["name-resolution<br/>名字解析"]
        P_FE["from-extraction<br/>来源提取"]
        P_PF["preflight-integrity<br/>预检完整性"]
        P_OJ["operation-journal<br/>操作日志"]
        P_SL["style-lifecycle<br/>风格生命周期"]
        P_PE["post-edit-impact-scan<br/>编辑后扫描"]
        P_CS["chapter-scope-guard<br/>章节容量"]
        P_CA["chapter-auto-inference<br/>章节推断"]
        P_EG["eval-gate<br/>评估闸门"]
        P_CB["context-budget<br/>上下文预算"]
    end

    CD["chapter-draft"] -.-> P_NR & P_PF & P_OJ & P_CS & P_CA
    CU["chapter-update"] -.-> P_PF & P_SL & P_CA
    CK["pipeline-chapter-kickoff"] -.-> P_PF & P_OJ & P_CS
    DP_P["pipeline-draft-polish"] -.-> P_PF & P_SL & P_DP
    CE["character-edit"] -.-> P_NR & P_PE
    SE["setting-edit"] -.-> P_PE
    CA["character-add"] -.-> P_NR & P_FE
    SA["setting-add"] -.-> P_FE
    PA["plot-add"] -.-> P_FE
    DI["draft-ingest"] -.-> P_FE & P_DP
    AAR["anti-ai-rewrite"] -.-> P_NR & P_CA
    CR["chapter-review"] -.-> P_CA
    AAC["anti-ai-check"] -.-> P_CA
    VC["voice-check"] -.-> P_CA
    CON["consistency-check"] -.-> P_DP
```

---

## 3. 数据文件读写矩阵

### 3.1 核心数据文件 → 哪些 skill 会写它

| 数据文件 | 写入者 |
|----------|--------|
| `chapters/{id}.md` | chapter-create, chapter-draft, anti-ai-rewrite, hook-add, hook-resolve |
| `chapters/index.yaml` | chapter-create, chapter-update, chapter-draft, hook-add, hook-resolve |
| `characters/{name}.yaml` | character-add, character-edit, relationship-add, project-reindex |
| `characters/character_index.yaml` | character-add, character-edit, project-reindex |
| `characters/relations.yaml` | relationship-add, relationship-log, project-reindex |
| `characters/relation_events.yaml` | relationship-log |
| `plot/outline.md` | plot-init, plot-add, plot-edit, project-reindex |
| `plot/outline.yaml` | plot-init, plot-edit, hook-add, hook-resolve |
| `worldbuilding/entries/*.yaml` | setting-add, setting-edit, project-reindex |
| `worldbuilding/worldbuilding.yaml` | setting-add, setting-edit, project-reindex |
| `worldbuilding/setting.md` | setting-edit, pipeline-outline-bootstrap, pipeline-setting-consolidate |
| `timeline/main.yaml` | timeline-add |
| `.novel/state.yaml` | novel-init, novel-edit, chapter-create, chapter-update, plot-add, plot-edit, character-add, character-edit, setting-add, setting-edit, hook-add, hook-resolve, relationship-add, relationship-log, timeline-add, draft-ingest, pipeline-outline-bootstrap, pipeline-setting-consolidate, scene-add |
| `.novel/meta.yaml` | novel-init, novel-edit, chapter-create |
| `.novel/ops_log.yaml` | chapter-draft, pipeline-chapter-kickoff |
| `ingestion_brief.md` | draft-ingest |
| `shared/styles/templates.yaml` | style-create |
| `compliance/inspiration_log.yaml` | inspiration-log |
| `compliance/risk_report.yaml` | inspiration-check |
| `quality/ai_trace_report.yaml` | anti-ai-check |
| `scenes/*.yaml` | scene-add |
| `.novel/materials.yaml` | material-manage |

### 3.2 高频读取文件

被 10+ 个 skill 读取的文件（改动时影响面大）：

| 文件 | 读取者数量 | 说明 |
|------|-----------|------|
| `chapters/index.yaml` | **20+** | 几乎所有章节/大纲/检查类 skill 都读 |
| `.novel/state.yaml` | **15+** | 项目状态，管理和诊断类 skill 必读 |
| `characters/*.yaml` | **15+** | 角色档案，写作和检查类 skill 必读 |
| `plot/outline.md` | **12+** | 大纲，写作和审查类 skill 必读 |
| `worldbuilding/entries/*.yaml` | **10+** | 设定条目，一致性检查和写作 skill 必读 |
| `characters/relations.yaml` | **10+** | 关系图谱，写作和关系检查类 skill 必读 |

---

## 4. 典型工作流的调用链追踪

### 4.1 从零到发布第一章

```
用户: "我有个故事想法"
    │
    ▼
/novel-init "书名"
    │ 写: projects/书名/ 全部目录骨架
    ▼
/draft-ingest 草稿.txt
    │ 读: 草稿.txt
    │ 写: ingestion_brief.md
    ▼
/pipeline-outline-bootstrap
    │
    ├─► /setting-add ×N          写: worldbuilding/entries/*.yaml
    ├─► /pipeline-setting-consolidate
    │   └─► /setting-edit ×N     写: worldbuilding/entries/*.yaml
    ├─► /character-add ×N        写: characters/*.yaml
    │
    │ (用户确认大纲)
    │
    └─► 生成 plot/outline.md     写: plot/outline.md + outline.yaml
        │
        ▼
/pipeline-chapter-kickoff ch001
    │
    │ [preflight-integrity] ← 检查引用链
    │ [operation-journal]   ← 记录 in_progress
    │
    ├─► /chapter-create ch001    写: chapters/ch001.md, index.yaml
    ├─► /chapter-update ch001    写: index.yaml (元数据)
    ├─► /plot-add ch001 "场景"   写: chapters/ch001.md (场景大纲)
    │
    │ [operation-journal]   ← 更新 completed
    ▼
/chapter-draft ch001
    │
    │ [preflight-integrity] ← 预检
    │ [name-resolution]     ← 确定称呼
    │ [chapter-scope-guard] ← 容量检查
    │
    │ 读: outline, 角色卡, 设定, 时间线, 前章
    │ 写: chapters/ch001.md (正文), ops_log.yaml
    │
    ├─► /chapter-update ch001    写: index.yaml (status → draft)
    ▼
/pipeline-draft-polish ch001
    │
    │ [preflight-integrity]
    │
    ├─► /chapter-review ch001    (结构审查报告)
    ├─► /voice-check ch001       (声音检查报告)
    ├─► /anti-ai-check ch001     写: quality/ai_trace_report.yaml
    ├─► /anti-ai-rewrite ch001   写: chapters/ch001.md (改写)
    │   [name-resolution] ← 保留原有称呼
    │
    │ [style-lifecycle] ← 漂移检测
    │ [draft-primacy]   ← 冲突检测
    │ [eval-gate]       ← 闸门检查（分数 < 阈值则阻断）
    │
    └─► /chapter-update ch001    写: index.yaml (status → revise)（需闸门通过或 --force）
        │
        ▼
/pipeline-compliance-gate ch001
    ├─► /inspiration-log         写: compliance/inspiration_log.yaml
    ├─► /inspiration-check       写: compliance/risk_report.yaml
    └─► /inspiration-report      (输出报告)
```

### 4.2 修改角色后的影响链

```
/character-edit 赵宋 "增加新特征"
    │
    │ [post-edit-impact-scan]
    │   读: chapters/index.yaml → 筛选含"赵宋"的章节
    │   对每个相关章节检查冲突
    │
    └─► 输出：
        "⚠️ ch003 中赵宋的行为与新增特征可能矛盾（L45: '...'）"
        "建议检查：/consistency-check --chapter ch003"
```

### 4.3 修改设定后的影响链

```
/setting-edit rule_001 "修改污染机制"
    │
    │ [post-edit-impact-scan]
    │   读: chapters/index.yaml → 检查引用此设定的章节
    │   读: characters/*.yaml → 检查引用此设定的角色
    │
    ├─► 若使用 --evolve：
    │   └─► /setting-add rule_001b (新版本, supersedes: rule_001)
    │       写: worldbuilding/entries/rule_001b.yaml
    │       写: worldbuilding/entries/rule_001.yaml (superseded_by: rule_001b)
    │
    └─► 输出影响报告
```
