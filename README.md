# AI 小说写作系统

面向长篇连载与多项目管理的写作工作台。  
你可以把它当成“小说生产系统”：既能写内容，也能管章节、关系、素材、风格与风险。

---

## 角色导航（先看这里）

| 你是谁 | 先看文档 | 先跑 3 个命令 |
|------|---------|---------------|
| 作者（专注写作） | `README-AUTHOR.md` | `/novel-switch` → `/chapter-create` → `/chapter-review` |
| 编辑/主编（控进度风险） | `README-EDITOR.md` | `/chapter-board` → `/project-weekly-report 最近7天 --view manager` → `/novel-kpi 最近30天` |
| 新人/搭建者（看全貌） | `README.md` + `docs/SPEC.md` | `/novel-init` → `/novel-status` → `/novel-doctor` |

---

## Harness 导航（文档整理入口）

- 总索引：`docs/index.md`
- Agent 地图：`AGENTS.md`
- 架构边界：`ARCHITECTURE.md`
- 项目命令总览：`README.md`（见“命令清单（必用版 + 完整版）”）
- 写作工作台笔记：`writing.md`

---

## 能力地图（README 版）

> 一句话理解：从“写出来”到“写得稳、可复盘、可扩展”。

| 能力域 | 解决什么问题 | 代表命令 |
|------|--------------|---------|
| 项目与运营 | 多书管理、周报复盘、健康体检 | `/novel-switch` `/novel-doctor` `/project-weekly-report` `/novel-kpi` |
| 流程编排 | 把常用写作流程打包成场景预设，少记命令 | `/pipeline-outline-bootstrap` `/pipeline-chapter-kickoff` `/pipeline-draft-polish` `/pipeline-compliance-gate`（共 6 个） |
| 章节生产 | 新章创建、状态推进、结构打磨 | `/chapter-create` `/chapter-update` `/chapter-review` `/chapter-board` |
| 角色关系 | 角色设定、关系维护、关系演进与跳变检查 | `/character-add` `/relationship-log` `/relationship-evolution` `/relationship-check` |
| 素材资产 | 素材入库、切片索引、剧情/人物检索 | `/material-add` `/material-chunk` `/material-search-plot` `/material-search-character` |
| 文风质量 | 去 AI 感、人物对白区分、风格调优 | `/anti-ai-check` `/anti-ai-rewrite` `/voice-check` `/rewrite` |
| 合规风控 | 借鉴留痕、风险检查、阶段报告 | `/inspiration-log` `/inspiration-check` `/inspiration-report` |

如果你是新用户，建议先只用三个域：

1. 章节生产（先把内容写出来）
2. 素材资产（卡文时能快速找到支撑）
3. 文风质量（出稿前做最低限度质检）

---

## 这套系统适合谁

- 同时写多本书，需要频繁切换项目的人
- 连载作者，需要稳定推进章节与节奏的人
- 有素材积累习惯，希望做检索和复用的人
- 在意“去 AI 感”、借鉴风险、人物一致性的人

---

## 快速开始（5 分钟）

```bash
# 1) 创建项目
/novel-init 《书名》 类型

# 2) 初始化剧情结构
/plot-init 三幕式

# 3) 添加主角色
/character-add 张三 主角 25岁 剑客 隐忍坚毅

# 4) 创建第一章
/chapter-create ch001 主角在危机中被迫离开故土

# 5) 开始写作前检查
/novel-status
```

---

## 极简日常命令（高频）

如果你只想先跑通写作，不用所有技能，优先这 8 个：

- `/novel-switch`：切换项目
- `/chapter-create`：创建章节
- `/chapter-update`：推进章节状态
- `/chapter-review`：审查章节结构/节奏
- `/material-search`：按需求找素材
- `/character-edit`：补充角色设定
- `/anti-ai-check`：检查 AI 痕迹
- `/consistency-check`：阶段性一致性体检

---

## Pipeline 预设（不想自己拼命令时）

如果你已经知道自己要做什么，但不想手动串命令，可以直接用这 6 个预设：

| 场景 | 预设命令 | 止点 |
|------|---------|------|
| 从一句话想法到可写大纲 | `/pipeline-outline-bootstrap [premise]` | `可写大纲` |
| 补强已有大纲与设定支撑 | `/pipeline-outline-polish [focus]` | `可写大纲` |
| 从章节想法到可开写章节 | `/pipeline-chapter-kickoff [chapter_id] [goal]` | `可开写章节` |
| 从草稿到一轮高收益修订 | `/pipeline-draft-polish [chapter_id]` | `可修订草稿` |
| 做阶段性连续性闸口 | `/pipeline-continuity-gate [range]` | `可执行修复清单` |
| 做发布前合规闸口 | `/pipeline-compliance-gate [chapter_or_range]` | `可发前闸口` |

