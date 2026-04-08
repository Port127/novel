# 使用指南：按场景找命令

> 不用记全部命令。找到你当前的场景，照着做。

---

## 一、你不用打字——文件就是输入

大多数命令支持直接引用文件或选中文本，不用手打参数。

### 打开章节文件就自动识别

章节类命令（`chapter-review`、`anti-ai-check`、`anti-ai-rewrite`、`chapter-update`、`voice-check`）支持**自动推断**：

```
打开 chapters/ch005.md → 直接说"帮我审查这个章节"
```

不需要 `/chapter-review ch005`，AI 会从你当前打开的文件推断章节 ID。如果你同时开了多个文件，会优先用当前聚焦的那个。

### 用 `--from` 引用文件内容

`setting-add`、`character-add`、`plot-add` 支持 `--from` 参数，直接从文件或选中内容提取信息：

**从章节中提取角色：**
```bash
/character-add --from chapters/ch003.md
```
自动扫描章节中出场的角色，提取姓名、身份、性格，逐个确认后创建。

**从草稿中提取设定：**
```bash
/setting-add --from drafts/worldview-notes.md
```
从笔记文件中识别设定要素，每条拆开让你确认。

**从灵感文件中提取情节：**
```bash
/plot-add --from drafts/plot-ideas.md
```
识别关键事件和冲突点，自动推断插入位置。

**选中文本直接用：**
选中编辑器里的一段文字，然后说"把选中的内容加到设定里"——等同于 `/setting-add --from "选中的文本"`。

**组合使用：**
```bash
/setting-add --from chapters/ch005.md --quick
```
从章节里提取设定，跳过确认，全部标记为 tentative 快速落地。

### 写了一个杂乱的笔记文件，什么都有

最强的文件输入方式——混合笔记分拣：

```bash
/pipeline-note-triage drafts/braindump.md
```

不管你的文件里混了多少种内容（设定、角色、剧情、时间线、关系、写作备忘），AI 会自动分拣，给你一张分类表，确认后批量落地到对应位置。灵感爆发时加 `--quick` 跳过逐条确认。

---

## 二、一章正文的完整节奏（从开工到归档）

> 先看全貌，再按场景找命令。

写一章正文不是"打开文件就写"——它有节奏。下面是一章从无到有的完整生命线：

```mermaid
flowchart LR
    kickoff["1. 开工"] --> research["2. 找素材"]
    research --> drafting["3. 写草稿"]
    drafting --> polish["4. 打磨"]
    polish --> revise["5. 修订"]
    revise --> gate["6. 质检"]
    gate --> publish["7. 归档发布"]
```

章节状态会随着你的推进自动变化：

```
idea → outline → draft → revise → final → published
```

所有正文都写在 `chapters/ch001.md` 的「正文草稿」区域。`drafts/` 目录是原始脑暴素材，不是章节草稿。

---

### 1. 开工：创建章节，填充骨架

```bash
/pipeline-chapter-kickoff ch001 主角在觉醒现场被误判为三阶空间系
```

**做了什么：** 创建章节文件 + 填充场景大纲 + 补齐对应的大纲情节点。
**改了什么文件：** `chapters/ch001.md`、`chapters/index.yaml`、`plot/outline.md`
**状态变化：** `idea → outline`
**产出：** 一个有场景骨架的章节文件，可以直接开写。

---

### 2. 找素材：检索参考场景，融合到写作中

```bash
# 搜一下类似场景
/material-search 觉醒现场 误判身份 众人围观

# 找到好的参考，融合技法到本章
/material-search apply #1 draft ch001
```

**做了什么：** 从素材库检索参考场景，提取开场技法、冲突结构、对白技巧，写入章节的写作备忘区域。
**改了什么文件：** `chapters/ch001.md`（写作备忘区域）
**状态变化：** 不变，仍是 `outline`
**产出：** 章节文件里多了一段参考技法笔记，写的时候可以参照。

> 这一步可选。没有素材库也可以直接写。

---

### 3. 写草稿：动笔（手写或 AI 辅助）

**方式 A：自己写**

