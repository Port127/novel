# Schema Alignment — nv_20260625_00t3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate `novels/nv_20260625_00t3` 的 5 组文件与项目 V4 schema 对齐，零内容丢失，5 个独立 commit。

**Architecture:** 逐文件分步迁移。每个 commit 独立可回滚。内容优先策略：Schema 标准字段为骨架，现有创意内容重新归类到对应字段，Schema 无对应字段的内容作为扩展字段保留。Enum 保留原始值不强行映射。

**Tech Stack:** YAML, Git

**Spec:** `docs/superpowers/specs/2026-07-01-schema-alignment-design.md`

**Commit message:** 每个 commit 遵循 commit-msg skill（`/commit-msg`）。

---

## File Structure Overview

| 操作 | 文件路径 | 说明 |
|------|----------|------|
| 重写 | `novels/nv_20260625_00t3/settings/worldbuilding.yaml` | 补 schema 骨架，现有内容重新归类 |
| 重写 | `novels/nv_20260625_00t3/settings/characters.yaml` | 分组对象 → `characters[]` 扁平数组 |
| 重写 | `novels/nv_20260625_00t3/settings/outline.yaml` | 拆 premise、补 acts、hooks → plotlines |
| 重写 | `novels/nv_20260625_00t3/settings/notes.yaml` | 新建结构化追踪骨架 |
| 新建 | `novels/nv_20260625_00t3/references/mechanics.yaml` | 从 notes 迁出的创意备忘 |
| 新建 | `novels/nv_20260625_00t3/references/design_principles.yaml` | 从 characters 迁出的设计原则 |
| 新建 | `novels/nv_20260625_00t3/settings/chapter_outlines/.gitkeep` | 蓝图目录占位 |
| 删除 | `novels/nv_20260625_00t3/content/chapters/` | 废弃路径 |

**Schema 参考文件**（只读，不修改）：

| Schema | 路径 |
|--------|------|
| worldbuilding | `data/schemas/worldbuilding.schema.yaml` |
| characters | `data/schemas/characters.schema.yaml` |
| outline | `data/schemas/outline.schema.yaml` |
| notes | `data/schemas/notes.schema.yaml` |

---

## Task 1: worldbuilding.yaml — 补 Schema 骨架 + 内容重新归类

**Files:**
- Read: `novels/nv_20260625_00t3/settings/worldbuilding.yaml` (current, 196 lines)
- Read: `data/schemas/worldbuilding.schema.yaml` (reference)
- Modify: `novels/nv_20260625_00t3/settings/worldbuilding.yaml`

**Transformation rules:**

1. 在文件顶部新增 `world_type: "都市"` 和 `setting_period: "2009年12月"`
2. 从原 `foreknowledge_advantages.limitations` + 金手指规则提取 `core_rules[]`
3. 从金手指规则 + 自主权成长线构建 `power_system` 对象
4. 从原 `school_info` 构建 `locations[]`（每个学校一个条目）
5. 从学校信息构建 `factions[]`
6. 从 `era_context.key_events` 构建 `lore.history[]`
7. 保留 `university_life`、`social_context`、`foreknowledge_advantages`（去掉 limitations）作为扩展字段
8. 删除原 `school_info`（已迁入 locations）和 `era_context`（已迁入 lore.history）

- [ ] **Step 1: Read current worldbuilding.yaml**

读取 `novels/nv_20260625_00t3/settings/worldbuilding.yaml`，确认当前内容包含：`school_info`、`era_context`、`university_life`、`social_context`、`foreknowledge_advantages`。

- [ ] **Step 2: Write transformed worldbuilding.yaml**

将文件完整替换为以下内容。内容来源标注在注释中：

