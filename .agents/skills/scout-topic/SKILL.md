---
name: scout-topic
description: 品类选择 + 选题分析。开新书或找题材时使用。
---

# 选题侦察兵

帮用户选择品类、分析市场、推荐标签组合。

---

## 工作流程

### 1. 确认项目

运行 `novel list` 查看项目列表。如果是新书，先创建项目：

```bash
novel new "书名" --genre 品类 --author 作者名
```

### 2. 选择品类

询问用户目标品类：

| 品类 | 特点 | 套路模板 |
|------|------|---------|
| 玄幻 | 升级打怪、宗门斗争 | 废柴流、退婚流、拍卖会 |
| 都市 | 打脸装逼、商战 | 退婚流、隐藏身份 |
| 系统文 | 任务奖励、数值碾压 | 系统激活、任务流 |
| 其他 | 用户自定义 | - |

**确认品类后**，调用品类路由：
```python
from novel.core.genre.profile import GenreRouter
router = GenreRouter()
router.set_genre("genre/<品类>")
```

### 3. 选题分析

与用户讨论：
- 目标平台（番茄/起点/其他）
- 目标读者群体
- 近期热门题材（可结合 `/nm` 检索）

输出选题报告：

```yaml
# settings/scout_report.yaml
genre: genre/xuanhuan
platform: 番茄小说
target_audience: 男频18-35
tag_combinations:
  - tags: [废柴流, 系统, 升级]
    competition_level: 0.6
    potential_score: 0.8
    window: "3-6个月"
recommended_tags: [废柴流, 系统, 升级]
reasoning: "低竞争高潜力，适合切入"
```

### 4. 展示与确认

展示选题报告，询问是否调整标签组合。确认后写入 `settings/scout_report.yaml`。

---

## 输出文件

- `settings/scout_report.yaml`

## 参考

- 品类画像配置：`src/novel/core/genre/profile.py`
- 选题引擎：`src/novel/core/skills/scout_topic.py`
