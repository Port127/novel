# 使用指南：按场景找命令

> 不用记全部命令。找到你当前的场景，照着做。

---

## 目录

- [一、核心概念：文件就是输入](#一核心概念文件就是输入)
  - [打开文件自动识别](#1-打开章节文件就自动识别)
  - [用 --from 引用文件](#2-用---from-引用文件内容)
  - [混合笔记自动分拣](#3-写了一个杂乱的笔记文件什么都有)
- [二、一章正文的完整节奏（从开工到归档）](#二一章正文的完整节奏从开工到归档)
  - [开工 → 找素材 → 写草稿 → 打磨 → 修订 → 质检 → 归档](#1-开工创建章节填充骨架)
  - [全流程速查表](#8-全流程速查表)
- [三、规划阶段（开新书 / 搭骨架）](#三规划阶段开新书--搭骨架)
  - [draft-ingest vs note-triage / 从头搭项目 / 设定整固 / 大纲补强](#1-draft-ingest-vs-note-triage先看你的文件像什么)
- [四、写作阶段（心流状态，别打断我）](#四写作阶段心流状态别打断我)
  - [快捕设定 / 补角色 / AI 初稿 / 卡文求助 / 伏笔管理 / 灵感分拣 / 场景建档](#1-突然想到一个新设定)
- [五、素材检索（找参考场景与技法）](#五素材检索找参考场景与技法)
  - [场景检索 / 技法案例 / 融合到写作 / 管理关联素材](#1-写某一类场景前想看别人怎么写的)
- [六、打磨阶段（章节写完，提质量）](#六打磨阶段章节写完提质量)
  - [一键打磨 / AI 痕迹检查 / 对白声音检查](#1-草稿写完做一轮打磨)
- [七、修改已有内容](#七修改已有内容)
  - [改项目信息 / 改设定 / 设定演化 / 改大纲 / 改角色 / 推进状态](#1-改项目信息书名类型视角)
- [八、收束与发布（阶段检查 / 准备发布）](#八收束与发布阶段检查--准备发布)
  - [全面体检 / 合规闸口 / 索引维护 / 导出](#1-做一次全面体检)
- [九、项目管理（多书切换 / 看进度）](#九项目管理多书切换--看进度)
  - [切换项目 / 状态 / 看板 / 周报 / KPI / skill 体检](#1-切换到另一本书)
- [十、Rules 与记忆（AI 怎么"记住"你的书）](#十rules-与记忆ai-怎么记住你的书)
  - [三层 Rules / 同步时机 / 手动编辑](#三层-rules)
- [附录 A：关键产物与状态速查](#附录-a关键产物与状态速查)
  - [章节状态生命周期 / 关键产物文件 / open_questions](#章节状态生命周期)
- [附录 B：Pipeline 快速参考](#附录-bpipeline-快速参考)
- [附录 C：最小记忆集（只记这些就能用）](#附录-c最小记忆集只记这些就能用)

---

## 一、核心概念：文件就是输入

大多数命令支持直接引用文件或选中文本，不用手打参数。

### 1. 打开章节文件就自动识别

章节类命令（`chapter-review`、`anti-ai-check`、`anti-ai-rewrite`、`chapter-update`、`voice-check`）支持**自动推断**：

```
打开 chapters/ch005.md → 直接说"帮我审查这个章节"
```

不需要 `/chapter-review ch005`，AI 会从你当前打开的文件推断章节 ID。如果你同时开了多个文件，会优先用当前聚焦的那个。

### 2. 用 `--from` 引用文件内容

`setting-add`、`character-add`、`plot-add`、`relationship-add` 支持 `--from` 参数，直接从文件或选中内容提取信息：

**从章节中批量提取角色：**
```bash
/character-add --from chapters/ch003.md
```
自动扫描章节中出场的角色，提取姓名、身份、性格，逐个确认后创建（5 人以上先出汇总表）。

**用参考资料填充单个角色：**
```bash
/character-add 张三 --from drafts/张三参考.md
```
把文件当成张三的参考资料（人设笔记、灵感来源等），提炼后填充角色卡。

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

**从章节中提取角色关系：**
```bash
/relationship-add --from chapters/ch005.md
```
扫描角色间的互动和态度，推断关系类型和张力来源。

**选中文本直接用：**
选中编辑器里的一段文字，然后说"把选中的内容加到设定里"——等同于 `/setting-add --from "选中的文本"`。

**组合使用：**
```bash
/setting-add --from chapters/ch005.md --quick
```
从章节里提取设定，跳过确认，全部标记为 tentative 快速落地。

### 3. 写了一个杂乱的笔记文件，什么都有

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
/material-apply #1 draft ch001
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

生成前会自动构建**前情提要**——读取前面所有已写章节的摘要 + 出场角色的当前状态快照，确保不和前文矛盾。

**方式 C：写多个备选版本对比**

```bash
/chapter-draft ch001 --alt 强调悬疑氛围
/chapter-draft ch001 --alt 偏动作场面
```

每个 `--alt` 会生成一个独立版本文件（`ch001_v2.md`、`ch001_v3.md`），不影响主版本。对比和提升：

```bash
/chapter-compare ch001                 # 对比主版本和最新备选
/chapter-compare ch001 main v2         # 指定两个版本对比
/chapter-update ch001 --promote v2     # 把 v2 提升为主版本
```

`/chapter-compare` 会从字数、场景结构、开头/结尾钩子、情感曲线、文风五个维度给出对比报告和合并建议。

**改了什么文件：** `chapters/ch001.md`（正文草稿区域）
**状态变化：** `outline → draft`
**产出：** 一份有完整正文的章节草稿。

---

### 3.5. 状态推进时自动生成前情摘要

当你把章节推进到 `draft` 或 `final`（手动 `/chapter-update` 或 AI 自动推进），系统会：
- 自动生成 2-3 句**章节摘要**（写入 `index.yaml`）
- 自动更新出场角色的**当前状态快照**（位置/情绪/已知信息/行动目标）

这些数据是后续章节的"前情记忆"——写第 20 章时，AI 会读取前 19 章的摘要链，而不是去翻 19 章正文。

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

### 8. 全流程速查表

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

## 三、规划阶段（开新书 / 搭骨架）

### 1. `draft-ingest` vs `note-triage`？先看你的文件像什么

| 你的文件 | 用什么 |
|---------|-------|
| 有叙事脉络——人物在做事、有事件推进 | `/draft-ingest` → 深度分析故事 DNA，再搭大纲 |
| 散装碎片——一条条的设定、角色、灵感 | `/pipeline-note-triage` → 分拣入库，直接落地 |
| 两种都有 | 先 `note-triage` 整理碎片，再把叙事段落单独给 `draft-ingest` |

### 2. 有一篇草稿，想从头搭项目

```bash
/novel-init 《书名》 类型
/pipeline-outline-bootstrap drafts/my-draft.md
```

pipeline 会引导你走完：素材消化 → 设定落地 → 大纲构建。全程有确认，不会自动跑飞。

### 3. 只有一句话想法

```bash
/novel-init 《书名》 类型
/pipeline-outline-bootstrap 主角因宗门灭门被迫踏上复仇与求真之路
```

会先问你 3-5 个问题展开想法，再构建大纲。

### 4. 大纲有了，想整固设定

```bash
/pipeline-setting-consolidate
```

逐条审查 tentative 设定，确认/废弃/补缺。

### 5. 想补强大纲节奏

```bash
/pipeline-outline-polish 中段节奏偏松
```

会做大纲审查 + 世界观审查，然后给出优化动作。

### 6. 想改一个大纲节点

```bash
/plot-edit midpoint 事件改为：主角发现盟友是卧底
```

会自动检查这个节点关联了哪些已写章节，该确认就确认。

### 7. 想加一条新设定（规划模式，仔细填）

```bash
/setting-add 现实抚平机制 --category world_rule
```

标准模式，会引导你填 description、rules、constraints、plot_links 等。

---

## 四、写作阶段（心流状态，别打断我）

### 1. 突然想到一个新设定

```bash
/setting-add 污染能量不能储存必须即时消耗 --quick
```

一句话搞定。自动标记为 tentative，自动记录你正在写的章节作为来源。写完这章再用 `/setting-edit` 补全，或者攒一批一起用 `/pipeline-setting-consolidate` 整固。

### 2. 写着写着冒出好多设定点

选中你正在写的那段文字，然后说"把这些设定提取出来"——等效于：

```bash
/setting-add --from chapters/ch005.md --quick
```

自动扫描并快捕，回头再整固。

### 3. 写到某个角色需要补设定

```bash
/character-edit 张三 致命缺陷：总以为自己能独自扛过去
```

直接补一个字段就行，不用把整个角色卡重新填一遍。

想让角色说话更有个性？补充语言画像：

```bash
/character-edit 张三 说话粗犷直接，满嘴脏话，口头禅是"老子"，绝对不会说"请"和"谢谢"
```

这会写入角色卡的 `speech_pattern` 字段，后续 `/chapter-draft` 生成初稿和 `/anti-ai-rewrite` 改写对白时都会参照。

想让 AI 从已写章节中自动补充？

```bash
/character-edit 张三 --auto-fill
```

扫描张三出场的所有章节，从正文中反推可补充的字段，列出 diff 表确认后写入。只补空字段，不覆盖你手写的内容。也可以指定范围：`/character-edit 张三 --from-chapters ch001-ch010`。

### 4. 想让 AI 帮出个初稿

```bash
/chapter-draft ch005
```

基于大纲、角色设定和世界观生成初稿。生成的是可编辑起点，不是成品。可以加 `--style 冷叙述` 指定文风，加 `--focus 开场悬念` 聚焦重点。

### 5. 卡文了，不知道下一场戏怎么写

```bash
/plot-suggest 第5章卡住了，主角进入敌营后没有冲突
```

会给你 2-3 个方案，带冲突点、代价和钩子。选一个继续写。

### 6. 写完一章，想快速记录关系变化

```bash
/relationship-log 张三 李四 因误会关系降温 --chapter ch005
```

### 6.5. 想批量建立某个角色的关系网络

```bash
/relationship-add --auto 张三
```

扫描全项目（角色卡 + 章节 + 大纲），自动推断张三和所有已建档角色的关系，跳过已存在的。也可以从单个章节提取：`/relationship-add --from chapters/ch005.md`。

### 7. 灵感爆发，随手写了一堆东西

先随便写到一个文件里（`drafts/ideas-0407.md`），不用管格式。写完后：

```bash
/pipeline-note-triage drafts/ideas-0407.md
```

自动分拣设定、角色、剧情、时间线，确认后一次性全部入库。

加 `--quick` 可以跳过逐条确认，全部快速落地（设定标 tentative，角色标基础档案）。

### 8. 想查大纲里某章的计划或伏笔状态

```bash
/plot-query 第5章
/plot-query 未回收的伏笔
/plot-query 张三的剧情线
```

只读查询，不改任何文件。

### 8.1. 伏笔/钩子管理

系统提供分级伏笔管理——major（跨季主线）、minor（3-10 章内回收）、micro（1-2 章内回收）。

**埋伏笔：**

```bash
/hook-add 阮声的真实身份 --chapter ch003 --level major --deadline 第一季结束 --condition 赵宋触发概念共鸣时揭示
```

**查看伏笔状态：**

```bash
/hook-query --overdue               # 看逾期未回收的钩子
/hook-query --near ch010            # 看 ch010 附近该回收的
/hook-query --level major --timeline # major 钩子时间轴视图
```

**回收/放弃/延期：**

```bash
/hook-resolve hook_001 --recover ch015        # 在 ch015 回收
/hook-resolve hook_003 --abandon 剧情调整不再需要  # 放弃（major 需确认）
/hook-resolve hook_002 --extend 第二季前半段   # 延期截止
```

`/pipeline-chapter-kickoff` 开写新章时会自动提醒即将到期的钩子。`/chapter-review` 审查时会按级别检查伏笔密度。

### 8.5. 想看某个角色的完整故事线

```bash
/character-query 张三 --storyline
```

一次性输出五个层面：已写章节中的实际剧情 → 大纲中的未来计划 → 关系演进 → 人物弧光 → 当前状态快照。写新章节前回顾角色脉络特别有用。

只想快速看角色此刻状态：

```bash
/character-query 张三 --status
```

### 9. 想为一个重要场景建档

```bash
/scene-add 宗门大殿 --location 青云宗 --category interior
```

记录空间布局、感官细节、氛围基调，写章节时可以当环境锚点参考。

### 10. 写着发现时间线可能有问题

```bash
/timeline-add 第3天清晨 主角抵达北城 --chapter ch005 --characters 张三
```

先记下来，之后用 `/timeline-check` 统一验证。

### 11. 想看两个角色的关系怎么演变的

```bash
/relationship-evolution 张三 --with 李四
```

按时间线展示两人关系的全部变化事件（每个事件由 `/relationship-log` 记录）。适合写新章节前回顾已有关系脉络。

### 12. 想用特定文风写/改一段

```bash
# 看有哪些风格模板
/style-list

# 创建自己的风格模板
/style-create 冷叙述 克制、短句、不抒情、动作优先

# 按指定风格改写一段文字
/rewrite --style 冷叙述
```

### 13. 想初始化大纲结构（还没有 outline）

```bash
/plot-init
```

从 `ingestion_brief.md` 自动推导大纲结构（三幕式/英雄旅程等）。也可以手动指定：`/plot-init 三幕式`。

---

## 五、素材检索（找参考场景与技法）

素材库（`../novel-material`）是独立项目，收录了已拆解的小说场景、人物原型和技法案例。不切换 workspace 也能搜。

### 1. 写某一类场景前，想看别人怎么写的

```bash
/material-search 恋人在雨中告别
/material-search 弱者反杀强者的对决
```

自动解析为标签组合，从素材库中检索匹配场景，返回摘要和原文定位。

### 2. 想借鉴别的小说的大纲结构

```bash
/material-search outline 从废物到强者的逆袭结构
/material-search outline 中点反转 导师死亡
```

搜索素材库中各小说的大纲，返回全书结构骨架、关键转折和节奏标注，并与你的项目大纲做结构对比。

### 3. 想借鉴某个角色的故事线

```bash
/material-search character-arc 导师牺牲线
/material-search character-arc 许七安
```

搜索素材库中角色的完整弧光——从起点到终点的每个阶段、心理画像、关键转折。可以直接搜角色名看其全线发展。

### 4. 想参考叙事节奏

```bash
/material-search rhythm 开篇快节奏案件推进
/material-search rhythm 高潮前的蓄力段
/material-search rhythm --material nm_novel_xxx 第二卷
```

分析参考小说的张力曲线和场景编排模式，输出节奏对比和调整建议。

### 5. 找到好的参考，想融合到自己的写作中

```bash
# 场景级融合
/material-apply ch0042_s03 draft ch005        # 技法融入初稿
/material-apply ch0042_s03 plot 第一季         # 冲突结构对齐大纲
/material-apply ch0042_s03 setting 双宇宙融合  # 世界观呈现技法
/material-apply ch0042_s03 character 赵宋      # 人物塑造技法

# 大纲级融合——借鉴整部小说的结构设计
/material-apply nm_novel_xxx outline

# 角色弧光融合——借鉴参考角色的弧光给你的角色
/material-apply 许七安 arc 张三

# 节奏融合——分析参考小说的节奏曲线，对比你的项目
/material-apply nm_novel_xxx rhythm-pattern ch001-ch020
```

所有融合都是**借机制不借表达**——提取骨架和技法，适配到你的故事。融合后可选登记借鉴来源。

也可以用检索结果的序号代替 ID：`/material-apply #1 draft ch005`

### 5. 写初稿和想剧情时自动检索

`/chapter-draft` 和 `/plot-suggest` 已内置素材库检索步骤——如果素材库存在，会自动按当前章节的场景类型和情感基调检索参考场景，附在写作上下文中。不需要手动调用。

### 6. 管理项目关联的素材

```bash
# 看素材库里有什么
/material-manage available

# 把某本素材关联到当前项目
/material-manage link nm_novel_20260405_zhbk

# 看当前项目关联了哪些素材
/material-manage list

# 取消关联（不删借鉴记录）
/material-manage unlink nm_novel_20260405_zhbk
```

### 7. 借鉴了某个场景，想登记来源

```bash
/inspiration-log ch005 nm_novel_20260405_zhbk 借鉴了第三章的告别节奏
```

素材 ID 会自动在素材库中校验。登记后可用 `/inspiration-check` 检查风险。

> 没有素材库时，以上功能全部跳过或降级，不影响写作主流程。

---

## 六、打磨阶段（章节写完，提质量）

### 1. 草稿写完，做一轮打磨

```bash
/pipeline-draft-polish ch005
```

打包执行：结构审查 → 对白声音检查 → 设定依赖检查 → 去 AI 感处理。

### 2. 只想检查 AI 痕迹

打开 `chapters/ch005.md` 后直接说"检查一下 AI 痕迹"，或：

```bash
/anti-ai-check ch005
```

会从七个维度给出评分：**套话密度、句式重复、比喻过载、描写堆砌、对白同质化、机械转折、心理描写质量**。每个维度独立打分，定位到具体段落。心理描写维度检测 show vs tell 比例、内心独白套路化、情绪层次数和身体感受密度。

想改就接着：

```bash
/anti-ai-rewrite ch005 --level 2
```

L1 只动词汇句式，L2 加上比喻瘦身、描写压缩和对白口语化，L3 可微调叙事视角。改写会参照角色的 `speech_pattern` 让对白符合人物性格。

打开章节文件时，这两个命令都不需要手写章节 ID。

### 3. 想检查角色对白是否同质化

```bash
/voice-check 张三 ch001-ch005
```

会对比角色卡中的语言画像（`speech_pattern`）和实际对白，检查语气、粗话频率、口头禅、用词层次是否匹配，并给出带原句和改后句的具体修复建议。还会横向对比同场景其他角色，检测区分度。

如果角色还没设置 `speech_pattern`，会提示你补充。补充方式：

```bash
/character-edit 张三 说话粗鲁直接，爱用反问，口头禅是"操"
```

如果你正好打开了某个角色卡或章节文件，可以省略对应参数。

---

## 七、修改已有内容

### 1. 改项目信息（书名、类型、视角）

```bash
/novel-edit 书名 新书名
/novel-edit 视角 第三人称限制
```

改书名会自动列出所有受影响文件，确认后级联更新。

### 2. 改一条设定

```bash
/setting-edit 污染体系 补充约束：触发后有冷却期
/setting-edit rule_001 --status confirmed
```

改 confirmed 设定的核心内容需要确认。修改设定或角色后，系统会自动扫描已写章节中的潜在冲突并给出提示。

### 2.5. 设定演化（规则随剧情更新）

设定不是一成不变的——故事发展到某个阶段后，旧规则会被新规则替代。

**创建接替设定：**

```bash
/setting-add 污染体系v2 --supersedes rule_001 --valid-from ch020
```

旧设定自动标记为 deprecated，新旧设定双向关联。

**在已有设定上演化：**

```bash
/setting-edit rule_001 --evolve
```

以旧设定为基础创建新版本，保留继承关系。

**设置有效期：**

```bash
/setting-edit rule_001 --valid-until ch019
/setting-add 灵气潮汐规则 --valid-from ch020 --valid-until ch050
```

有效期可以是章节号、事件名或其他标记。`/chapter-draft` 生成初稿时会自动过滤过期设定，`/pipeline-chapter-kickoff` 开写时会提醒即将过期的设定。

### 3. 改大纲节点

```bash
/plot-edit 第5章 事件改为：主角发现旧友已投敌
```

关联已写章节时会做影响分析。

### 4. 改角色信息

```bash
# 手动改一个字段
/character-edit 张三 年龄改为26岁

# 让 AI 从剧情中自动补充空字段
/character-edit 张三 --auto-fill

# 指定章节范围
/character-edit 张三 --from-chapters ch001-ch010
```

### 5. 推进章节状态

```bash
/chapter-update ch005 --status revise
```

published 状态的章节回退需要确认。

---

## 八、收束与发布（阶段检查 / 准备发布）

### 1. 做一次全面体检

```bash
/pipeline-continuity-gate ch001-ch020
```

检查关系跳变、时间线冲突、设定依赖问题、跨模块矛盾，输出修复清单。

### 2. 发布前做合规闸口

```bash
/pipeline-compliance-gate ch015-ch020
```

检查借鉴登记是否完整、风险级别、降风险建议。

### 3. 怀疑设定有矛盾

```bash
/consistency-check
```

全项目扫描，分级输出问题和修复建议。

### 4. 项目结构是不是哪里坏了

```bash
/novel-doctor
```

### 5. 项目索引维护（`/project-reindex`）

```bash
/project-reindex
```

不只是"刷交叉索引"——它是项目级的全量对齐工具，一次做六件事：

| 步骤 | 做什么 | 影响范围 |
|------|--------|---------|
| 1 | 收集全量数据（角色、设定、关系、章节、情节、时间线） | 只读扫描 |
| 2 | 推导交叉引用（角色 ↔ 设定双向同步、势力关联） | 自动补全遗漏 |
| 3 | 对比差异，生成报告 | 只读 |
| 4 | 写入更新（角色文件、设定文件、索引文件） | 批量修复 |
| 5 | 刷新 `PROJECT_MAP.md`（项目全景地图） | 进度/角色/设定一览 |
| 6 | 同步 Cursor Rules（`.novel/rules/` → `.cursor/rules/`） | AI 上下文自动更新 |

加 `--dry-run` 只看差异不改文件。

**什么时候该跑一次？**

- 大批量添加角色或设定后（bootstrap / note-triage 之后）
- 新项目完成第一轮 outline-bootstrap + setting-consolidate 后
- 切换项目发现 AI "不认识"当前书的设定
- 阶段性收束前，和 `continuity-gate` 搭配
- 觉得 `PROJECT_MAP.md` 过时了

### 6. 想导出章节给人看或投稿

```bash
/chapter-export ch001-ch020 --format txt --clean
```

合并指定范围的章节为一个文件，`--clean` 会去掉所有内部标记和元数据。也可以只导出已发布的：

```bash
/chapter-export 已发布 --format md
```

---

## 九、项目管理（多书切换 / 看进度）

### 1. 切换到另一本书

```bash
/novel-switch 仙途
```

切换时会自动把该项目的 Rules（上下文 + 世界观护栏）同步到 `.cursor/rules/`，让 AI 立刻进入这本书的状态。如果提示"尚未配置专属规则"，运行 `/project-reindex` 生成。

### 2. 看当前项目状态

```bash
/novel-status
```

### 3. 看所有书的概览

```bash
/novel-list
```

### 4. 看章节进度看板

```bash
/chapter-board
```

### 5. 生成周报

```bash
/project-weekly-report 最近7天 --view both
```

### 6. 看 KPI

```bash
/novel-kpi 最近30天
```

### 7. 改了一个 skill，想知道影响面

```bash
/skill-doctor consistency-check
```

列出所有依赖 consistency-check 的下游 skill、共享数据文件和需要同步的文档。

### 8. skill 体系全面体检

```bash
/skill-doctor --full
```

检查断裂引用、循环依赖、枢纽风险、协议覆盖率，然后自动同步文档。

### 9. 只想同步文档（SPEC.md、协议引用列表等）

```bash
/skill-doctor sync
```

扫描所有 skill，比对文档，展示 diff 预览后一键更新。

---

## 十、Rules 与记忆（AI 怎么"记住"你的书）

系统通过三层 Cursor Rules 让 AI 在每次对话开始时自动加载项目上下文，不用你每次重复介绍设定。

### 三层 Rules

| 层级 | 文件 | 作用 | 谁维护 |
|------|------|------|--------|
| 通用规则 | `.cursor/rules/novel-workflow.mdc` | 所有项目共享的工作流经验、文件约定、创作护栏 | 手动编辑 |
| 项目上下文 | `.novel/rules/context.md` → `.cursor/rules/novel-project-context.mdc` | 当前书的世界观概要、角色地图、文件导航 | `/project-reindex` 自动刷新 |
| 世界观护栏 | `.novel/rules/constraints.md` → `.cursor/rules/novel-core-constraints.mdc` | 硬约束速查，写作和大纲修改不得违反 | `/project-reindex` 自动刷新，手动可编辑 |

### 什么时候会同步？

- **`/novel-switch`**：切换项目时，自动把目标项目的 rules 同步到 `.cursor/rules/`
- **`/project-reindex`**：重建索引时，用最新数据刷新 `context.md` 并同步
- **`/novel-init`**：创建新项目时，初始化空模板

### 新项目没有 Rules 怎么办？

如果你的项目是在 Rules 功能上线前创建的（没有 `.novel/rules/` 目录），运行一次：

```bash
/project-reindex
```

会自动创建 `context.md` 和 `constraints.md` 并同步。

### 想手动编辑约束？

直接编辑 `projects/你的书/.novel/rules/constraints.md`，然后运行 `/novel-switch` 或 `/project-reindex` 同步到 `.cursor/rules/`。

---

## 附录 A：关键产物与状态速查

### 章节状态生命周期

每个章节有一个状态字段，沿着以下路径推进：

| 状态 | 含义 | 怎么进入 | 下一步 |
|------|------|---------|--------|
| `idea` | 有想法，还没展开 | `/chapter-create` 默认 | 写场景大纲 |
| `outline` | 场景骨架已填充 | `/pipeline-chapter-kickoff` | 写正文 |
| `draft` | 正文草稿完成 | 手写后 `/chapter-update --status draft`，或 `/chapter-draft` | 打磨 |
| `revise` | 打磨完，待修订 | `/pipeline-draft-polish` | 手动改文 |
| `final` | 终稿 | `/chapter-update --status final` | 导出发布 |
| `published` | 已发布 | `/chapter-update --status published` | 归档 |

published 状态的章节回退需要确认。任何时候都可以用 `/chapter-update` 手动推进或回退。

### 关键产物文件

这些文件在写作过程中自动产生，了解它们的作用有助于理解系统行为：

| 文件 | 什么时候产生 | 作用 |
|------|-------------|------|
| `ingestion_brief.md` | `/draft-ingest` 或 `/pipeline-outline-bootstrap` | 草稿的深度消化摘要：故事 DNA、角色动机、规则缺口。后续 skill 以此为基础避免误读 |
| `PROJECT_MAP.md` | `/project-reindex` | 项目全景地图：进度总览、角色地图、设定地图、关系网络。一页看全貌 |
| `.novel/rules/context.md` | `/novel-init`、`/project-reindex` | AI 的"开工记忆"：书名、类型、文件导航，让 AI 秒进状态 |
| `.novel/rules/constraints.md` | `/project-reindex`、手动编辑 | 世界观硬约束，AI 写作和改大纲时自动遵守 |

### 设定条目的 `open_questions`

用 `/setting-add --quick` 快捕设定时，系统会自动在条目中填入 `open_questions: ["待补充完整描述和规则"]`。这是正常的——快捕就是先记下来，不打断心流。

这些未解决问题的处理路径：

```
/setting-add --quick → 自动留下 open_questions
      ↓
/pipeline-setting-consolidate → 逐条审查时展示 open_questions，引导你补全或跳过
      ↓
/setting-edit → 手动补全内容，清空 open_questions
```

`/worldbuilding-review` 也会在设定集健康度中统计 open_questions 总数。不用急着清零——保留 tentative 设定的模糊点是正确的，等写到相关章节再明确。

---

## 附录 B：Pipeline 快速参考

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
| 检查与前后章衔接 | `/chapter-review --context` |
| 跨章文风一致性 | `/style-audit` |
| 多线叙事检查 | `/timeline-view --multi-thread` |
| 力量体系专审 | `/worldbuilding-review --focus power_system` |
| 人设矛盾修复 | `/character-edit 角色名 --fix` |
| 阶段性体检 | `/pipeline-continuity-gate` |
| 发布前合规 | `/pipeline-compliance-gate` |
| 管理伏笔/钩子 | `/hook-add` `/hook-query` `/hook-resolve` |
| 对比章节备选版本 | `/chapter-compare` → `/chapter-update --promote` |
| 设定演化接替 | `/setting-edit --evolve` 或 `/setting-add --supersedes` |
| 重命名角色（安全） | `/character-edit 角色名 改名为新名`（自动预览影响面） |
| 配置命名风格 | `/novel-edit naming.era modern`（或 ancient/fantasy） |

**推荐顺序：**

```
bootstrap → setting-consolidate → outline-polish
  → chapter-kickoff → chapter-draft（可选）→ 写/改正文
  → note-triage（随时可用）
  → draft-polish → continuity-gate → compliance-gate → chapter-export
```

---

## 附录 C：最小记忆集（只记这些就能用）

**核心原则：打开文件 = 传参数。** 大部分命令会从你当前打开的文件自动推断上下文。

**每天写作：**
- `/chapter-create` / `/chapter-update` — 管章节（打开章节文件可省略 ID）
- `/chapter-draft` — 让 AI 辅助出初稿（`--alt` 生成备选版本）
- `/setting-add --quick` — 快捕设定灵感
- `/plot-suggest` — 卡文时找思路
- `/plot-query` — 查大纲、伏笔、角色线
- `/hook-add` — 埋伏笔时登记（别忘分级）
- `/material-search` — 找参考场景和技法案例
- `--from 文件路径` — 从文件提取角色/设定/情节

**每完成一章：**
- `/pipeline-draft-polish` — 一键打磨
- `/hook-query --near ch_id` — 看附近该回收的钩子

**每周一次：**
- `/consistency-check` — 查矛盾（含钩子健康度和设定有效期）
- `/project-weekly-report` — 看进度
- `/hook-query --overdue` — 清理逾期钩子

**每个里程碑：**
- `/pipeline-continuity-gate` — 连续性闸口
- `/pipeline-setting-consolidate` — 设定整固