直接打开 `chapters/ch001.md`，在「正文草稿」区域写正文。写完后手动推进状态：

```bash
/chapter-update ch001 --status draft
```

**方式 B：AI 辅助出初稿**

```bash
/chapter-draft ch001 --pov-deep
```

AI 基于大纲、角色设定和世界观生成初稿，写入「正文草稿」区域。初稿是可编辑起点，不是成品。

**改了什么文件：** `chapters/ch001.md`（正文草稿区域）
**状态变化：** `outline → draft`
**产出：** 一份有完整正文的章节草稿。

---

### 4. 打磨：结构审查 + 声音检查 + 去 AI 感

```bash
/pipeline-draft-polish ch001
```

**做了什么：** 一键打包执行四件事——
- 结构审查（开场/冲突/钩子是否到位）
- 人物声音检查（对白是否同质化）
- 设定依赖检查（引用的设定是否已确认）
- 去 AI 感检查与定向改写

**改了什么文件：** `chapters/ch001.md`（高风险片段会给出替换建议）
**状态变化：** `draft → revise`
**产出：** 一份带修订建议的可修订草稿，以及 3-5 条按优先级排序的改文清单。

> 如果只想做其中一项，也可以单独调用：
> - `/chapter-review ch001` — 只看结构
> - `/voice-check 赵宋 ch001` — 只查对白
> - `/anti-ai-check ch001` — 只查 AI 痕迹

---

### 5. 修订：根据反馈改文

这一步是**你自己改**。根据打磨阶段的修订建议，逐条修改正文。

改完后，确认本章达到终稿标准：

```bash
/chapter-update ch001 --status final
```

**改了什么文件：** `chapters/ch001.md`（你手动改正文）
**状态变化：** `revise → final`
**产出：** 终稿。

> 如果改完觉得还不够好，可以再跑一轮 `/pipeline-draft-polish`，不用急着推到 `final`。

---

### 6. 质检：阶段性体检（攒几章一起做）

不用每章都做。攒 5-10 章后集中检查一次：

```bash
# 连续性检查（关系跳变、时间线冲突、设定矛盾）
/pipeline-continuity-gate ch001-ch010

# 合规检查（借鉴登记是否完整、风险级别）
/pipeline-compliance-gate ch001-ch010
```

**做了什么：** 跨章节扫描，输出按优先级排序的问题清单。
**改了什么文件：** 不改任何文件，只输出报告。
**状态变化：** 不变
**产出：** 修复清单。有问题回去改，没问题继续。

---

### 7. 归档发布：标记发布 + 导出

```bash
# 标记为已发布
/chapter-update ch001 --status published

# 导出为可投稿的纯文本
/chapter-export ch001-ch010 --format txt --clean
```

**做了什么：** 将章节合并导出为一个连续文件，去除所有内部标记（元数据、写作备忘、TODO、HTML 注释）。
**改了什么文件：** 导出到 `export/` 目录，不修改原始章节文件。
**状态变化：** `final → published`
**产出：** 一个干净的文本文件，可以直接投稿或发布。

---

### 全流程速查表

| 阶段 | 命令 | 状态变化 | 改什么文件 |
|------|------|---------|-----------|
| 开工 | `/pipeline-chapter-kickoff` | idea → outline | chapters/、plot/ |
| 找素材 | `/material-search` + `apply` | 不变 | chapters/（写作备忘） |
| 写草稿 | 手写 或 `/chapter-draft` | outline → draft | chapters/（正文草稿） |
| 打磨 | `/pipeline-draft-polish` | draft → revise | chapters/（修订建议） |
| 修订 | 手动改文 + `/chapter-update` | revise → final | chapters/（正文） |
| 质检 | `/pipeline-continuity-gate` | 不变 | 不改文件 |
| 归档 | `/chapter-update` + `/chapter-export` | final → published | export/ |

---

## 三、我在规划中（开新书 / 搭骨架）

### `draft-ingest` vs `note-triage`？先看你的文件像什么

