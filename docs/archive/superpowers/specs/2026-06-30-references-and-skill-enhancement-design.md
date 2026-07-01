# References 移植 + SKILL.md 加厚设计

## 概述

从 oh-story-claudecode 移植 10 个核心 references 文件到对应 skill，并加厚 4 个 SKILL.md 的流程密度，使 agent 有深度方法论可读、skill 流程能指导具体执行。

**核心决策**：
- References：合并适配（以 oh-story 为蓝本，调整路径引用，与现有 references 去重）
- SKILL.md：全部 4 个 skill 都加厚（从要点级别到可执行级别）
- 执行顺序：先 references → 再 SKILL.md → 最后更新 agent 定义
- Commit 策略：按 skill 分组（不再每个文件单独 commit）

---

## References 移植方案

### 移植清单

10 个文件全部需要新增（与现有 references 无重名冲突），总计 ~3,148 行：

| # | 文件 | 行数 | 目标 skill | 内容 |
|---|------|------|-----------|------|
| 1 | `writing-craft.md` | 383 | daily-write | 写作技法大全（三维度揉进、身体细节、物件三次出现、疏密分配、长短句、视角姿态） |
| 2 | `dialogue-mastery.md` | 282 | daily-write | 对话方法（潜台词、权力博弈、信息控制、7维差异化、自查清单） |
| 3 | `emotional-methods.md` | 179 | daily-write | 情绪技法（情绪引擎、情绪节拍、拉扯节奏） |
| 4 | `style-craft.md` | 347 | daily-write | 风格技法（打斗写法、装逼写法、日常写法） |
| 5 | `hooks-paragraph.md` | 146 | daily-write | 段落级钩子（段内悬念/好奇驱动，与现有章级 hooks-guide 互补） |
| 6 | `format-and-structure.md` | 178 | daily-write | 格式规范（段落节奏、语气标点谱系、手机阅读密度） |
| 7 | `plot-core-methods.md` | 542 | design-outline | 情节核心方法（高潮构建蓄能→假胜→崩解、AB交织、连续性追踪） |
| 8 | `reversal-toolkit.md` | 361 | design-outline | 反转设计（7种类型、嵌套反转、误导技巧、自检清单） |
| 9 | `opening-design.md` | 345 | golden-chapters | 开篇设计（黄金三章法则、9种开头技巧、开头选择决策树） |
| 10 | `character-relations.md` | 385 | design-character | 关系设计（四种关系类型、好感度体系、男女频差异，与现有 relationship-network 互补） |

### 路径调整规则

oh-story 的 reference 路径格式改为我们的格式：

```
oh-story:  story-setup/references/agent-references/{file}
我们:      .agents/skills/{skill-name}/references/{file}
```

具体调整：
1. 文件内容主体不动（方法论本身通用）
2. 文件内引用其他 reference 的路径改为我们的格式
3. 去掉 oh-story 特有的 agent frontmatter 字段（`memory`、`model` 等）

### 移植后各 skill 的 references 变化

| Skill | 移植前 | 移植后 | 新增 |
|-------|--------|--------|------|
| daily-write | 6 | 12 | +6 |
| design-outline | 5 | 7 | +2 |
| design-character | 5 | 6 | +1 |
| golden-chapters | 4 | 5 | +1 |

---

## SKILL.md 加厚方案

核心原则：从「做什么」加厚到「怎么做」，每个 Phase 从 2-5 行变为 10-30 行，具体到可执行级别，并引用新的 references。

### daily-write（228 → ~420 行）

**Phase 3 写作执行**（20 行 → 100 行）：

```
Phase 3：写作执行

入口条件：上下文加载完成
目标：按细纲生成正文

步骤：
1. 写前准备
   1.1 状态筛选：从追踪文件筛选本章涉及角色的当前状态、待回收伏笔
   1.2 模块召回：读取 references/emotional-methods.md，确定本章情绪引擎
   1.3 文风确认：如有文风文件/上下文.md 文风指纹，按目标句长带写作
   1.4 意图确认：用一句话概括本章节奏和情绪目标

2. 写作
   2.1 按三维度揉进写场景（参考 references/writing-craft.md 第 8 节）
       - 深度限知视角：锁死主视角角色的此刻感知
       - 发生+感知+反应织在同一段
       - 画面分段：按新动作/新物件/新信息断段
   2.2 对话按语言风格档案差异化（参考 references/dialogue-mastery.md）
       - 潜台词与信息控制
       - 权力模式（谁在掌控节奏）
       - 逐句情绪承接
   2.3 情绪弧线执行（参考 references/emotional-methods.md）
       - 情绪烈度：爽点要狠要具体，敢写极端反应
       - 拉扯节奏：有回落再升
   2.4 格式遵守（参考 references/format-and-structure.md）
       - 段落间无空行（\n 不是 \n\n）
       - 不用省略号/破折号
       - 标点服务语气

3. 字数验证（写完第一件事）
   3.1 wc -m 统计实际字数
   3.2 不足章目标 90% → 定位欠账的密点，一次性重写到配额
   3.3 超过章目标×1.1 → 压过场、合并疏点

出口条件：正文已生成，字数达标
加载 References：writing-craft.md, dialogue-mastery.md, emotional-methods.md, format-and-structure.md
```