```yaml
# 世界观设定
# 2009年大学生活背景 + 金手指规则 + 时代设定
# Schema: data/schemas/worldbuilding.schema.yaml

# ═══════════════════════════════════════════════════
# Schema 标准字段
# ═══════════════════════════════════════════════════

world_type: "都市"
setting_period: "2009年12月"

core_rules:
  - rule: "不能暴露穿越身份"
    implications: "所有先知行为必须有合理掩护，不能直接引用未来事件"
  - rule: "大一学生身份约束：资金有限、人脉为零、信任度低"
    implications: "创业需要从零积累，商业谈判时缺乏背书"
  - rule: "歌曲只能入梦，不能直接发布"
    implications: "金手指不提供直接的'文抄公'收入，只能通过副本奖励变现"

power_system:
  name: "梦入歌曲"
  type: "异能"
  ranks:
    - name: "初期"
      description: "无自主权，被动跟随歌曲剧情线扮演角色"
      capabilities:
        - "像看电影一样被剧情推着走"
        - "只能在角色框架内行动"
    - name: "中期"
      description: "有限自主权，可在关键节点做出选择"
      capabilities:
        - "开始影响剧情走向"
        - "大框架仍受歌曲约束"
    - name: "后期"
      description: "高度自主权，可以主动改变故事结局"
      capabilities:
        - "能从歌曲世界中带出非随机奖励"
        - "主动选择副本和策略"
  rules:
    - rule: "原作发布前一个月内 + 第一次唱出 = 触发入梦"
      implications: "天然有时间压力和稀缺性"
    - rule: "必须与歌手有现实接触（同处一室/看到本人/一起吃饭等），才能解锁该歌手的歌曲"
      implications: "接触歌手本身就是一条剧情线"
    - rule: "每首歌只有唯一一次机会，错过窗口期永久失效"
      implications: "选歌 = 选副本 = 选奖励方向 = 重要剧情决策"
    - rule: "接触一位歌手 = 解锁该歌手全部歌曲（各歌窗口期独立计算）"
      implications: "每个新歌手都是一条冒险/任务线"
    - rule: "被他人（女主）听到歌声才会一同入梦"
      implications: "入梦可以是多人参与"
    - rule: "男主清晰记住梦境，其他人只有模糊印象"
      implications: "男主可以复盘梦境情报，其他人只能'好像做了个梦'"
  limitations:
    - limitation: "资金有限（大一学生身份）"
    - limitation: "人脉有限（需要从零积累，大一没校友资源）"
    - limitation: "时间有限（还要上课、晚自习）"
    - limitation: "不能暴露穿越身份"
    - limitation: "歌曲只能入梦，不能直接发布（版权限制）"
    - limitation: "必须与歌手有现实接触，才能解锁其歌曲（核心约束）"
    - limitation: "大一身份 = 商业谈判时信任度极低"

factions:
  - name: "合肥工业大学计算机系"
    type: "其他"
    stance: "中立"
    territory: "合工大校园（包河区屯溪路193号）"
    key_figures:
      - "男主（大一新生）"
      - "室友/合伙人"
    description: "男主所在学校，故事主场景"
  - name: "中国科学技术大学"
    type: "其他"
    stance: "中立"
    territory: "中科大校园（包河区金寨路96号）"
    key_figures:
      - "女主一（大一新生）"
    description: "女主所在学校，与合工大距离3-4km，打车10-20分钟"
  - name: "安徽医科大学"
    type: "其他"
    stance: "中立"
    territory: "蜀山区梅山路81号"
    key_figures:
      - "许嵩（校友）"
    description: "许嵩母校，2009年12月许嵩回校做小演出，是触发第一个副本的关键地点"
  - name: "安徽农业大学"
    type: "其他"
    stance: "中立"
    territory: "蜀山区长江西路130号"
    key_figures:
      - "男主高中同学"
    description: "男主高中同学在此就读，周末去找他玩时偶遇许嵩演出"

locations:
  - name: "合肥工业大学"
    type: "建筑"
    description: "男主所在学校，计算机科学与技术专业大一。包河区屯溪路193号。"
    significance: "故事主场景，男主宿舍/教室/食堂/图书馆均在此"
    sub_locations:
      - name: "男生宿舍"
        type: "区域"
        description: "6人宿舍（大一标配），室友是最早的核心圈子"
      - name: "计算机系教学楼"
        type: "建筑"
        description: "上课和机房开发的主要场所"
      - name: "食堂"
        type: "建筑"
        description: "日常就餐，偶尔电话订外卖"
      - name: "图书馆"
        type: "建筑"
        description: "5层楼，自习和查阅资料"
      - name: "操场/篮球场"
        type: "区域"
        description: "课外活动和社交"
  - name: "中国科学技术大学"
    type: "建筑"
    description: "女主所在学校。东校区在包河区金寨路96号，西校区在蜀山区黄山路。与合工大距离3-4km。"
    significance: "女主活动场景，跨校串门合理"
  - name: "安徽医科大学"
    type: "建筑"
    description: "蜀山区梅山路81号。许嵩母校。"
    significance: "许嵩回校演出的地点，触发第一个副本的关键场景"
  - name: "安徽农业大学"
    type: "建筑"
    description: "蜀山区长江西路130号。"
    significance: "男主高中同学在此，周末去找他玩的目的地"
  - name: "合肥市区"
    type: "城市"
    description: "蜀山区/包河区为中心，大学都在市中心区域，打车15-30分钟可达。庐州=合肥古称。"
    significance: "故事发生城市，庐州月的'庐州'即此"

lore:
  history:
    - event: "3G牌照发放，移动互联网元年"
      period: "2009-01"
      impact: "男主先知移动互联网爆发，创业方向的基础"
    - event: "新浪微博上线"
      period: "2009-08"
      impact: "社交媒体新渠道"
    - event: "iPhone 3GS进入中国"
      period: "2009-09"
      impact: "智能手机时代开启，移动App开发机会"
    - event: "淘宝第一次双11"
      period: "2009-11"
      impact: "电商爆发的前兆"
    - event: "小米公司筹备中"
      period: "2010-01"
      impact: "男主可以先知的手机市场变化"
    - event: "iPhone 4发布"
      period: "2010-06"
      impact: "智能手机真正爆发"
    - event: "微信上线"
      period: "2011-01"
      impact: "男主可以预见的最大社交产品机会"
  artifacts: []
  terminology: []

# ═══════════════════════════════════════════════════
# 扩展字段（Schema 外，内容保留）
# ═══════════════════════════════════════════════════

# 大学生活详细设定
university_life:
  academics:
    major: "计算机科学与技术"
    year: "大一"
    key_courses:
      - "高等数学"
      - "大学英语"
      - "C语言程序设计"
      - "计算机导论"
      - "大学物理"
    workload: "中等（大一基础课为主，课余时间充裕）"
    note: "大一是黄金时间：课程压力小，有充足时间探索/创业/接触人"
    gpa_requirement: "保持中等即可，不影响主线"

  campus_culture:
    note: "大一新生：课少、时间多、精力旺盛、规则感弱、对一切充满好奇"
    dorm_life: "6-8人宿舍（大一标配），室友是最早的核心圈子"
    social_media: "QQ空间、人人网（校内网）、博客"
    messaging: "QQ、飞信"
    entertainment:
      - "网吧打游戏（魔兽世界、DOTA、CS）"
      - "KTV"
      - "社团招新/活动（大一最积极）"
      - "校园歌会/音乐节（接触外部歌手的机会）"
    restrictions: "大一有晚自习、查寝、不能随便出校（比高年级受限）"
    shopping: "淘宝刚兴起，线下购物为主"
    food: "食堂为主，偶尔外卖（电话订餐）"

  tech_environment:
    programming_languages:
      - "C/C++（教学用）"
      - "Java（企业开发）"
      - "Python（开始流行）"
      - "PHP（Web开发）"
      - "JavaScript（前端）"
    frameworks:
      - "Struts/Spring（Java）"
      - "Django/Rails（新兴）"
    mobile_development:
      - "iOS开发（刚起步）"
      - "Android开发（2008年SDK发布）"
      - "Symbian（诺基亚，即将淘汰）"
    tools:
      - "IDE: Eclipse, Visual Studio"
      - "版本控制: SVN（Git还没普及）"
      - "数据库: MySQL, Oracle"

  career_landscape:
    it_industry:
      hot_companies:
        - "BAT（百度、阿里、腾讯）刚崛起"
        - "华为、中兴（通信设备）"
        - "微软、谷歌（外企）"
        - "盛大、网易（游戏）"
      salary_range: "应届生5k-10k（一线城市）"
      career_paths:
        - "程序员（技术路线）"
        - "产品经理（产品路线）"
        - "创业（风险高，机会多）"

    entrepreneurship:
      opportunities:
        - "移动互联网创业（App开发）"
        - "电商创业（淘宝开店）"
        - "网站建设（外包）"
      challenges:
        - "资金门槛（大一学生几乎为零）"
        - "经验不足（学生创业难，大一更甚）"
        - "身份劣势（大一没有专业背书，比高年级更难获得信任）"
        - "时间管理（大一课多+晚自习，时间碎片化）"
      advantages:
        - "大一时试错成本低，没有毕业压力"
        - "同学是大一，容易组建忠诚团队（一起从零开始）"
        - "合工大=合肥，合肥2009年互联网氛围弱但成本低"
        - "许嵩回安医大演出=接触娱乐圈/音乐圈的天然切入点"

# 社会背景
social_context:
  economy:
    gdp_growth: "8.7%（2009年）"
    real_estate: "房价开始上涨，但还没到疯狂程度"
    stock_market: "2008年股灾后恢复中"
    consumer_behavior: "储蓄为主，消费观念保守"

  culture:
    music:
      - "许嵩、徐良、汪苏泷（网络歌手三巨头）"
      - "周杰伦、林俊杰、王力宏（流行天王）"
      - "陈奕迅、张学友（实力派）"
      - "独立音乐开始兴起"
    movies:
      - "国产片崛起（《建国大业》《风声》）"
      - "好莱坞大片（《阿凡达》2009年底上映）"
    tv_shows:
      - "选秀节目（快乐女声）"
      - "偶像剧（《一起来看流星雨》）"
      - "美剧（《越狱》《迷失》）"
    internet_culture:
      - "贴吧文化（李毅吧）"
      - "天涯论坛"
      - "猫扑"
      - "AcFun、Bilibili（刚起步）"

  technology:
    smartphones:
      - "iPhone 3GS（高端）"
      - "诺基亚（N97、5800）"
      - "HTC（Android手机）"
      - "山寨机（低端市场）"
    computers:
      - "笔记本电脑开始普及"
      - "台式机仍是主流"
      - "上网本（短暂流行）"
    internet:
      - "宽带普及（2M-4M）"
      - "WiFi开始进入校园"
      - "3G网络刚起步"

# 男主的先知优势
foreknowledge_advantages:
  business_opportunities:
    - "知道移动互联网会爆发"
    - "知道微信会成功"
    - "知道比特币会暴涨（2009年1月上线）"
    - "知道房价会涨"
    - "知道哪些App会火"

  tech_advantages:
    - "掌握未来5-6年的技术趋势"
    - "知道哪些编程语言会流行"
    - "知道哪些框架会成功"
    - "有实际项目开发经验（前世创业）"

  cultural_advantages:
    - "知道哪些歌会火"
    - "知道哪些电影会票房大卖"
    - "知道哪些网络用语会流行"
```

