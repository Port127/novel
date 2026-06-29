---
name: daily-write
description: 日更写作入口。扩写 → 核查 → 去AI味 → 钩子审查，通过质量门禁后定稿。
---

# 日更写作

交互式写作章节正文，通过质量门禁流水线确保输出质量。

---

## 前置依赖

- 章节已规划（`settings/chapters_index.yaml` 有摘要）

---

## 工作流程

### 1. 选择章节

展示待写章节列表，选择本章目标。

### 2. 检查衔接

展示前章结尾 300 字 + 本章摘要，确认衔接点。

### 3. 写作方向

询问写作方向（情节推进/人物展示/环境氛围/对话为主）。

### 4. 生成正文

Agent 直接生成正文（2000-3000 字/章）。

### 5. 质量门禁流水线

生成后自动进入质量检查：

**Gate 1: 事实核查**
```python
from novel.core.skills.check_logic import CheckLogicSkill
skill = CheckLogicSkill()
verdict = await skill.evaluate({"content": chapter_text})
```
- 检查角色名称、时间线、地点一致性
- 未通过 → 给出修正建议

**Gate 2: 去 AI 味**
```python
from novel.core.skills.anti_ai_polish import AntiAiPolishSkill
skill = AntiAiPolishSkill()
verdict = await skill.evaluate(chapter_text)
```
- 五层检测（词汇/句式/段落/叙事/情感）
- 综合分 < 60 → 必须修改
- 检测到的禁词 → 列出替换建议

**Gate 3: 钩子审查**
```python
from novel.core.skills.audit_hooks import AuditHooksSkill
skill = AuditHooksSkill()
verdict = await skill.evaluate(chapter_text)
```
- 检查最后 800 字悬念强度
- 检查全文冲突密度
- 检查章节标题点击吸引力
- 未通过 → 建议修改结尾或标题

### 6. 展示正文 + 审查报告

展示正文开头 500 字 + 结尾 300 字 + 质量审查摘要。

### 7. 续写/改写

不满意时可选：
- **续写**：在已有正文基础上继续写作
- **改写**：修改已有正文（润色/扩充/精简/重写）
- **重新过审**：修改后重新跑质量门禁

### 8. 定稿

通过所有门禁后，写入 `content/chapter_XXX.md`。

---

## 质量门禁标准

| 门禁 | 检查项 | 通过标准 |
|------|--------|---------|
| 事实核查 | 角色/时间/地点一致性 | 无硬逻辑错误 |
| 去AI味 | 五层综合评分 | ≥ 60 分 |
| 钩子审查 | 悬念强度 | ≥ 60 分 |
| 钩子审查 | 冲突密度 | ≥ 60 分 |

---

## 输出文件

- `content/chapter_XXX.md`

## 参考

- 引擎: `src/novel/core/skills/anti_ai_polish.py`、`audit_hooks.py`、`check_logic.py`
- 旧模式: 旧 write-chapter 的续写/改写流程