**Phase 4/5 微调**：引用新的 references（style-craft.md 用于风格检查，hooks-paragraph.md 用于段落级钩子检查）。

### design-outline（174 → ~320 行）

**加厚内容**：

- Phase 3-4 加入：卷级大纲模板、细纲蓝图模板（内容概括五段式 + 情节安排多线 + 人物关系出场顺序 + 情节细化 + 结尾设定）、大纲五检清单（① 情绪交付 ② 核心冲突 ③ 卷节奏 ④ 伏笔 ⑤ 章节定位分布）、对标节奏回流
- 引用新 references：plot-core-methods.md（高潮构建）、reversal-toolkit.md（反转设计）

### design-character（198 → ~310 行）

**加厚内容**：

- Phase 2 加入：主角设计流程（三层标签 → 九维深化 → 动机链 → 语言风格档案）、语言风格档案 7 维度建立步骤
- Phase 3 加入：反派层级设计流程（小反派→中等反派→大弧Boss→最终Boss）、镜像关系设计
- Phase 4 加入：关系网络建立流程（四种关系类型 + 好感度阶段 + 关系弧线）
- 引用新 references：character-relations.md

### golden-chapters（211 → ~310 行）

**加厚内容**：

- Phase 1 加入：品类适配检查清单、开篇策略选择决策树
- Phase 2-4 加入：单章锻造检查清单（前100字事件密度、核心展示、章尾钩子）、微节拍对照、品类差异化要求
- 引用新 references：opening-design.md

### 加厚前后对比

| Skill | 加厚前 | 加厚后 | 主要加厚点 |
|-------|--------|--------|-----------|
| daily-write | 228 行 | ~420 行 | Phase 3 从 20 行 → 100 行（13 步写作流程） |
| design-outline | 174 行 | ~320 行 | 卷级大纲模板 + 细纲蓝图 + 五检清单 |
| design-character | 198 行 | ~310 行 | 主角/反派/配角设计流程 + 语言风格档案步骤 |
| golden-chapters | 211 行 | ~310 行 | 品类适配 + 单章锻造检查 + 开篇策略决策树 |

---

## Agent 定义更新

移植完 references 后，3 个 agent 定义文件的「参考文件体系」表格同步更新：

| Agent | 当前 references 数 | 新增条目 |
|-------|-------------------|---------|
| narrative-writer | 8 | +6（writing-craft, dialogue-mastery, emotional-methods, style-craft, hooks-paragraph, format-and-structure） |
| story-architect | 13 | +2（plot-core-methods, reversal-toolkit） |
| character-designer | 6 | +1（character-relations） |
| consistency-checker | 2 | 不变 |

---

## 交付清单

| 类别 | 数量 | 说明 |
|------|------|------|
| 新增 reference 文件 | 10 个 | 从 oh-story 移植+路径调整 |
| 修改 SKILL.md | 4 个 | 加厚流程到可执行级别 |
| 修改 agent 定义 | 3 个 | 同步 references 表 |
| **总计** | **17 个文件** | |

---

## 执行顺序

```
Step 1: 移植 10 个 references
  - daily-write ×6（writing-craft, dialogue-mastery, emotional-methods, style-craft, hooks-paragraph, format-and-structure）
  - design-outline ×2（plot-core-methods, reversal-toolkit）
  - design-character ×1（character-relations）
  - golden-chapters ×1（opening-design）

Step 2: 加厚 4 个 SKILL.md
  - daily-write（Phase 3 加厚到 100 行）
  - design-outline（加入卷级大纲+细纲蓝图+五检）
  - design-character（加入主角/反派/配角设计流程）
  - golden-chapters（加入品类适配+锻造检查+开篇策略）

Step 3: 更新 3 个 agent 定义的 references 表

Step 4: 验证（所有 reference 引用解析正确）
```

---

## Commit 策略

按 skill 分组 commit：

```
feat(daily-write): 移植 6 个核心 references + 加厚 SKILL.md Phase 3
feat(design-outline): 移植 2 个 references + 加厚 SKILL.md
feat(design-character): 移植 1 个 reference + 加厚 SKILL.md
feat(golden-chapters): 移植 1 个 reference + 加厚 SKILL.md
feat(agents): 同步 agent 定义文件的 references 表
```

---

## 不在范围内

- novel-material 增强（拆文能力整合到 novel-material，不在本项目做）
- Hooks 实现（后续迭代）
- 新增 skill（如拆文 skill、路由入口 skill）
- 新增 agent（story-explorer/story-researcher/chapter-extractor）