- [ ] **Step 3: Validate structure**

验证要点：
- 顶层存在 `world_type`、`setting_period`、`core_rules`、`power_system`、`factions`、`locations`、`lore` — Schema 必填/核心字段
- `power_system` 包含 `name`、`type`、`ranks`（3 级）、`rules`、`limitations` — Schema 必填子字段
- `locations[]` 每项含 `name`、`type`、`description` — Schema 必填子字段
- 扩展字段 `university_life`、`social_context`、`foreknowledge_advantages` 存在且内容完整
- 原 `school_info` 已拆解到 `locations` + `factions`（不再存在）
- 原 `era_context` 已迁移到 `lore.history`（不再存在）
- 原 `foreknowledge_advantages.limitations` 已迁入 `power_system.limitations`（原位置不再有）

- [ ] **Step 4: Commit**

```bash
git add novels/nv_20260625_00t3/settings/worldbuilding.yaml
```

Commit message 遵循 commit-msg skill。建议 scope: `settings`，subject: `worldbuilding: 对齐 V4 schema，补 world_type/power_system/locations 等标准字段`

---

## Task 2: characters.yaml — 分组对象 → 扁平 `characters[]` 数组

**Files:**
- Read: `novels/nv_20260625_00t3/settings/characters.yaml` (current, 188 lines)
- Read: `data/schemas/characters.schema.yaml` (reference)
- Modify: `novels/nv_20260625_00t3/settings/characters.yaml`
- Create: `novels/nv_20260625_00t3/references/design_principles.yaml`

**Transformation rules:**

1. 顶层改为 `characters: []` 扁平数组
2. 每个角色带 `role` 字段：`protagonist`/`antagonist`/`supporting`
3. `protagonist` → `characters[0]`，archetype 保留 `重生逆袭型`
4. `heroine_1/2/3` → `characters[1-3]`，role 设为 `supporting`
5. `supporting_characters` → `characters[4-5]`，原 `role` 描述并入 `description`
6. `antagonists` → `characters[6-7]`，新增 psychology/arc 骨架
7. 各角色的 `background` 扩展字段保留 age/school/major/family 等非 Schema 信息
8. 女主的 `romance_arc` 重构为 Schema 的 `arc` 格式
9. 顶层 `relationships: []`（空）丢弃 → 改为各角色内 `relationships[]`
10. `design_principles` 移出到新文件

- [ ] **Step 1: Read current characters.yaml**

读取 `novels/nv_20260625_00t3/settings/characters.yaml`，确认当前结构包含 `protagonist`、`heroine_1`、`heroine_2`、`heroine_3`、`supporting_characters`、`antagonists`、`relationships`、`design_principles`。

- [ ] **Step 2: Write references/design_principles.yaml**

将 `design_principles` 段落提取到新文件：

```yaml
# 人物设计原则
# 从 characters.yaml 迁出，独立维护

principles:
  - id: "P001"
    principle: "差异化"
    description: "每个女主必须有鲜明的性格、背景、互动模式"
    note: "避免同质化，让读者能清晰区分"

  - id: "P002"
    principle: "功能分工"
    description: "每个女主在故事中有不同的功能"
    note: "主线恋爱/调剂/冲突/成长等"

  - id: "P003"
    principle: "独立价值"
    description: "每个女主都有独立的存在价值，不依附男主"
    note: "有自己的事业、追求、成长线"

  - id: "P004"
    principle: "副本配合"
    description: "不同女主适合不同的副本风格"
    note: "古风副本适合古典气质女主，现代副本适合活泼女主等"

  - id: "P005"
    principle: "修罗场平衡"
    description: "多女主之间要有适度的竞争和张力"
    note: "但不过度撕逼，保持和谐"
```

- [ ] **Step 3: Write transformed characters.yaml**

将文件完整替换为以下内容：

