---
name: paywall-design
description: 付费卡点设计。分析大纲找最优切割点，设计过渡章节奏。
---

# 付费卡点设计

分析大纲，找到最优付费切割点，设计过渡章节奏。

---

## 前置依赖

- 大纲已完成
- 黄金三章已完成

---

## 工作流程

### 1. 分析大纲

```python
from novel.core.skills.design_paywall import DesignPaywallSkill
skill = DesignPaywallSkill()
analysis = await skill.analyze_outline(outline_text)
```

### 2. 展示推荐卡点

输出：
- 推荐切割章节
- 切割理由（爽点兑现 + 新悬念）
- 警告（如当前处于主角低谷期）

### 3. 设计过渡章

**免费末章**：
- 必须做到"爽点兑现 + 致命悬念"双保险
- 读者合上这一章时，必须"不花钱就难受"

**付费首章**：
- 开头 200 字内必须立刻给出爽感反馈
- 随后展开新弧线

### 4. 评估过渡章

```python
verdict = await skill.evaluate(transition_chapter_text)
```

检查：
- 爽点是否兑现？
- 悬念是否抛出？

### 5. 输出

生成 `paywall_report.yaml`：

```yaml
paywall_chapter: 25
reasoning: "第24章主角首次击败小反派（爽点兑现），第25章开头大反派登场（新悬念）"
free_last_chapter_design:
  - 爽点兑现
  - 致命悬念抛出
paid_first_chapter_design:
  - 200字内爽感反馈
  - 展开新弧线
```

---

## 输出文件

- `paywall_report.yaml`

## 参考

- 引擎: `src/novel/core/skills/design_paywall.py`