| 你的文件 | 用什么 |
|---------|-------|
| 有叙事脉络——人物在做事、有事件推进 | `/draft-ingest` → 深度分析故事 DNA，再搭大纲 |
| 散装碎片——一条条的设定、角色、灵感 | `/pipeline-note-triage` → 分拣入库，直接落地 |
| 两种都有 | 先 `note-triage` 整理碎片，再把叙事段落单独给 `draft-ingest` |

### 有一篇草稿，想从头搭项目

```bash
/novel-init 《书名》 类型
/pipeline-outline-bootstrap drafts/my-draft.md
```

pipeline 会引导你走完：素材消化 → 设定落地 → 大纲构建。全程有确认，不会自动跑飞。

### 只有一句话想法

```bash
/novel-init 《书名》 类型
/pipeline-outline-bootstrap 主角因宗门灭门被迫踏上复仇与求真之路
```

会先问你 3-5 个问题展开想法，再构建大纲。

### 大纲有了，想整固设定

```bash
/pipeline-setting-consolidate
```

逐条审查 tentative 设定，确认/废弃/补缺。

### 想补强大纲节奏

```bash
/pipeline-outline-polish 中段节奏偏松
```

会做大纲审查 + 世界观审查，然后给出优化动作。

### 想改一个大纲节点

```bash
/plot-edit midpoint 事件改为：主角发现盟友是卧底
```

会自动检查这个节点关联了哪些已写章节，该确认就确认。

### 想加一条新设定（规划模式，仔细填）

```bash
/setting-add 现实抚平机制 --category world_rule
```

标准模式，会引导你填 description、rules、constraints、plot_links 等。

---

## 四、我想找参考（素材库检索）

素材库（`../novel-material`）是独立项目，收录了已拆解的小说场景、人物原型和技法案例。不切换 workspace 也能搜。

### 写某一类场景前，想看别人怎么写的

```bash
/material-search 恋人在雨中告别
/material-search 弱者反杀强者的对决
```

自动解析为标签组合，从素材库中检索匹配场景，返回摘要和原文定位。

### 想找特定技法的案例

```bash
/material-search 催泪但不煽情的技法
/material-search 用留白制造悬念
```

### 想看类似类型的小说怎么处理某种情节

```bash
/material-search 都市异能中的小团体内部分裂
```

会在素材库中按类型和场景标签检索，返回最相关的场景。

### 找到好的参考，想融合到自己的写作中

```bash
# 把参考场景的技法融入章节初稿
/material-search apply ch0042_s03 draft ch005

# 提取参考场景的冲突结构，对齐到大纲
/material-search apply ch0042_s03 plot 第一季

# 学参考场景的世界观呈现方式
/material-search apply ch0042_s03 setting 双宇宙融合

# 分析参考场景的节奏曲线
/material-search apply ch0042_s03 rhythm ch001-ch010

# 学参考人物的塑造技法
/material-search apply ch0042_s03 character 赵宋
```

五种融合模式，都是**借机制不借表达**——提取骨架和技法，适配到你的故事。融合后可选登记借鉴来源。

也可以用检索结果的序号代替场景 ID：`/material-search apply #1 draft ch005`

### 写初稿和想剧情时自动检索

`/chapter-draft` 和 `/plot-suggest` 已内置素材库检索步骤——如果素材库存在，会自动按当前章节的场景类型和情感基调检索参考场景，附在写作上下文中。不需要手动调用。

### 管理项目关联的素材

```bash
# 看素材库里有什么
/material-search available

# 把某本素材关联到当前项目
/material-search link nm_novel_20260405_zhbk

# 看当前项目关联了哪些素材
/material-search list

# 取消关联（不删借鉴记录）
/material-search unlink nm_novel_20260405_zhbk
```

### 借鉴了某个场景，想登记来源

```bash
/inspiration-log ch005 nm_novel_20260405_zhbk 借鉴了第三章的告别节奏
```

素材 ID 会自动在素材库中校验。登记后可用 `/inspiration-check` 检查风险。

> 没有素材库时，以上功能全部跳过或降级，不影响写作主流程。

---

## 五、我在写作中（心流状态，别打断我）

### 突然想到一个新设定

