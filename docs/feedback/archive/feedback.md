# bug

# 阶段行优化
- 审查.agents/skills所有定义schema：
第一层：是否都已经跟项目对齐。
第二层：不同的skills，使用同一份schema的时候是否存在冲突。
第三层：判断这些schema是否够用，是否需要补充？参考本项目同级项目other/oh-story-claudecode。

# 长期优化（暂时不管）

## 对于项目的疑问（学习提升）

# 常用话术
- 好，使用commit-msg，帮我commit，然后push


# 小说skill
你先阅读.agents/skills/design-chapters（skill、references、scripts），注意：每个字符都要看！
（参考内容，本项目同级项目other/oh-story-claudecode，是否使用它的提示词，照抄了还是进行针对本项目的改造？有没有缺漏关键能力）
帮我看看有哪些欠缺，包括但不限于描述、提示词、上下文、引用文件
你要整体的审查这个skill，放在我们整个系统、agent中所起到的作用，整体审查

现在参考 .agents/skills/SKILL_TEMPLATE.md，对当前 Skill 进行非破坏性合并。请你只把模板里的架构要求（UX、进度保存、门禁等）穿插进去，绝对不要删减、概括或修改任何原有的业务逻辑、细化标准和模板格式！

最后在审查一次.agents/skills/design-chapters（skill、references、scripts），从多角度、全局考虑，有任何问题都可以提出来

反思、提炼的改动，然后分析是否有可以落实到.agents/skills/SKILL_TEMPLATE.md的内容

好，帮我使用commit-msg进行commit，然后push

