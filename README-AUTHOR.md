# 作者极简手册（3 分钟上手）

如果你只想专注写小说，不想记太多命令，先用这一版。

> 完整场景指南见 `docs/USAGE-GUIDE.md`  
> 一章正文从开工到归档的七步节奏见 `docs/USAGE-GUIDE.md` → §二

---

## 只记 6 个命令

| 命令 | 干什么 | 什么时候用 |
|------|-------|-----------|
| `/novel-switch 项目名` | 切换书 | 每天开工第一件事 |
| `/chapter-create ch012 目标` | 建新章 | 每次开新章 |
| `/chapter-update ch012 --status draft` | 推进状态 | 写完草稿、修订完、定稿后 |
| `/setting-add 一句话描述 --quick` | 快捕设定灵感 | 写着写着冒出新想法 |
| `/plot-suggest 卡点描述` | 找灵感 | 卡文时 |
| `/pipeline-draft-polish ch012` | 一键打磨 | 写完草稿想打磨 |

---

## 三条核心流程

### 流程 A：今天开始写新章

```bash
/novel-switch 仙途
/chapter-create ch012 主角误入敌营并触发旧友冲突
```

然后直接写正文。或者用 pipeline 一步到位：

```bash
/pipeline-chapter-kickoff ch012 主角误入敌营并触发旧友冲突
```

### 流程 B：写到一半有新想法

**灵感很杂（设定+角色+剧情混在一起）**——写到一个文件里，然后：

```bash
/pipeline-note-triage drafts/ideas-0407.md
```

自动分拣所有内容类型，确认后一次性入库。加 `--quick` 跳过逐条确认。

**灵感是设定**（规则、势力、道具等）：

```bash
/setting-add 污染能量不能储存必须即时消耗 --quick
```

一句话记下来，继续写。等之后用 `/pipeline-setting-consolidate` 统一整理。

**灵感是剧情**：

```bash
/plot-suggest 中段需要一次反转，且不破坏主线动机
```

**角色需要补信息**：

```bash
/character-edit 张三 致命缺陷：总以为自己能独自扛过去
```

### 流程 C：写完后快速打磨

```bash
/pipeline-draft-polish ch012
```

打包完成：结构审查 + 对白检查 + 设定依赖检查 + 去 AI 感。

---

## 什么时候用进阶命令

| 场景 | 命令 |
|------|-----|
| 埋了伏笔想登记 | `/hook-add 名称 --chapter ch012 --level minor` |
| 查哪些伏笔该回收了 | `/hook-query --overdue` 或 `--near ch012` |
| 写了两版想对比 | `/chapter-draft ch012 --alt 方案B` → `/chapter-compare ch012` |
| 设定随剧情过期了 | `/setting-edit rule_001 --evolve` |
| 角色关系复杂了 | `/relationship-check` |
| 文风有 AI 感 | `/anti-ai-check ch012` |
| 发文前怕借鉴风险 | `/pipeline-compliance-gate ch012` |
| 阶段性体检 | `/pipeline-continuity-gate ch001-ch020` |
| 设定太多太乱 | `/pipeline-setting-consolidate` |
| 每周复盘 | `/project-weekly-report` |

---

## 5 个常用 Pipeline（不想记组合就记这些）

| Pipeline | 什么时候用 |
|----------|-----------|
| `/pipeline-outline-bootstrap [想法]` | 从零搭大纲 |
| `/pipeline-note-triage [文件]` | 杂乱笔记一键分拣入库 |
| `/pipeline-chapter-kickoff [ch_id] [目标]` | 开始写新章节 |
| `/pipeline-draft-polish [ch_id]` | 草稿写完，打磨 |
| `/pipeline-setting-consolidate` | 设定太散，整固一次 |

> 完整 8 个 Pipeline 及推荐顺序见 `docs/USAGE-GUIDE.md` → 附录 B：Pipeline 快速参考

---

## 最小工作节奏

- **每天**：`create → 写正文 → draft-polish`
- **每周**：做一次 `consistency-check`
- **每个里程碑**：`continuity-gate` + `setting-consolidate`

---

## 第一次用？

```bash
/novel-init 《书名》 类型
/pipeline-outline-bootstrap drafts/我的草稿.md
```

然后回到上面的三条流程。