```bash
/setting-add 污染能量不能储存必须即时消耗 --quick
```

一句话搞定。自动标记为 tentative，自动记录你正在写的章节作为来源。写完这章再用 `/setting-edit` 补全，或者攒一批一起用 `/pipeline-setting-consolidate` 整固。

### 写着写着冒出好多设定点

选中你正在写的那段文字，然后说"把这些设定提取出来"——等效于：

```bash
/setting-add --from chapters/ch005.md --quick
```

自动扫描并快捕，回头再整固。

### 写到某个角色需要补设定

```bash
/character-edit 张三 致命缺陷：总以为自己能独自扛过去
```

直接补一个字段就行，不用把整个角色卡重新填一遍。

### 想让 AI 帮出个初稿

```bash
/chapter-draft ch005
```

基于大纲、角色设定和世界观生成初稿。生成的是可编辑起点，不是成品。可以加 `--style 冷叙述` 指定文风，加 `--focus 开场悬念` 聚焦重点。

### 卡文了，不知道下一场戏怎么写

```bash
/plot-suggest 第5章卡住了，主角进入敌营后没有冲突
```

会给你 2-3 个方案，带冲突点、代价和钩子。选一个继续写。

### 写完一章，想快速记录关系变化

```bash
/relationship-log 张三 李四 因误会关系降温 --chapter ch005
```

### 灵感爆发，随手写了一堆东西

先随便写到一个文件里（`drafts/ideas-0407.md`），不用管格式。写完后：

```bash
/pipeline-note-triage drafts/ideas-0407.md
```

自动分拣设定、角色、剧情、时间线，确认后一次性全部入库。

加 `--quick` 可以跳过逐条确认，全部快速落地（设定标 tentative，角色标基础档案）。

### 想查大纲里某章的计划或伏笔状态

```bash
/plot-query 第5章
/plot-query 未回收的伏笔
/plot-query 张三的剧情线
```

只读查询，不改任何文件。

### 想为一个重要场景建档

```bash
/scene-add 宗门大殿 --location 青云宗 --category interior
```

记录空间布局、感官细节、氛围基调，写章节时可以当环境锚点参考。

### 写着发现时间线可能有问题

```bash
/timeline-add 第3天清晨 主角抵达北城 --chapter ch005 --characters 张三
```

先记下来，之后用 `/timeline-check` 统一验证。

---

## 六、我在打磨中（章节写完，提质量）

### 草稿写完，做一轮打磨

```bash
/pipeline-draft-polish ch005
```

打包执行：结构审查 → 对白声音检查 → 设定依赖检查 → 去 AI 感处理。

### 只想检查 AI 痕迹

打开 `chapters/ch005.md` 后直接说"检查一下 AI 痕迹"，或：

```bash
/anti-ai-check ch005
```

给评分和具体高风险段落。想改就接着：

```bash
/anti-ai-rewrite ch005 --level 2
```

打开章节文件时，这两个命令都不需要手写章节 ID。

### 想检查角色对白是否同质化

```bash
/voice-check 张三 ch001-ch005
```

如果你正好打开了某个角色卡或章节文件，可以省略对应参数。

---

## 七、我在收束中（阶段检查 / 准备发布）

### 做一次全面体检

```bash
/pipeline-continuity-gate ch001-ch020
```

检查关系跳变、时间线冲突、设定依赖问题、跨模块矛盾，输出修复清单。

### 发布前做合规闸口

```bash
/pipeline-compliance-gate ch015-ch020
```

检查借鉴登记是否完整、风险级别、降风险建议。

### 怀疑设定有矛盾

```bash
/consistency-check
```

全项目扫描，分级输出问题和修复建议。

### 项目结构是不是哪里坏了

```bash
/novel-doctor
```

### 角色/设定的交叉索引好像过期了

```bash
/project-reindex
```

扫描全部角色和设定文件，重建交叉引用（角色→设定、设定→角色）、刷新 PROJECT_MAP.md 和 Cursor Rules。加 `--dry-run` 只看差异不改文件。建议在大批量添加角色或设定后运行一次。