```yaml
# 人物设定
# Schema: data/schemas/characters.schema.yaml
# 设计原则见 references/design_principles.yaml

characters:
  # ═══════════════════════════════════════════════════
  # 男主
  # ═══════════════════════════════════════════════════
  - name: ""
    role: protagonist
    archetype: 重生逆袭型
    description: "前世商业失败，重生回2009年大一，带着前世记忆重新来过"

    traits:
      - "商业嗅觉敏锐（前世经验）"
      - "技术背景扎实（计算机系）"
      - "人情世故老练（前世历练）"
      - "外表年轻但内心成熟"

    psychology:
      fatal_flaw: "前世失败留下的心理阴影，对某些决定过于谨慎"
      obsession: "弥补前世遗憾（感情+事业）"
      soft_spot: "对女主一的感情，对家人的愧疚"
      misbelief: "以为靠先知优势就能一帆风顺"

    arc:
      type: 成长弧线
      start: "带着前世记忆的重生者，自以为能掌控一切"
      end: "真正理解生活意义，平衡事业与感情"

    appearance:
      age: "18岁"
      gender: "男"
      features:
        - "身高175cm左右"
        - "普通长相，但气质沉稳"
        - "穿着朴素（大一学生标配）"

    background:                          # 扩展字段
      age: "18岁（大一新生）"
      school: "合肥工业大学"
      major: "计算机科学与技术"

  # ═══════════════════════════════════════════════════
  # 女主一
  # ═══════════════════════════════════════════════════
  - name: ""
    role: supporting
    archetype: 青梅竹马型
    description: "高中时就认识，大学重逢，家境优渥但不张扬"

    traits:
      - "温柔内敛"
      - "聪明但不张扬"
      - "家境好但不炫耀"
      - "对男主有好感但不明说"

    arc:
      type: 成长弧线
      start: "高中同学，大学重逢，彼此有好感"
      end: "卷一末明确关系"

    relationships:
      - to: "男主"
        type: 恋爱
        description: "高中同学，大学重逢，彼此有好感"
        importance: primary

    background:                          # 扩展字段
      age: "18岁（大一新生）"
      school: "中国科学技术大学"
      note: "男主的高中同学，隐形富二代"
      family: "隐形富二代（家里有钱但不张扬）"
      personality: "安静、有主见、不随波逐流"

    romance_arc:                         # 扩展字段
      initial_dynamic: "高中同学，大学重逢，彼此有好感"
      turning_points:
        - chapter: "第4章"
          event: "聚餐后散场，男主唱歌，女主听到，一同入梦"
          emotional_beat: "共同经历副本，关系拉近"
        - chapter: "第97-98章"
          event: "危机后感情突破"
          emotional_beat: "从暧昧到明确"
      confession_timing: "卷一末或卷二初"
      relationship_status: "卷一末明确关系"

  # ═══════════════════════════════════════════════════
  # 女主二（待设计）
  # ═══════════════════════════════════════════════════
  - name: ""
    role: supporting
    archetype: 待定
    description: "待定"
    traits: []

    arc:
      type: 探索弧线
      start: "待定"
      end: "待定"

    background:                          # 扩展字段
      age: "待定"
      school: "待定"
      note: "卷一后半段登场（约第57-60章）"
      family: "待定"
      personality: "待定（建议：干练外放，与女主一的温柔内敛形成对比）"

    romance_arc:                         # 扩展字段
      initial_dynamic: "因业务关系产生交集"
      turning_points: []
      confession_timing: "待定"
      relationship_status: "待定"

  # ═══════════════════════════════════════════════════
  # 女主三（待设计）
  # ═══════════════════════════════════════════════════
  - name: ""
    role: supporting
    archetype: 待定
    description: "待定"
    traits: []

    arc:
      type: 探索弧线
      start: "待定"
      end: "待定"

    background:                          # 扩展字段
      age: "待定"
      school: "待定"
      note: "卷二或卷三登场"
      family: "待定"
      personality: "待定"

    romance_arc:                         # 扩展字段
      initial_dynamic: "待定"
      turning_points: []
      confession_timing: "待定"
      relationship_status: "待定"

  # ═══════════════════════════════════════════════════
  # 配角
  # ═══════════════════════════════════════════════════
  - name: ""
    role: supporting
    archetype: 其他
    description: "男主的室友，技术骨干，一起创业"
    traits: []

  - name: ""
    role: supporting
    archetype: 其他
    description: "男主的高中同学，在安徽农业大学就读。周末去找他玩时引发许嵩接触线。"
    traits: []

  # ═══════════════════════════════════════════════════
  # 反派
  # ═══════════════════════════════════════════════════
  - name: ""
    role: antagonist
    archetype: 反派
    description: "卷二登场，同行竞争"

    traits: []

    psychology:
      obsession: "争夺市场份额"

    arc:
      type: 扁平弧线
      start: "竞争对手，争夺市场份额"
      end: "被击败或退让"

    background:                          # 扩展字段
      note: "卷二登场"

  - name: ""
    role: antagonist
    archetype: 反派
    description: "卷三登场，想控制男主公司"

    traits: []

    psychology:
      obsession: "资本逐利，控制男主公司"

    arc:
      type: 扁平弧线
      start: "资本方，想控制男主公司"
      end: "最终决战/和解"

    background:                          # 扩展字段
      note: "卷三登场"
```

- [ ] **Step 4: Validate structure**

验证要点：
- 顶层只有 `characters: []`（无 `protagonist`、`heroine_*`、`supporting_characters`、`antagonists`、`relationships`、`design_principles`）
- 共 8 个角色条目
- 每个条目有 `name`、`role`、`archetype`、`description` — Schema 必填字段
- protagonist 有 `traits`、`psychology`、`arc` — Schema 主角必填
- antagonist 有 `traits`、`psychology`、`arc` — Schema 反派必填
- supporting 有 `traits`、`description` — Schema 配角必填
- `design_principles` 不存在于此文件（已移到 references/design_principles.yaml）

- [ ] **Step 5: Commit**

```bash
git add novels/nv_20260625_00t3/settings/characters.yaml novels/nv_20260625_00t3/references/design_principles.yaml
```

Commit message 遵循 commit-msg skill。建议 scope: `settings`，subject: `characters: 分组对象重构为 characters[] 扁平数组，design_principles 迁出`

---

## Task 3: outline.yaml — 拆 premise、补 acts、hooks → plotlines

**Files:**
- Read: `novels/nv_20260625_00t3/settings/outline.yaml` (current, 75 lines)
- Read: `novels/nv_20260625_00t3/settings/arcs.yaml` (reference, for acts content)
- Read: `data/schemas/outline.schema.yaml` (reference)
- Modify: `novels/nv_20260625_00t3/settings/outline.yaml`

**Transformation rules:**

1. `premise` 从对象（含 statement/themes/tones/target_chapters/structure_note）拆为：
   - `premise: "..."` 字符串（从 statement 提取）
   - `theme: []` 顶层数组（从 themes 提取，保留原始值）
   - `tone: []` 顶层数组（从 tones 提取，保留原始值）
   - 丢弃 `target_chapters`（与 project.yaml 重复）和 `structure_note`
2. 从 arcs.yaml 的 6 个 arc 提炼 `acts[]`，每个 act 含 2-3 个 sequence，每个 sequence 含 beats
3. `hooks` 从分类嵌套（core/business/dungeon）重构为 `plotlines[]`
4. 新增空 `hooks: []` 和 `pacing_curve: []`

- [ ] **Step 1: Read source files**

读取 `outline.yaml` 和 `arcs.yaml`，确认当前内容。

- [ ] **Step 2: Write transformed outline.yaml**

将文件完整替换为以下内容：

