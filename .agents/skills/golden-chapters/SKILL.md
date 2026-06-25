---
name: golden-chapters
description: 黄金三章锻造。按微节拍逐段生成前三章，验证结构。
---

# 黄金三章锻造

前三章决定生死。按品类模板，逐段生成，严格验证结构。

---

## 前置依赖

- 品类已选择
- 人设已完成（`settings/characters/` 存在）
- 细纲已有初步方向

---

## 工作流程

### 1. 确认项目与品类

读取 `settings/scout_report.yaml` 获取品类。

### 2. 加载品类模板

```python
from novel.core.skills.forge_golden_chapters import ForgeGoldenChaptersSkill
skill = ForgeGoldenChaptersSkill()
template = skill.get_genre_template("genre/xuanhuan")
```

展示品类标准套路：

| 品类 | 标准套路 |
|------|---------|
| 玄幻 | 废柴受辱 → 金手指觉醒 → 首次反击 |
| 都市 | 被退婚/背叛 → 隐藏身份曝光 → 第一波打脸 |
| 系统文 | 系统激活 → 首个任务 → 奖励碾压 |

### 3. 逐章生成

**第一章**：
- 300 字内出第一冲突
- 立住主角人设
- 展示主角起点状态

**第二章**：
- 金手指亮相
- 展示金手指机制与限制

**第三章**：
- 第一个小高潮
- 让读者看到"爽"的可能性

### 4. 结构验证

每章生成后调用引擎验证：

```python
analysis = await skill.validate_chapter(
    text=chapter_text,
    chapter_number=1,
    genre_id="genre/xuanhuan"
)
```

检查清单：
- [ ] 首冲突 ≤ 300 字？
- [ ] 人设建立？
- [ ] 金手指亮相？
- [ ] 第一个小高潮？

未通过项给出修改建议。

### 5. 输出

生成 `content/chapter_001.md`、`chapter_002.md`、`chapter_003.md`。

输出评估报告：

```yaml
# golden_chapters_report.yaml
chapter_1:
  first_conflict_at_word: 250
  character_setup: true
  score: 85
chapter_2:
  golden_finger_reveal: true
  score: 80
chapter_3:
  first_climax: true
  score: 90
overall: 85
passed: true
```

---

## 输出文件

- `content/chapter_001.md`
- `content/chapter_002.md`
- `content/chapter_003.md`
- `golden_chapters_report.yaml`

## 参考

- 引擎: `src/novel/core/skills/forge_golden_chapters.py`
- 品类模板: `TEMPLATES` 字典