配套补强命令：

- `/plot-review [focus]`：先查大纲结构、节奏、伏笔再优化
- `/worldbuilding-review [focus]`：先查设定是否服务剧情、是否自洽

---

## 命令清单（必用版 + 完整版）

### 必用版（10个，日常优先）

1. `/novel-switch [项目名]`：切换当前写作项目。  
2. `/novel-status`：查看当前项目状态。  
3. `/chapter-create [章节ID] [目标]`：新建章节并初始化元数据。  
4. `/chapter-update [章节ID] --status [状态]`：推进章节状态。  
5. `/chapter-review [章节ID]`：审查章节并给修订建议。  
6. `/material-search [关键词]`：卡文时检索素材。  
7. `/character-edit [角色名] [修改内容]`：修正角色设定。  
8. `/anti-ai-check [章节ID]`：检测 AI 痕迹。  
9. `/consistency-check`：全项目一致性检查。  
10. `/novel-doctor`：项目健康诊断。  

---

### 完整版（按能力域）

#### Pipeline 编排

- `/pipeline-outline-bootstrap [premise]`：从想法启动大纲并产出可写骨架。  
- `/pipeline-outline-polish [focus]`：补强现有大纲、节奏与设定支撑。  
- `/pipeline-chapter-kickoff [章节ID] [目标]`：创建章节并补齐开写前的章节节点。  
- `/pipeline-draft-polish [章节ID]`：打包完成章节审查、人物声音检查与去 AI 感处理。  
- `/pipeline-continuity-gate [范围]`：输出关系/时间线/一致性修复清单。  
- `/pipeline-compliance-gate [章节ID或范围]`：完成借鉴留痕与合规闸口汇总。  

#### 项目管理

- `/novel-init [书名] [类型]`：创建新项目并初始化结构。  
- `/novel-switch [项目名]`：切换当前项目。  
- `/novel-status`：查看当前项目详情。  
- `/novel-list`：查看全部项目。  
- `/novel-doctor`：检查项目结构与索引健康度。  
- `/project-weekly-report [范围] [--view ...]`：生成周报（管理者/作者/双视角）。  
- `/novel-kpi [范围]`：计算核心 KPI（完稿率、返工率、风险消解率等）。  

#### 章节管理

- `/chapter-create [章节ID] [目标]`：创建章节与章节索引条目。  
- `/chapter-update [章节ID] ...`：更新状态、标题、字数、POV。  
- `/chapter-board [--status]`：查看章节看板和堆积。  
- `/chapter-review [章节ID]`：章节结构/节奏/行为一致性审查。  

#### 角色与关系

- `/character-add [姓名] [定位] [年龄]...`：创建角色卡。  
- `/character-edit [姓名] [修改]`：编辑角色信息。  
- `/character-query [查询]`：查询角色。  
- `/relationship-add [角色1] [角色2] [关系]`：建立关系。  
- `/relationship-map [角色名]`：查看关系图谱。  
- `/relationship-log [角色1] [角色2] [变化] --chapter ...`：记录关系演进事件。  
- `/relationship-evolution [角色名]`：查看关系时间轨迹。  
- `/relationship-check`：检查关系跳变与逻辑断裂。  

#### 剧情与时间线

- `/plot-init [结构]`：初始化剧情结构。  
- `/plot-add [章节] [内容]`：添加情节节点。  
- `/plot-review [focus]`：审查大纲结构、节奏、转折与伏笔安排。  
- `/plot-suggest [描述]`：生成剧情建议。  
- `/timeline-add [时间] [事件]`：添加时间线事件。  
- `/timeline-check`：检查时间冲突。  
- `/timeline-view [范围]`：查看时间线。  

#### 世界观与设定

- `/worldbuilding-review [focus]`：审查世界规则、势力、地理与剧情支撑度。  

#### 素材与标签

- `/material-add [路径]`：素材入库。  
- `/material-search [关键词]`：通用素材检索入口。  
- `/material-style [素材]`：提取素材风格。  
- `/material-chunk [素材ID]`：素材分段索引。  
- `/material-index-plot [素材ID]`：建立剧情索引。  
- `/material-index-character [素材ID]`：建立人物索引。  
- `/material-search-plot [剧情需求]`：按剧情需求检索。  
- `/material-search-character [人物需求]`：按人物需求检索。  
- `/material-retag [素材ID] [标签...]`：重设素材标签。  
- `/tag-add [标签] --group ...`：新增规范标签。  
- `/tag-merge [旧标签] [新标签]`：合并同义标签。  