```yaml
# 大纲
# Schema: data/schemas/outline.schema.yaml
# 详细弧线见 settings/arcs.yaml

# ═══════════════════════════════════════════════════
# 核心设定
# ═══════════════════════════════════════════════════

premise: "穿越回2009年的计算机系大学生，靠'梦入歌曲'的金手指在现实商业和梦境副本双线逆袭，最终建立商业帝国并收获多段感情。"

theme:
  - 商业逆袭
  - 多女主恋爱
  - 副本冒险
  - 青春校园

tone:
  - 轻松
  - 爽文
  - 温馨

# ═══════════════════════════════════════════════════
# 三幕式结构（卷一：第1-100章）
# 详细节拍见 settings/arcs.yaml
# ═══════════════════════════════════════════════════

acts:
  - act: 1
    title: 穿越觉醒
    chapters: [1, 5]
    arc: "穿越确认 + 偶遇许嵩 + 第一次入梦触发"
    sequences:
      - sequence: 1
        title: 穿越确认与规则摸索
        chapters: [1, 2]
        beats:
          - beat: 1
            title: 宿舍醒来
            chapter: 1
            description: "合工大男生宿舍醒来，确认回到2009年12月，前世记忆闪回（商海浮沉/感情遗憾），计算机系大一新生，一切都还来得及"
            tension: 4
          - beat: 2
            title: 金手指摸索
            chapter: 2
            description: "偶然哼《庐州月》发现奇异感应但唱到一半断了，摸索出部分规则：窗口期（12/6~1/5）+ 必须与歌手有现实接触"
            tension: 3
      - sequence: 2
        title: 偶遇许嵩与入梦触发
        chapters: [3, 5]
        beats:
          - beat: 1
            title: 偶遇演出
            chapter: 3
            description: "周末找高中同学(安农大)玩，听说许嵩回安医大做小演出，大家一起去看，远远看到许嵩，意识到这是接触他的机会"
            tension: 4
          - beat: 2
            title: 聚餐与唱歌
            chapter: 4
            description: "演出结束聚餐，女主（中科大，高中同学）也到场，散场时男主有感而发唱起《庐州月》，被女主听到，入梦触发"
            tension: 5
          - beat: 3
            title: 进入副本
            chapter: 5
            description: "意识被拉入古代庐州，发现变成赴考书生，女主也进来了扮演富商之女，章末钩子：庐州=合肥，一切冥冥之中"
            tension: 4
    turning_point:
      chapter: 4
      description: "散场时男主有感而发唱起庐州月，被女主听到，入梦触发"
      type: inciting_incident

  - act: 2
    title: 庐州月副本
    chapters: [6, 14]
    arc: "第一个完整副本 + 感情升温 + 建立金手指规则"
    sequences:
      - sequence: 1
        title: 副本深入
        chapters: [6, 11]
        beats:
          - beat: 1
            title: 感情萌芽
            chapter: 6
            description: "书生苦读，富商之女暗中送书，两人月下初谈，感情萌芽"
            tension: 3
          - beat: 2
            title: 阶级落差
            chapter: 7
            description: "月考/诗会展才华，富商注意，阶级落差初现，与现实中男主处境呼应"
            tension: 3
          - beat: 3
            title: 月下相会
            chapter: 8
            description: "两人互诉心事，感情升温，关键场景：为女主写诗"
            tension: 4
          - beat: 4
            title: 富商阻拦
            chapter: 9
            description: "富商发现，强行阻拦，冲突，书生被迫离开"
            tension: 4
          - beat: 5
            title: 高中状元
            chapter: 10
            description: "赴京赶考，路上波折，高中状元，短暂喜悦"
            tension: 3
          - beat: 6
            title: 绝望重逢
            chapter: 11
            description: "归来发现女主已被许配他人，绝望，名场面：月下重逢，相对无言"
            tension: 5
      - sequence: 2
        title: 梦醒与宝藏
        chapters: [12, 14]
        beats:
          - beat: 1
            title: 梦醒
            chapter: 12
            description: "梦境崩塌，醒来，清晨宿舍，两人面面相觑，只有男主记得全部"
            tension: 3
          - beat: 2
            title: 发现奖励
            chapter: 13
            description: "复盘发现手边多了古宅地图/钥匙，梦境奖励是真的，震惊"
            tension: 4
          - beat: 3
            title: 找到宝藏
            chapter: 14
            description: "按图索骥在庐州（合肥）找到古宅，发现宝藏，金银珠宝、古董文物，大惊喜"
            tension: 5
    turning_point:
      chapter: 13
      description: "醒来发现梦境奖励是真的，金手指从体验型变为实质收益型"
      type: first_threshold

  - act: 3
    title: 宝藏与觉醒
    chapters: [15, 25]
    arc: "宝藏名场面 + 创业启动 + 金手指规则确认"
    sequences:
      - sequence: 1
        title: 宝藏名场面
        chapters: [15, 19]
        beats:
          - beat: 1
            title: 文物困境
            chapter: 15
            description: "研究宝藏发现是文物不能卖，纠结"
            tension: 3
          - beat: 2
            title: 上报国家
            chapter: 16
            description: "思想斗争后决定上报国家联系文物局，名场面：泪崩（前世遗憾的映射）"
            tension: 4
          - beat: 3
            title: 表彰与反应
            chapter: 17
            description: "获得表彰但没赚到钱，室友同学的反应（喜剧效果），女主一觉得男主不简单"
            tension: 3
          - beat: 4
            title: 规则确认
            chapter: 18
            description: "复盘金手指，总结规则：发布前1个月/首次唱出/随机奖励，意识到每首歌只有一次机会"
            tension: 3
          - beat: 5
            title: "重新审视未来"
            chapter: 19
            description: "前世互联网记忆，2009年末时间节点：移动互联网前夜/淘宝崛起/微博兴起"
            tension: 3
      - sequence: 2
        title: 创业启动
        chapters: [20, 25]
        beats:
          - beat: 1
            title: 制定计划
            chapter: 20
            description: "第一个项目方向确定（校园社交/本地生活/外包开发），找合伙人"
            tension: 3
          - beat: 2
            title: 组建团队
            chapter: 21
            description: "拉室友入伙，技术分工，在机房没日没夜开发，第一次展示前世的产品思维"
            tension: 3
          - beat: 3
            title: 资金困境
            chapter: 22
            description: "项目雏形遇到资金问题，家里给不了钱，阶级落差感再次袭来"
            tension: 4
          - beat: 4
            title: 女主助力
            chapter: 23
            description: "女主一主动帮忙（不是直接给钱而是介绍资源/人脉），男主自尊心vs现实需要的张力"
            tension: 3
          - beat: 5
            title: 第一笔收入
            chapter: 24
            description: "项目上线小范围测试数据不错，第一笔收入进账（不多但是从零到一）"
            tension: 4
          - beat: 6
            title: 寻找更大机会
            chapter: 25
            description: "阶段性胜利但意识到小打小闹不够，需要更大的机会，看到下一首歌的窗口在逼近"
            tension: 3
    turning_point:
      chapter: 16
      description: "宝藏上报国家，反套路名场面，确立男主价值观"
      type: midpoint

  - act: 4
    title: "素颜副本 + 创业加速"
    chapters: [26, 50]
    arc: "第二个副本 + 业务增长 + 竞争对手初现"
    sequences:
      - sequence: 1
        title: 业务竞争
        chapters: [26, 33]
        beats:
          - beat: 1
            title: 项目迭代
            chapter: 26
            description: "项目迭代用户增长，从校园扩展到周边高校"
            tension: 3
          - beat: 2
            title: 竞争对手出现
            chapter: 29
            description: "遇到第一个竞争对手（校外开发团队/学长创业公司）"
            tension: 4
          - beat: 3
            title: 硬扛竞争
            chapter: 31
            description: "竞争压力，对方有资金有人脉，男主靠产品思维和前世经验硬扛"
            tension: 4
      - sequence: 2
        title: 素颜副本
        chapters: [34, 41]
        beats:
          - beat: 1
            title: 窗口逼近
            chapter: 34
            description: "《素颜》窗口期逼近（5/24~6/23），男主决定主动触发第二个副本"
            tension: 3
          - beat: 2
            title: 进入副本
            chapter: 36
            description: "唱出《素颜》，两人一同入梦，副本世界：现代校园/青春回忆风格"
            tension: 4
          - beat: 3
            title: 青春日常
            chapter: 38
            description: "副本内青春日常，甜蜜与遗憾并存，感情线加速"
            tension: 3
          - beat: 4
            title: 微弱自主权
            chapter: 40
            description: "副本高潮：关键选择，男主试图改变结局，发现有了微弱自主权，结局部分改变"
            tension: 5
          - beat: 5
            title: 梦醒暧昧
            chapter: 41
            description: "梦醒，两人关系微妙变化，女主一的记忆模糊但情感残留，暧昧加深"
            tension: 3
      - sequence: 3
        title: 能力反哺与打脸
        chapters: [42, 50]
        beats:
          - beat: 1
            title: 能力奖励
            chapter: 42
            description: "副本奖励：实用型（过目不忘/编程天赋/设计灵感），直接提升男主能力"
            tension: 4
          - beat: 2
            title: 数据暴涨
            chapter: 43
            description: "能力反哺创业，产品大升级，数据暴涨，打脸竞争对手"
            tension: 4
          - beat: 3
            title: 双线作战
            chapter: 46
            description: "竞争对手加大攻势，商业冲突升级，男主用新能力+前世记忆双线作战"
            tension: 4
          - beat: 4
            title: 逆转取胜
            chapter: 49
            description: "关键反击，利用前世记忆的杀手锏，逆转"
            tension: 5
          - beat: 5
            title: 考虑注册公司
            chapter: 50
            description: "阶段性大胜，项目站稳脚跟，考虑正式注册公司"
            tension: 4
    turning_point:
      chapter: 40
      description: "副本内发现微弱自主权，金手指成长体系确立"
      type: midpoint

  - act: 5
    title: "工作室升级 + 新角色"
    chapters: [51, 75]
    arc: "团队成型 + 新角色登场 + 暑期冲刺 + 接触新歌手"
    sequences:
      - sequence: 1
        title: 团队扩张与女主二登场
        chapters: [51, 60]
        beats:
          - beat: 1
            title: 注册公司
            chapter: 51
            description: "注册公司，从个人项目变成正式团队，招人/分工，室友变合伙人"
            tension: 3
          - beat: 2
            title: 业务扩展
            chapter: 54
            description: "从单一产品到多条线，管理挑战初现，男主用前世经验应对"
            tension: 3
          - beat: 3
            title: 女主二登场
            chapter: 57
            description: "女主二登场，因业务关系产生交集，初次碰撞（不一定是正面的），与女主一形成反差"
            tension: 4
      - sequence: 2
        title: 商业冲突与感情推进
        chapters: [61, 75]
        beats:
          - beat: 1
            title: 更大冲突
            chapter: 61
            description: "更大的商业冲突，涉及行业资源争夺，对手可能是本地互联网公司/有背景的竞争者/想收购的大厂"
            tension: 4
          - beat: 2
            title: 感情推进
            chapter: 66
            description: "女主一和男主关系从暧昧到半明确，但阶级问题仍然是暗雷"
            tension: 3
          - beat: 3
            title: 三角苗头
            chapter: 67
            description: "女主二开始对男主产生好奇/好感，三角关系初现苗头"
            tension: 3
          - beat: 4
            title: 暑假冲刺
            chapter: 69
            description: "暑假别人休息他们在拼，关键项目冲刺，同时寻找机会接触新歌手"
            tension: 4
          - beat: 5
            title: 关键合作
            chapter: 73
            description: "拿下关键合作，公司估值上台阶，但更大级别的对手注意到了他们"
            tension: 4
    turning_point:
      chapter: 57
      description: "女主二登场，多女主格局打开"
      type: midpoint

  - act: 6
    title: 卷一高潮
    chapters: [76, 100]
    arc: "最大危机 + 关键抉择 + 感情突破 + 卷末爽点"
    sequences:
      - sequence: 1
        title: 危机与副本破局
        chapters: [76, 88]
        beats:
          - beat: 1
            title: 大对手出手
            chapter: 76
            description: "大对手正式出手，打压/挖人/抄袭/断资源，团队面临分裂危险"
            tension: 5
          - beat: 2
            title: 内忧外患
            chapter: 78
            description: "内部矛盾：室友/合伙人在压力下产生分歧，外部压力：竞争对手有资本支持"
            tension: 5
          - beat: 3
            title: 选歌入梦
            chapter: 84
            description: "男主决定用下一个副本窗口寻找破局关键，精心选歌，入梦第三个副本"
            tension: 4
          - beat: 4
            title: 副本内冒险
            chapter: 86
            description: "热血/未来感副本，男主有了更多自主权，获得关键奖励：商业直觉/战略眼光"
            tension: 4
      - sequence: 2
        title: 逆转与突破
        chapters: [89, 100]
        beats:
          - beat: 1
            title: 制定反击
            chapter: 89
            description: "梦醒获得破局灵感/能力，制定反击计划，利用前世记忆+副本奖励+团队力量多线反攻"
            tension: 4
          - beat: 2
            title: 终极对决
            chapter: 94
            description: "终极对决，男主使出杀手锏，逆转取胜，竞争对手溃败/退让/被收购"
            tension: 5
          - beat: 3
            title: 感情突破
            chapter: 97
            description: "危机过后女主一在关键时刻的支持被男主看到，两人关系实质性突破，从暧昧到明确，名场面"
            tension: 5
          - beat: 4
            title: 卷末钩子
            chapter: 100
            description: "新危机/机会出现，下一首歌的窗口逼近，一个大事件/大人物出现，为卷二埋钩子"
            tension: 5
    turning_point:
      chapter: 94
      description: "终极对决逆转取胜，卷一商战线收束"
      type: climax

# ═══════════════════════════════════════════════════
# 情节线索（跨卷伏笔）
# ═══════════════════════════════════════════════════

plotlines:
  - name: "金手指规则"
    description: "第一卷建立'原作发布前1个月内首次唱出'的规则，第二-三卷逐步揭示更多规则细节（如自主权递增、记忆差等），第四卷男主完全掌握金手指可以主动选择副本和策略"
    importance: primary
    chapters_covered: [1, 500]
  - name: "女主一的真实身份"
    description: "第一卷女主一是隐形富二代阶级落差，第二卷身份逐渐暴露带来新的冲突，第三-四卷身份问题解决感情线收束"
    importance: primary
    chapters_covered: [1, 400]
  - name: "副本奖励的用途"
    description: "第一卷古宅宝藏上报国家（反套路），第二-三卷后续奖励越来越实用（能力/资源/信息），第四卷关键奖励在商业/感情危机中发挥作用"
    importance: primary
    chapters_covered: [1, 500]
  - name: "多女关系协调"
    description: "第一卷女主一登场，第二卷女主二/三登场修罗场初现，第三-四卷多女关系明朗化最终协调"
    importance: primary
    chapters_covered: [1, 500]
  - name: "创业项目"
    description: "第一卷小型互联网项目，第二卷公司扩张遭遇竞争，第三-四卷成为商业帝国"
    importance: primary
    chapters_covered: [1, 500]
  - name: "商业竞争对手"
    description: "第二卷同行竞争，第三卷大资本介入，第四卷最终决战/和解"
    importance: secondary
    chapters_covered: [101, 500]
  - name: "自主权递增"
    description: "第一卷被动跟随剧情，第二卷可以做出选择，第三-四卷高度自主可以改变剧情"
    importance: primary
    chapters_covered: [1, 500]

# ═══════════════════════════════════════════════════
# 钩子网络（章节级，留给 design-chapters 填充）
# ═══════════════════════════════════════════════════

hooks: []

pacing_curve: []
```

