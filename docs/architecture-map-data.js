// ═══════════════════════════════════════════════════════════════
// AI Novel Writing System — Architecture Map Data
// ═══════════════════════════════════════════════════════════════
// 编辑此文件以更新架构地图，HTML 渲染器会自动反映变更。
// Last updated: 2026-04-08
// ═══════════════════════════════════════════════════════════════

const MAP_DATA = {

  // ─── 项目元信息 ───
  meta: {
    title: "AI 小说写作系统",
    subtitle: "面向长篇连载与多项目管理的 AI 写作工作台",
    version: "v2.0",
    highlights: [
      { value: 57, label: "专业技能", suffix: "个" },
      { value: 8,  label: "自动化流水线", suffix: "条" },
      { value: 12, label: "领域模块", suffix: "个" },
      { value: 20, label: "数据模板", suffix: "套" }
    ],
    selling_points: [
      "多项目隔离管理，同时运营多部长篇作品",
      "57 个原子技能覆盖创作全链路，按需编排",
      "8 条端到端流水线，意图驱动、一键触发",
      "AI 痕迹检测与去除，保障作品原创质感",
      "世界观一致性审查，自动消灭设定矛盾",
      "合规闸口 + 可追溯借鉴台账，规避法律风险",
      "数据驱动模板系统，5 分钟初始化新项目"
    ]
  },

  // ─── 架构分层 ───
  layers: [
    {
      id: "pipeline",
      name: "流水线编排层",
      subtitle: "Pipeline Orchestration",
      description: "意图驱动的自动化编排，将多个原子技能组合为端到端工作流",
      color: "#8b5cf6",
      gradient: ["#7c3aed", "#a78bfa"]
    },
    {
      id: "creative",
      name: "创作引擎层",
      subtitle: "Creative Engine",
      description: "覆盖小说创作全要素：角色、关系、剧情、世界观、章节、时间线、场景",
      color: "#3b82f6",
      gradient: ["#2563eb", "#60a5fa"]
    },
    {
      id: "quality",
      name: "质量保障层",
      subtitle: "Quality Assurance",
      description: "风格控制、AI痕迹检测、一致性审查、合规闸口",
      color: "#14b8a6",
      gradient: ["#0d9488", "#5eead4"]
    },
    {
      id: "platform",
      name: "平台基础层",
      subtitle: "Platform Foundation",
      description: "项目管理、素材桥接、模板系统、共享协议",
      color: "#6366f1",
      gradient: ["#4f46e5", "#818cf8"]
    }
  ],

  // ─── 领域模块（含嵌套技能） ───
  modules: [

    // ── 流水线编排层 ──
    {
      id: "pipeline",
      name: "流水线",
      icon: "⚡",
      layer: "pipeline",
      description: "薄编排预设，组合原子技能为完整工作流",
      skills: [
        { id: "pipeline-outline-bootstrap",    name: "大纲启动",   description: "从草稿/想法出发，经消化→确认→推导，产出初版大纲与基础设定" },
        { id: "pipeline-setting-consolidate",  name: "设定整固",   description: "审查、补强并确认世界观设定，清理 tentative 堆积" },
        { id: "pipeline-outline-polish",       name: "大纲打磨",   description: "审查并补强大纲，联动世界观与一致性检查" },
        { id: "pipeline-note-triage",          name: "笔记分拣",   description: "读取混合笔记，按类型分拣派发到对应技能落地" },
        { id: "pipeline-chapter-kickoff",      name: "章节启动",   description: "编排章节创建、状态推进、情节点补全" },
        { id: "pipeline-draft-polish",         name: "草稿打磨",   description: "结构审查 + 人物声音 + 去AI感处理" },
        { id: "pipeline-continuity-gate",      name: "连续性闸口", description: "汇总关系、时间线、跨模块一致性检查" },
        { id: "pipeline-compliance-gate",      name: "合规闸口",   description: "串联借鉴登记→风险检查→范围报告" }
      ]
    },

    // ── 创作引擎层 ──
    {
      id: "character",
      name: "角色系统",
      icon: "👤",
      layer: "creative",
      description: "角色创建、编辑与查询，含五件套心理模型",
      skills: [
        { id: "character-add",   name: "创建角色", description: "创建角色并补齐缺陷、执念、软肋、误判、反差" },
        { id: "character-edit",  name: "编辑角色", description: "编辑已有角色信息，补充心理特征与弧光" },
        { id: "character-query", name: "查询角色", description: "查询角色详细信息" }
      ]
    },
    {
      id: "relationship",
      name: "关系系统",
      icon: "🔗",
      layer: "creative",
      description: "角色关系定义、图谱、演进追踪与一致性检查",
      skills: [
        { id: "relationship-add",       name: "建立关系",   description: "定义关系类型、张力来源与机制" },
        { id: "relationship-map",       name: "关系图谱",   description: "生成角色关系网络图" },
        { id: "relationship-log",       name: "关系日志",   description: "记录关系变化事件（原因/代价/误判）" },
        { id: "relationship-evolution", name: "关系演进",   description: "查看关系时间演进轨迹" },
        { id: "relationship-check",     name: "关系审查",   description: "检查关系跳变、逻辑断裂" }
      ]
    },
    {
      id: "worldbuilding",
      name: "世界观",
      icon: "🌍",
      layer: "creative",
      description: "设定集管理与世界观自洽性审查",
      skills: [
        { id: "setting-add",         name: "添加设定",   description: "创建/更新设定条目，支持批量导入" },
        { id: "setting-edit",        name: "编辑设定",   description: "修改设定内容与状态流转" },
        { id: "worldbuilding-review", name: "世界观审查", description: "审查自洽性、规则缺口、代价缺失" }
      ]
    },
    {
      id: "plot",
      name: "剧情系统",
      icon: "📖",
      layer: "creative",
      description: "大纲初始化、节点管理、审查与 AI 剧情建议",
      skills: [
        { id: "plot-init",    name: "初始化大纲", description: "从素材推导或模板创建大纲结构" },
        { id: "plot-add",     name: "添加节点",   description: "添加情节节点到大纲" },
        { id: "plot-edit",    name: "编辑节点",   description: "修改大纲节点，内置影响分析" },
        { id: "plot-query",   name: "查询大纲",   description: "按章节/伏笔/角色/冲突维度检索" },
        { id: "plot-review",  name: "大纲审查",   description: "审查结构骨架、转折、节奏、钩子" },
        { id: "plot-suggest", name: "剧情建议",   description: "AI 生成反转、钩子、爽点升级建议" }
      ]
    },
    {
      id: "chapter",
      name: "章节系统",
      icon: "📝",
      layer: "creative",
      description: "章节全生命周期：创建、写作、看板、审查、导出",
      skills: [
        { id: "chapter-create", name: "创建章节", description: "新建章节并初始化元数据" },
        { id: "chapter-update", name: "更新章节", description: "更新章节元数据与状态" },
        { id: "chapter-draft",  name: "章节写作", description: "基于大纲和设定辅助生成初稿" },
        { id: "chapter-board",  name: "章节看板", description: "按状态展示章节看板" },
        { id: "chapter-review", name: "章节审查", description: "审查结构、节奏、角色行为、钩子" },
        { id: "chapter-export", name: "章节导出", description: "导出连续文档用于发布" }
      ]
    },
    {
      id: "timeline",
      name: "时间线",
      icon: "⏳",
      layer: "creative",
      description: "时间线事件管理与逻辑冲突检测",
      skills: [
        { id: "timeline-add",   name: "添加事件", description: "添加时间线事件" },
        { id: "timeline-check", name: "时间检查", description: "检查时间线逻辑冲突" },
        { id: "timeline-view",  name: "查看时间线", description: "查看时间线（支持范围筛选）" }
      ]
    },
    {
      id: "scene",
      name: "场景系统",
      icon: "🎬",
      layer: "creative",
      description: "场景空间、氛围、感官细节与叙事功能档案",
      skills: [
        { id: "scene-add", name: "创建场景", description: "记录场景的空间、氛围、感官和叙事功能" }
      ]
    },

    // ── 质量保障层 ──
    {
      id: "style",
      name: "风格与改写",
      icon: "🎨",
      layer: "quality",
      description: "写作风格模板管理、文本改写、人物声音检查",
      skills: [
        { id: "style-create", name: "创建风格", description: "创建写作风格模板" },
        { id: "style-list",   name: "列出风格", description: "列出可用的风格模板" },
        { id: "rewrite",      name: "风格改写", description: "按指定风格改写文本" },
        { id: "voice-check",  name: "声音检查", description: "检查对白是否有稳定可区分的人物声音" }
      ]
    },
    {
      id: "anti-ai",
      name: "AI 痕迹治理",
      icon: "🛡️",
      layer: "quality",
      description: "检测并消除 AI 写作痕迹，保障原创质感",
      skills: [
        { id: "anti-ai-check",   name: "AI 痕迹检测", description: "检测章节中的 AI 痕迹并输出量化评分" },
        { id: "anti-ai-rewrite", name: "去 AI 改写",   description: "保持剧情信息不变，去除 AI 感" }
      ]
    },
    {
      id: "compliance",
      name: "合规系统",
      icon: "⚖️",
      layer: "quality",
      description: "借鉴来源登记、风险检测与合规报告",
      skills: [
        { id: "inspiration-log",    name: "借鉴登记", description: "记录借鉴来源与借鉴维度" },
        { id: "inspiration-check",  name: "风险检测", description: "检查借鉴风险并输出降风险建议" },
        { id: "inspiration-report", name: "合规报告", description: "汇总借鉴登记与风险结果" }
      ]
    },
    {
      id: "consistency",
      name: "一致性引擎",
      icon: "🔍",
      layer: "quality",
      description: "全面跨模块一致性审查",
      skills: [
        { id: "consistency-check", name: "一致性检查", description: "全面一致性检查（角色/设定/时间线/剧情）" }
      ]
    },

    // ── 平台基础层 ──
    {
      id: "project-mgmt",
      name: "项目管理",
      icon: "⚙️",
      layer: "platform",
      description: "多项目生命周期管理、状态诊断、KPI 与周报",
      skills: [
        { id: "novel-init",            name: "创建项目",   description: "初始化新的小说项目" },
        { id: "novel-switch",          name: "切换项目",   description: "切换当前工作的小说项目" },
        { id: "novel-list",            name: "列出项目",   description: "列出所有小说项目" },
        { id: "novel-status",          name: "项目状态",   description: "查看当前项目详细状态" },
        { id: "novel-edit",            name: "编辑项目",   description: "编辑项目基础信息并级联更新" },
        { id: "novel-doctor",          name: "项目诊断",   description: "诊断项目健康状态" },
        { id: "novel-kpi",             name: "项目 KPI",   description: "计算产能与风险治理指标" },
        { id: "project-weekly-report", name: "项目周报",   description: "管理者版与作者版双视角周报" },
        { id: "project-reindex",       name: "索引重建",   description: "重建交叉索引、反向引用与项目地图" }
      ]
    },
    {
      id: "material",
      name: "素材桥接",
      icon: "📚",
      layer: "platform",
      description: "草稿/素材深度消化与外部素材库检索",
      skills: [
        { id: "draft-ingest",    name: "素材消化",   description: "深度消化草稿/素材，提取真实逻辑与创作意图" },
        { id: "material-search", name: "素材检索",   description: "跨库场景检索、人物原型、技法参考" }
      ]
    },
    {
      id: "infra",
      name: "系统维护",
      icon: "🏗️",
      layer: "platform",
      description: "技能系统自身的健康检查与文档同步",
      skills: [
        { id: "skill-doctor", name: "技能诊断", description: "评估技能变更影响范围，检查跨技能一致性" }
      ]
    }
  ],

  // ─── 流水线组合关系（pipeline → 消费的原子技能） ───
  pipeline_composition: {
    "pipeline-outline-bootstrap":   ["draft-ingest", "setting-add", "plot-init", "plot-add", "timeline-add", "timeline-check"],
    "pipeline-setting-consolidate": ["setting-edit", "worldbuilding-review"],
    "pipeline-outline-polish":      ["plot-review", "worldbuilding-review", "plot-suggest", "plot-edit", "plot-add", "setting-edit", "setting-add", "consistency-check"],
    "pipeline-note-triage":         ["setting-add", "character-add", "plot-add", "timeline-add", "relationship-add"],
    "pipeline-chapter-kickoff":     ["chapter-create", "chapter-update", "plot-add"],
    "pipeline-draft-polish":        ["chapter-review", "voice-check", "anti-ai-check", "anti-ai-rewrite", "chapter-update"],
    "pipeline-continuity-gate":     ["relationship-check", "timeline-check", "worldbuilding-review", "consistency-check"],
    "pipeline-compliance-gate":     ["inspiration-log", "inspiration-check", "inspiration-report"]
  },

  // ─── 小说创作生命周期（推荐宏观流程） ───
  lifecycle: [
    { step: 1,  id: "ingest",      name: "素材消化",   pipeline: "draft-ingest",                  description: "深度理解草稿与创作意图" },
    { step: 2,  id: "bootstrap",   name: "大纲启动",   pipeline: "pipeline-outline-bootstrap",     description: "产出初版大纲与基础设定" },
    { step: 3,  id: "setting",     name: "设定整固",   pipeline: "pipeline-setting-consolidate",   description: "清理并确认世界观设定" },
    { step: 4,  id: "outline",     name: "大纲打磨",   pipeline: "pipeline-outline-polish",        description: "优化结构、节奏与转折" },
    { step: 5,  id: "kickoff",     name: "章节启动",   pipeline: "pipeline-chapter-kickoff",       description: "创建章节并补全情节点" },
    { step: 6,  id: "draft",       name: "章节写作",   pipeline: "chapter-draft",                  description: "基于设定辅助生成初稿" },
    { step: 7,  id: "polish",      name: "草稿打磨",   pipeline: "pipeline-draft-polish",          description: "审查 + 声音 + 去AI感" },
    { step: 8,  id: "continuity",  name: "连续性检查", pipeline: "pipeline-continuity-gate",       description: "关系/时间线/设定一致性" },
    { step: 9,  id: "compliance",  name: "合规检查",   pipeline: "pipeline-compliance-gate",       description: "借鉴风险与合规报告" },
    { step: 10, id: "export",      name: "导出发布",   pipeline: "chapter-export",                 description: "导出为连续文档发布" }
  ],

  // ─── 共享协议与基础设施 ───
  protocols: [
    { id: "chapter-auto-inference", name: "章节自动推断", description: "省略章节 ID 时自动推断当前章节" },
    { id: "from-extraction",        name: "统一提取协议", description: "character-add / plot-add / setting-add 的 --from 流程" },
    { id: "reference-reporting",    name: "缺失口径协议", description: "数据缺失时的 N/A 统一处理规则" }
  ],

  shared_resources: [
    { id: "templates",       name: "项目模板",     count: 20, description: "20 套 YAML/MD 模板，覆盖角色/剧情/设定/章节/合规" },
    { id: "style-templates", name: "风格模板库",   count: null, description: "古龙风、热血玄幻等预设风格与反面教材" },
    { id: "anti-ai-rules",  name: "AI 痕迹规则库", count: null, description: "短语黑名单、句式限制、对白评分阈值" },
    { id: "cursor-rules",   name: "编辑器规则",   count: 3, description: "自动同步的世界观护栏 + 工作流 + 项目上下文" }
  ],

  // ─── 外部集成 ───
  external: [
    { id: "novel-material",  name: "素材库",   description: "外部素材检索库（人物原型、技法参考、场景库）" },
    { id: "novel-knowledge", name: "知识库",   description: "写作知识与技法参考库" },
    { id: "cursor-ide",      name: "Cursor IDE", description: "编辑器集成，规则自动同步" }
  ]
};
