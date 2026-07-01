# bug

# 阶段行优化
- 审查.agents/skills所有定义schema：
第一层：是否都已经跟项目对齐。
第二层：不同的skills，使用同一份schema的时候是否存在冲突。
第三层：判断这些schema是否够用，是否需要补充？参考本项目同级项目other/oh-story-claudecode。

# 长期优化（暂时不管）

## 对于项目的疑问（学习提升）

# 常用话术


# 小说skill
你先阅读.agents/skills/review（skill、references、scripts），注意：每个字符都要看！
（参考内容，本项目同级项目other/oh-story-claudecode，是否使用它的提示词，照抄了还是进行针对本项目的改造？有没有缺漏关键能力）
帮我看看有哪些欠缺，包括但不限于描述、提示词、上下文、引用文件
你要整体的审查这个skill，放在我们整个系统、agent中所起到的作用，整体审查

现在参考 .agents/skills/SKILL_TEMPLATE.md，对当前 Skill 进行非破坏性合并。请你只把模板里的架构要求（UX、进度保存、门禁等）穿插进去，绝对不要删减、概括或修改任何原有的业务逻辑、细化标准和模板格式！

再审查一次.agents/skills/review（skill、references、scripts），从多角度、全局考虑，有任何问题都可以提出来

反思、提炼的改动，然后分析是否有可以落实到.agents/skills/SKILL_TEMPLATE.md的内容

好，帮我使用commit-msg进行commit，然后push

这三个还没做，先不管
| `data-diagnosis` | 数据诊断（导入平台数据，分析追读/互动，定位问题章节） |
| `stock-check` | 存稿看板（查看存稿水位、成本报告、应急建议） |
| `export-novel` | 导出作品（将正文编译为 txt/md/epub） |



之前我让你分析过本项目，然后你的分析是：
问题：
···
Skill 内部还没完全对齐新文档
文档现在主推 settings/chapters_index.yaml，但 design-chapters 和 daily-write 仍大量依赖 settings/chapter_outlines/chapter_{N}.md。这未必是错，但需要明确：章节索引是总表，chapter_outlines/ 是详细细纲。否则执行时会混乱。

正文路径存在轻微漂移
文档多处写 content/chapter_*.md，.agents/AGENTS.md 里还有 content/chapters/。这类路径差异会影响导出、审查和日更恢复。

执行仍依赖人类/Agent 纪律，没有统一 runtime
现在 Skill 很完整，但本质还是“Agent 读 SKILL.md 后按规程执行”。没有一个统一的 Skill Runner 来强制读取 schema、记录 _progress.md、调用脚本、收集门禁结果。这意味着质量很依赖执行者是否守规矩。

历史文档很多，容易误导未来维护者
docs/superpowers/plans 和 archive 中仍保留大量旧自动化/模块化结构内容。你现在的 docs 已经声明“历史仅供参考”，但后续维护时仍可能被旧计划带偏。
···
需要做的事
···
统一正文路径：content/ 还是 content/chapters/。
明确 chapters_index.yaml 与 settings/chapter_outlines/ 的关系。
统一 paywall_report.yaml 放根目录还是 settings/。
给每个 Skill 做一次“路径、输入、输出、脚本调用”审计。
暂时接受 Python 测试红，但在 README 或开发说明里标注 Python 已冻结，避免误判。
···