- [ ] **Step 3: Validate structure**

验证要点：
- `premise` 是字符串（不是对象）
- `theme: []` 和 `tone: []` 是顶层数组
- `acts[]` 有 6 个 act，每个含 `act`/`title`/`chapters`/`arc`/`sequences`
- 每个 sequence 含 `sequence`/`title`/`chapters`/`beats`
- 每个 beat 含 `beat`/`title`/`chapter`（int）/`description`（≥30字）/`tension`（1-5）
- 每个 act 含 `turning_point`（含 `chapter`/`description`/`type`）
- `plotlines[]` 有 7 条线索，每条含 `name`/`description`/`importance`/`chapters_covered`
- `hooks: []` 和 `pacing_curve: []` 存在但为空
- 无 `premise.themes`、`premise.tones`、`premise.target_chapters`、`premise.structure_note`
- 无 `hooks.core/business/dungeon` 旧结构

- [ ] **Step 4: Commit**

```bash
git add novels/nv_20260625_00t3/settings/outline.yaml
```

Commit message 遵循 commit-msg skill。建议 scope: `settings`，subject: `outline: 拆 premise 为扁平字段，补 acts[] 三幕结构，hooks 重构为 plotlines[]`

---

## Task 4: notes.yaml 拆分 — 创意备忘迁出 + 结构化重建

