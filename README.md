# AI 小说写作系统

面向长篇连载与多项目管理的写作工作台。  
你可以把它当成"小说生产系统"：既能写内容，也能管章节、关系、素材、风格与风险。

---

## 角色导航（先看这里）

| 你是谁 | 先看文档 | 先跑 3 个命令 |
|------|---------|---------------|
| 作者（专注写作） | `README-AUTHOR.md` | `/novel-switch` → `/chapter-create` → `/chapter-review` |
| 编辑/主编（控进度风险） | `README-EDITOR.md` | `/chapter-board` → `/project-weekly-report 最近7天 --view manager` → `/novel-kpi 最近30天` |
| 新人/搭建者（看全貌） | 本文件 + `docs/SPEC.md` | `/novel-init` → `/novel-status` → `/novel-doctor` |

---

## Harness 导航

- **想看写一章正文的完整节奏？** → `docs/USAGE-GUIDE.md` §二（从开工到归档的七步流程）
- **不知道用什么命令？** → `docs/USAGE-GUIDE.md`（场景使用指南）
- 场景使用指南：`docs/USAGE-GUIDE.md`
- Agent 地图：`AGENTS.md`
- 架构边界：`ARCHITECTURE.md`
- 完整命令参考：`docs/SPEC.md`（见"Skill清单"）

---

## 能力地图

> 一句话理解：从"写出来"到"写得稳、可复盘、可扩展"。

| 能力域 | 解决什么问题 | 代表命令 |
|------|--------------|---------|
| 项目与运营 | 多书管理、周报复盘、健康体检、Skill 变更管理 | `/novel-switch` `/novel-doctor` `/skill-doctor` `/project-weekly-report` `/novel-kpi` |
| 流程编排 | 把常用写作流程打包成场景预设，少记命令 | `/pipeline-outline-bootstrap` `/pipeline-note-triage` `/pipeline-draft-polish`（共 8 个） |
| 章节生产 | 新章创建、AI 辅助初稿、状态推进、结构打磨、导出发布 | `/chapter-create` `/chapter-draft` `/chapter-review` `/chapter-export` |
| 角色关系 | 角色设定、关系维护、关系演进与跳变检查 | `/character-add` `/relationship-log` `/relationship-evolution` `/relationship-check` |
| 素材消化与设定 | 草稿消化、世界观设定管理、场景档案 | `/draft-ingest` `/setting-add` `/scene-add` `/worldbuilding-review` |
| 素材库检索 | 从已拆解的小说中找参考场景、人物原型、技法案例 | `/material-search` `/material-apply` `/material-manage` |
| 文风质量 | 去 AI 感、人物对白区分、风格调优 | `/anti-ai-check` `/anti-ai-rewrite` `/voice-check` `/rewrite` |
| 合规风控 | 借鉴留痕、风险检查、阶段报告 | `/inspiration-log` `/inspiration-check` `/inspiration-report` |

如果你是新用户，建议先只用三个域：

1. 章节生产（先把内容写出来）
2. 素材消化与设定（把想法落地成可查的设定）
3. 文风质量（出稿前做最低限度质检）

---

## 这套系统适合谁

- 同时写多本书，需要频繁切换项目的人
- 连载作者，需要稳定推进章节与节奏的人
- 有素材积累习惯，希望做检索和复用的人
- 在意"去 AI 感"、借鉴风险、人物一致性的人

---

## 快速开始（5 分钟）

```bash
# 1) 创建项目
/novel-init 《书名》 类型

# 2) 初始化剧情结构（从素材推导，或手动指定）
/plot-init

# 3) 添加主角色
/character-add 张三 主角 25岁 剑客 隐忍坚毅

# 4) 创建第一章
/chapter-create ch001 主角在危机中被迫离开故土

# 5) 开始写作前检查
/novel-status
```

---

## 必用命令（10 个，日常优先）

1. `/novel-switch [项目名]`：切换当前写作项目
2. `/novel-status`：查看当前项目状态
3. `/chapter-create [章节ID] [目标]`：新建章节并初始化元数据
4. `/chapter-update [章节ID] --status [状态]`：推进章节状态
5. `/chapter-review [章节ID]`：审查章节并给修订建议
6. `/plot-suggest [描述]`：卡文时获取剧情建议
7. `/character-edit [角色名] [修改内容]`：修正角色设定
8. `/anti-ai-check [章节ID]`：检测 AI 痕迹
9. `/consistency-check`：全项目一致性检查
10. `/novel-doctor`：项目健康诊断

> 完整命令清单（含参数说明）见 `docs/SPEC.md` → Skill清单  
> 按场景查找命令见 `docs/USAGE-GUIDE.md`

---

## 进一步阅读

- 作者极简版：`README-AUTHOR.md`
- 编辑/主编版：`README-EDITOR.md`
- 场景使用指南：`docs/USAGE-GUIDE.md`
- 设计规范与命令参考：`docs/SPEC.md`
