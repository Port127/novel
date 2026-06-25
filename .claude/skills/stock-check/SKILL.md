---
name: stock-check
description: 存稿看板。查看存稿水位、成本报告、应急建议。
---

# 存稿看板

查看存稿状态、成本消耗、应急建议。

---

## 工作流程

### 1. 统计存稿

```python
from novel.core.workflow.daily_manager import DailyUpdateManager
from novel.core.workflow.manuscript_store import ManuscriptStore, ManuscriptTier

manager = DailyUpdateManager(
    written_chapters=written,
    published_chapters=published,
    mode="fine"
)
status = manager.check_reserves()
```

### 2. 展示看板

```
== 存稿看板 ==

存稿水位: 🟢 正常（12 章）
- 精修稿: 5 章（可直接发布）
- 粗稿: 4 章（需去AI味）
- 大纲稿: 3 章（需扩写）

成本报告:
- 今日消耗: $3.20
- 剩余预算: $11.80

建议:
- 存稿充足，可切换精细模式
```

### 3. 应急建议

| 水位 | 等级 | 建议 |
|------|------|------|
| ≥10 章 | 🟢 正常 | 正常运行 |
| 6-9 章 | 🟡 预警 | 暂停非紧急任务 |
| ≤5 章 | 🔴 危险 | 切换快速模式 |

---

## 输出

控制台报告（不写文件）

## 参考

- 引擎: `src/novel/core/workflow/daily_manager.py`、`manuscript_store.py`