**Files:**
- Read: `novels/nv_20260625_00t3/settings/notes.yaml` (current, 54 lines)
- Read: `data/schemas/notes.schema.yaml` (reference)
- Modify: `novels/nv_20260625_00t3/settings/notes.yaml`
- Create: `novels/nv_20260625_00t3/references/mechanics.yaml`

**Transformation rules:**

1. 当前 notes.yaml 的全部创意内容（穿越设定/金手指规则/许嵩接触线/入梦机制/梦境奖励示例/自主权成长线）→ 迁移到 `references/mechanics.yaml`，保持原始格式
2. `notes.yaml` 按 Schema 重建：`version: 1` + `tracking` + `preferences`
3. `tracking.foreshadowing[]` 从原 outline.yaml 的 7 条 hooks 转换，status 全部为 `open`

- [ ] **Step 1: Read current notes.yaml**

读取 `novels/nv_20260625_00t3/settings/notes.yaml`，确认包含 6 个段落：`穿越设定`、`金手指规则`、`许嵩接触线`、`入梦机制`、`梦境奖励示例`、`自主权成长线`。

- [ ] **Step 2: Write references/mechanics.yaml**

```yaml
# 核心机制设定
# 从 settings/notes.yaml 迁出
# 包含：穿越规则、金手指机制、接触线、入梦机制、奖励、自主权成长

# 用户补充设定 (2026-06-25)
穿越设定:
  穿越时间: "2009年12月"
  穿越类型: "重生回过去，不是平行世界"
  记忆: "男主保留前世完整记忆，包括所有歌曲"
  限制: "不能做传统文抄公（歌本来就是别人的，会暴露）"
  学校: "合肥工业大学（计算机系大一）"
  女主学校: "中国科学技术大学"
  备注: "合肥几所大学距离很近，跨校串门、偶遇都很自然"

金手指规则:
  条件1: "在原作发布前一个月内唱出"
  条件2: "必须是第一次唱"
  条件3: "必须与歌手有现实接触（同处一个空间/看到本人/一起吃饭等都算）"
  触发: "两个条件同时满足才能触发入梦"
  限制: "错过窗口期 = 永久失效"
  解锁: "接触一位歌手 = 解锁该歌手全部歌曲（各歌窗口期独立计算）"
  策略: "选歌 = 选副本 = 选节奏，需要配合真实发行时间线规划"
  剧情驱动: "接触歌手是剧情驱动线：每个新歌手都是一条冒险/任务线"

许嵩接触线:
  时间: "2009年12月"
  背景: "许嵩刚发《自定义》专辑不久，在圈内小有名气但还没爆红"
  过程:
    - "男主周末去找高中同学(安农大)玩"
    - "听说许嵩回安医大做小演出"
    - "大家一起去看"
    - "演出结束后聚餐"
    - "女主(中科大，高中同学)也到场"
    - "散场时男主有感而发，唱起《庐州月》"
    - "被女主听到"
    - "入梦触发"
  备注: "看演出+聚餐本身就是一次完整的接触过程"

入梦机制:
  触发条件: "男主唱歌被女主听到，才会一起入梦"
  第一首歌: "庐州月（许嵩）"
  记忆规则: "男主清晰记住梦境，其他人只有模糊印象（角色越重要印象越深）"

梦境奖励示例:
  庐州月副本:
    奖励: "获得庐州古宅宝藏"
    处理: "文物禁止买卖，上报国家"
    结果: "男主泪崩"
    说明: "这个例子说明：奖励不一定好用，增加现实冲突和喜剧效果"

自主权成长线:
  初期: "无自主权，被动跟随歌曲剧情"
  中期: "有限选择权，可影响关键节点"
  后期: "高度自主权，可改变故事结局"
```

- [ ] **Step 3: Write restructured notes.yaml**

