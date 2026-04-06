# 作者极简手册（3分钟上手）

如果你只想专注写小说，不想记太多命令，先用这一版。

---

## 只记 6 个命令

```bash
/novel-switch 项目名
/chapter-create 章节ID 一句话目标
/material-search 关键词
/chapter-review 章节ID
/chapter-update 章节ID --status draft|revise|final
/consistency-check
```

---

## 三条核心流程

### 流程 A：今天开始写新章

```bash
/novel-switch 仙途
/chapter-create ch012 主角误入敌营并触发旧友冲突
```

然后直接写正文。

如果你不想自己拼命令，也可以直接用：

```bash
/pipeline-chapter-kickoff ch012 主角误入敌营并触发旧友冲突
```

---

### 流程 B：卡文时快速找灵感

```bash
/material-search 反转 背刺 误会
```

拿到片段后，只借结构和节奏，不要照搬表达。

---

### 流程 C：写完后快速打磨

```bash
/chapter-review ch012
/chapter-update ch012 --status revise
/consistency-check
```

你只要把高优先级问题先修完，就能进入可发状态。

如果你想把“审查 + 声音检查 + 去 AI 感”打包跑完，可以直接用：

```bash
/pipeline-draft-polish ch012
```

---

## 什么时候再用“进阶命令”

- 角色关系复杂了：`/relationship-check`
- 文风有 AI 感：`/anti-ai-check`
- 发文前怕借鉴风险：`/inspiration-check`
- 每周复盘：`/project-weekly-report` 或 `/novel-kpi`

如果你不想记太多组合，优先记这 4 个 pipeline：

| Pipeline | 什么时候用 |
|----------|-----------|
| `/pipeline-outline-bootstrap [premise]` | 从一句话想法启动大纲 |
| `/pipeline-chapter-kickoff [chapter_id] [goal]` | 开始写新章节 |
| `/pipeline-draft-polish [chapter_id]` | 草稿写完，打包打磨 |
| `/pipeline-compliance-gate [chapter_id|range]` | 发文前做借鉴留痕与风险闸口 |

---

## 最小工作节奏（建议）

- 每天：`create -> write -> review`
- 每周：做一次 `consistency-check`
- 每个里程碑：再补一次 `novel-doctor`

---

## 如果你是第一次用

还没项目就先执行：

```bash
/novel-init 《书名》 类型
```

然后回到上面的三条流程即可。