#### 写作风格与去 AI 感

- `/style-list`：查看风格模板。  
- `/style-create [名称] [特征]`：创建风格模板。  
- `/rewrite [内容] --style [风格]`：按风格改写文本。  
- `/anti-ai-check [章节ID]`：检测 AI 痕迹并评分。  
- `/anti-ai-rewrite [章节ID] --level [1-3]`：去 AI 感改写。  
- `/voice-check [角色名] [范围]`：检查人物对白区分度。  

#### 合规与一致性

- `/inspiration-log [章节ID] [素材ID] [借鉴点]`：登记借鉴来源。  
- `/inspiration-check [章节ID]`：检查借鉴风险。  
- `/inspiration-report [范围]`：输出借鉴与风险报告。  
- `/consistency-check`：跨模块一致性总检查。  

---

## 经典工作流程（按场景）

### 1) 切换书继续写

```bash
/novel-list
/novel-switch 仙途
/novel-status
```

适用：今天想从 A 书切到 B 书继续推进。

---

### 2) 新开一章（从空白到可写）

```bash
/chapter-create ch012 主角误入敌营并发现旧友背叛
/chapter-update ch012 --status outline
/plot-add 第12章 冲突升级，尾部埋设“身份反转”伏笔
```

适用：每次新章开工。

---

### 3) 写完草稿后快速打磨

```bash
/chapter-update ch012 --status draft
/chapter-review ch012
/chapter-update ch012 --status revise
```

适用：希望从“能看”到“可发”。

---

### 4) 卡文时找剧情灵感

```bash
/material-search-plot 中段需要一次高强度反转，且不破坏主线动机
/material-search 反转 背刺 误会解除
```

适用：不知道下一场戏怎么转。

---

### 5) 角色写崩前做关系校准

```bash
/relationship-log 张三 李四 因误会关系降温 --chapter ch012
/relationship-evolution 张三
/relationship-check
```

适用：角色关系变化频繁、担心突兀。

---

### 6) 新素材入库并建立可检索索引

```bash
/material-add ./素材/参考小说A.txt --type novel --tag 玄幻,热血
/material-chunk mat_001
/material-index-plot mat_001
/material-index-character mat_001
```

适用：拿到新参考文本后，做“可复用资产化”。

---

### 7) 标签治理（素材越多越重要）

```bash
/tag-add 宗门 --group 场景 --alias 门派
/tag-merge 门派 宗门
/material-retag mat_001 宗门,权力斗争,师徒
```

适用：素材库变大后，防止标签失控。

---

### 8) 去 AI 感专项修文

```bash
/anti-ai-check ch012
/anti-ai-rewrite ch012 --level 2
/voice-check 张三 ch001-ch012
```

适用：文本“像机器写的”、角色说话同质化。

---

### 9) 借鉴合规闭环

```bash
/inspiration-log ch012 mat_001 借鉴冲突节奏，不复用表达
/inspiration-check ch012
/inspiration-report ch001-ch012
```

适用：发布前做风险审查和留痕。

---

### 10) 每周运营复盘（主编/作者双视角）

```bash
/project-weekly-report 最近7天 --view both
/novel-kpi 最近30天
```

适用：周更复盘、查进度、查风险、定下周动作。

---

### 11) 大版本发布前总检查

```bash
/novel-doctor
/consistency-check
```

适用：阶段性收束、准备连发前。

---

## 推荐节奏（轻量）

- 每天：`chapter-create -> 写作 -> chapter-review`
- 每 2-3 天：`relationship-check` 或 `anti-ai-check`
- 每周：`project-weekly-report` + `novel-kpi`
- 每个里程碑：`novel-doctor` + `consistency-check`

---

## 常见问题

### Q1：Skill 太多，会不会很重？

不会。把它们当“按需工具箱”。  
大多数写作日，你只会用 3-5 个高频命令。

### Q2：没有当前项目怎么办？

先创建或切换项目：

```bash
/novel-init 《书名》 类型
# 或
/novel-switch 项目名
```

### Q3：指标算不出来怎么办？

系统会按统一规则输出 `N/A`，并提示缺哪个数据文件。  
口径见：`.claude/skills/reference-reporting.md`

---

## 进一步阅读

- 作者极简版：`README-AUTHOR.md`
- 编辑/主编版：`README-EDITOR.md`
- Pipeline 编排规格：`docs/product-specs/novel-pipeline.md`
- 设计规范：`docs/SPEC.md`
- 业务扩展蓝图：`docs/BUSINESS-EXPANSION.md`
- 项目命令总览：`README.md`（见“命令清单（必用版 + 完整版）”）