```yaml
# 项目备忘与长篇上下文追踪
# Schema: data/schemas/notes.schema.yaml
# 核心机制设定已迁至 references/mechanics.yaml

version: 1

tracking:
  recent_chapters: []

  ten_chapter_summaries: []

  volume_overview:
    - volume: 1
      goal: "重生回归 + 初恋重逢 + 第一桶金"
      current_state: "未开始"

  character_states: []

  foreshadowing:
    - id: f001
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 400
      note: "金手指规则 — 第一卷建立规则，第二-三卷揭示细节，第四卷完全掌握"
    - id: f002
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 350
      note: "女主一的真实身份 — 第一卷隐形富二代，第二卷身份暴露，第三-四卷收束"
    - id: f003
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 400
      note: "副本奖励的用途 — 第一卷上报国家，后续奖励越来越实用，第四卷关键奖励发挥作用"
    - id: f004
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 400
      note: "多女关系协调 — 第一卷女主一，第二卷女主二三登场，第三-四卷明朗化"
    - id: f005
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 400
      note: "创业项目 — 第一卷小项目，第二卷扩张，第三-四卷商业帝国"
    - id: f006
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 400
      note: "商业竞争对手 — 第二卷同行竞争，第三卷大资本，第四卷决战"
    - id: f007
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 400
      note: "自主权递增 — 第一卷被动跟随，第二卷有限选择，第三-四卷高度自主"

preferences:
  style_notes: []
  banned_settings: []
  pending_confirmations: []
```

- [ ] **Step 4: Validate structure**

验证要点：
- `notes.yaml`：顶层有 `version: 1`、`tracking`、`preferences`
- `tracking` 含 `recent_chapters`/`ten_chapter_summaries`/`volume_overview`/`character_states`/`foreshadowing` — 全部存在
- `foreshadowing` 共 7 条，每条含 `id`/`planted_chapter`/`status`/`planned_resolution_chapter`/`note`
- 所有 `status` 值为 `open`（枚举 `open/resolved/dropped` 之一）
- `preferences` 含 `style_notes`/`banned_settings`/`pending_confirmations` — 全部为空数组
- 无旧内容（穿越设定/金手指规则/许嵩接触线等已迁走）
- `references/mechanics.yaml` 包含原 notes.yaml 的全部 6 个段落，内容完整

- [ ] **Step 5: Commit**

```bash
git add novels/nv_20260625_00t3/settings/notes.yaml novels/nv_20260625_00t3/references/mechanics.yaml
```

Commit message 遵循 commit-msg skill。建议 scope: `settings`，subject: `notes: 创意备忘迁至 references/mechanics.yaml，重建结构化追踪骨架`

---

## Task 5: 目录修复 + 收尾

**Files:**
- Delete: `novels/nv_20260625_00t3/content/chapters/` (empty directory)
- Create: `novels/nv_20260625_00t3/settings/chapter_outlines/.gitkeep`

- [ ] **Step 1: Remove deprecated content/chapters/ directory**

```bash
rmdir novels/nv_20260625_00t3/content/chapters/
```

Expected: Directory removed (it is empty, no files lost).

- [ ] **Step 2: Create settings/chapter_outlines/ directory**

```bash
mkdir -p novels/nv_20260625_00t3/settings/chapter_outlines/
touch novels/nv_20260625_00t3/settings/chapter_outlines/.gitkeep
```

- [ ] **Step 3: Verify directory structure**

```bash
find novels/nv_20260625_00t3/ -type f | sort
```

Expected output includes:
- `project.yaml`
- `template.yaml`
- `REFACTOR_SUMMARY.md`
- `settings/scout_report.yaml`
- `settings/worldbuilding.yaml`
- `settings/characters.yaml`
- `settings/outline.yaml`
- `settings/arcs.yaml`
- `settings/pacing.yaml`
- `settings/chapters_index.yaml`
- `settings/notes.yaml`
- `settings/chapter_outlines/.gitkeep`
- `references/mechanics.yaml`
- `references/design_principles.yaml`
- `references/2009_era_details.yaml`
- `references/songs_timeline.yaml`
- `references/dungeons/001_庐州月.yaml`
- `references/business/internet_2009_2015.yaml`
- `references/locations/hefei_universities.yaml`
- `references/locations/hfut_campus.yaml`
- `references/novels/_index.yaml`

Expected **NOT** in output:
- `content/chapters/` (deleted)

- [ ] **Step 4: Commit**

```bash
git add -A novels/nv_20260625_00t3/
```

Commit message 遵循 commit-msg skill。建议 scope: `settings`，subject: `chore: 删除废弃 content/chapters/，新建 chapter_outlines/ 蓝图目录`

---

## Task 6: 最终验证

**Files:**
- All modified files in `novels/nv_20260625_00t3/`

- [ ] **Step 1: Review git log**

```bash
git log --oneline -7
```

Expected: 5 new commits (plus the spec commit), each touching the correct files.

- [ ] **Step 2: Verify Schema field coverage**

For each file, check that the Schema-required fields exist:

| File | Required Fields to Verify |
|------|--------------------------|
| `worldbuilding.yaml` | `world_type`, `power_system.name`, `power_system.ranks` (≥3), `factions` (≥1), `locations` (≥1) |
| `characters.yaml` | `characters[]`, each protagonist has `traits`/`psychology`/`arc`, each antagonist has `traits`/`psychology`/`arc` |
| `outline.yaml` | `premise` (string, ≥20 chars), `theme[]`, `acts[]` (≥3, each with `sequences[]` ≥2, each sequence with `beats[]` ≥5) |
| `notes.yaml` | `version: 1`, `tracking.recent_chapters`, `tracking.foreshadowing[]` with valid `status` enum |

- [ ] **Step 3: Content integrity check**

Verify zero content loss:

1. **worldbuilding.yaml**: `university_life` section exists with `academics`/`campus_culture`/`tech_environment`/`career_landscape`. `social_context` exists with `economy`/`culture`/`technology`. `foreknowledge_advantages` exists with `business_opportunities`/`tech_advantages`/`cultural_advantages`.

2. **characters.yaml**: 8 characters in `characters[]`. Protagonist has all psychology fields. Heroine 1 has `romance_arc` with turning_points. Heroine 2/3 marked as 待定. Both supporting characters present. Both antagonists present with psychology/arc skeletons.

3. **outline.yaml**: `premise` string matches original `statement`. All 7 plotlines present. 6 acts with correct chapter ranges.

4. **references/mechanics.yaml**: Contains all 6 sections from original notes.yaml (穿越设定/金手指规则/许嵩接触线/入梦机制/梦境奖励示例/自主权成长线).

5. **references/design_principles.yaml**: Contains all 5 principles (P001-P005).

- [ ] **Step 4: Run check-notes.js gate script**

```bash
node .agents/skills/_shared/scripts/check-notes.js novels/nv_20260625_00t3/settings/notes.yaml
```

Expected: Exit code 0 (pass). This validates `foreshadowing.status` enum values.

- [ ] **Step 5: Done**

All 5 commits complete. Schema alignment verified. No content lost.