### 想导出章节给人看或投稿

```bash
/chapter-export ch001-ch020 --format txt --clean
```

合并指定范围的章节为一个文件，`--clean` 会去掉所有内部标记和元数据。也可以只导出已发布的：

```bash
/chapter-export 已发布 --format md
```

---

## 八、我在管理中（多书切换 / 看进度）

### 切换到另一本书

```bash
/novel-switch 仙途
```

### 看当前项目状态

```bash
/novel-status
```

### 看所有书的概览

```bash
/novel-list
```

### 看章节进度看板

```bash
/chapter-board
```

### 生成周报

```bash
/project-weekly-report 最近7天 --view both
```

### 看 KPI

```bash
/novel-kpi 最近30天
```

### 改了一个 skill，想知道影响面

```bash
/skill-doctor consistency-check
```

列出所有依赖 consistency-check 的下游 skill、共享数据文件和需要同步的文档。

### skill 体系全面体检

```bash
/skill-doctor --full
```

检查断裂引用、循环依赖、枢纽风险、协议覆盖率，然后自动同步文档。

### 只想同步文档（SPEC.md、协议引用列表等）

```bash
/skill-doctor sync
```

扫描所有 skill，比对文档，展示 diff 预览后一键更新。

---

## 九、我想改已有内容

### 改项目信息（书名、类型、视角）

```bash
/novel-edit 书名 新书名
/novel-edit 视角 第三人称限制
```

改书名会自动列出所有受影响文件，确认后级联更新。

### 改一条设定

```bash
/setting-edit 污染体系 补充约束：触发后有冷却期
/setting-edit rule_001 --status confirmed
```

改 confirmed 设定的核心内容需要确认。

### 改大纲节点

```bash
/plot-edit 第5章 事件改为：主角发现旧友已投敌
```

关联已写章节时会做影响分析。

### 改角色信息

```bash
/character-edit 张三 年龄改为26岁
```

### 推进章节状态

```bash
/chapter-update ch005 --status revise
```

published 状态的章节回退需要确认。

---

## 十、Pipeline 快速参考

Pipeline 是"不想自己拼命令"时的打包预设。

| 我想做什么 | 用哪个 |
|-----------|-------|
| 找参考场景/技法 | `/material-search` |
| 从想法到可写大纲 | `/pipeline-outline-bootstrap` |
| 补强已有大纲 | `/pipeline-outline-polish` |
| 整固设定集 | `/pipeline-setting-consolidate` |
| 杂乱笔记一键入库 | `/pipeline-note-triage` |
| 开始写新章节 | `/pipeline-chapter-kickoff` |
| AI 辅助出初稿 | `/chapter-draft` |
| 打磨草稿 | `/pipeline-draft-polish` |
| 阶段性体检 | `/pipeline-continuity-gate` |
| 发布前合规 | `/pipeline-compliance-gate` |

**推荐顺序：**

```
bootstrap → setting-consolidate → outline-polish → chapter-kickoff → chapter-draft（可选）→ 写/改正文（note-triage 随时可用）→ draft-polish → continuity-gate → compliance-gate → chapter-export
```

---

## 十一、最小记忆集（只记这些就能用）

**核心原则：打开文件 = 传参数。** 大部分命令会从你当前打开的文件自动推断上下文。

**每天写作：**
- `/chapter-create` / `/chapter-update` — 管章节（打开章节文件可省略 ID）
- `/chapter-draft` — 让 AI 辅助出初稿
- `/setting-add --quick` — 快捕设定灵感
- `/plot-suggest` — 卡文时找思路
- `/plot-query` — 查大纲、伏笔、角色线
- `/material-search` — 找参考场景和技法案例
- `--from 文件路径` — 从文件提取角色/设定/情节

**每完成一章：**
- `/pipeline-draft-polish` — 一键打磨

**每周一次：**
- `/consistency-check` — 查矛盾
- `/project-weekly-report` — 看进度

**每个里程碑：**
- `/pipeline-continuity-gate` — 连续性闸口
- `/pipeline-setting-consolidate` — 设定整固
