# References 移植 + SKILL.md 加厚 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从 oh-story-claudecode 移植 10 个核心 references 文件并加厚 4 个 SKILL.md，使 agent 有深度方法论可读、skill 流程能指导具体执行。

**Architecture:** 先移植 10 个 references（从 oh-story 复制 + 路径调整），再基于新 references 加厚 4 个 SKILL.md（从要点级别到可执行级别），最后同步 3 个 agent 定义的 references 表。按 skill 分组 commit。

**Tech Stack:** Markdown, YAML frontmatter

**Spec:** `docs/superpowers/specs/2026-06-30-references-and-skill-enhancement-design.md`

---

## File Structure

### 新建文件（10 个 references）

| 文件 | 职责 |
|------|------|
| `.agents/skills/daily-write/references/writing-craft.md` | 写作技法大全 |
| `.agents/skills/daily-write/references/dialogue-mastery.md` | 对话创作方法 |
| `.agents/skills/daily-write/references/emotional-methods.md` | 情绪技法 |
| `.agents/skills/daily-write/references/style-craft.md` | 风格技法 |
| `.agents/skills/daily-write/references/hooks-paragraph.md` | 段落级钩子 |
| `.agents/skills/daily-write/references/format-and-structure.md` | 格式与结构规范 |
| `.agents/skills/design-outline/references/plot-core-methods.md` | 情节核心方法 |
| `.agents/skills/design-outline/references/reversal-toolkit.md` | 反转设计 |
| `.agents/skills/design-character/references/character-relations.md` | 角色关系设计 |
| `.agents/skills/golden-chapters/references/opening-design.md` | 开篇设计 |

### 修改文件（7 个）

| 文件 | 改动范围 |
|------|---------|
| `.agents/skills/daily-write/SKILL.md` | Phase 3 加厚到 ~100 行，Phase 4/5 引用新 references |
| `.agents/skills/design-outline/SKILL.md` | 加入卷级大纲模板 + 细纲蓝图 + 五检清单 |
| `.agents/skills/design-character/SKILL.md` | 加入主角/反派/配角设计流程 + 语言风格档案步骤 |
| `.agents/skills/golden-chapters/SKILL.md` | 加入品类适配 + 单章锻造检查 + 开篇策略决策树 |
| `.agents/agents/narrative-writer.md` | 更新参考文件体系表（+6） |
| `.agents/agents/story-architect.md` | 更新参考文件体系表（+2） |
| `.agents/agents/character-designer.md` | 更新参考文件体系表（+1） |

---

## Task 1: 移植 6 个 references 到 daily-write

**Files:**
- Create: `.agents/skills/daily-write/references/writing-craft.md`（从 oh-story 复制）
- Create: `.agents/skills/daily-write/references/dialogue-mastery.md`（从 oh-story 复制）
- Create: `.agents/skills/daily-write/references/emotional-methods.md`（从 oh-story 复制）
- Create: `.agents/skills/daily-write/references/style-craft.md`（从 oh-story 复制）
- Create: `.agents/skills/daily-write/references/hooks-paragraph.md`（从 oh-story 复制）
- Create: `.agents/skills/daily-write/references/format-and-structure.md`（从 oh-story 复制）

- [ ] **Step 1: 复制 writing-craft.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/writing-craft.md \
   .agents/skills/daily-write/references/writing-craft.md
```

调整文件内所有 reference 路径引用：
- `story-setup/references/agent-references/` → `daily-write/references/`
- 其他 oh-story 特有路径 → 对应我们的路径

- [ ] **Step 2: 复制 dialogue-mastery.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/dialogue-mastery.md \
   .agents/skills/daily-write/references/dialogue-mastery.md
```

同样调整 reference 路径引用。

- [ ] **Step 3: 复制 emotional-methods.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/emotional-methods.md \
   .agents/skills/daily-write/references/emotional-methods.md
```

- [ ] **Step 4: 复制 style-craft.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/style-craft.md \
   .agents/skills/daily-write/references/style-craft.md
```

- [ ] **Step 5: 复制 hooks-paragraph.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/hooks-paragraph.md \
   .agents/skills/daily-write/references/hooks-paragraph.md
```

- [ ] **Step 6: 复制 format-and-structure.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/format-and-structure.md \
   .agents/skills/daily-write/references/format-and-structure.md
```

- [ ] **Step 7: 验证所有 6 个文件存在**

```bash
ls -la .agents/skills/daily-write/references/
```

Expected: 12 个 .md 文件（原 6 + 新 6）

- [ ] **Step 8: Commit（使用 commit-msg skill）**

```
feat(daily-write): 移植 6 个核心写作方法论 references
```

---

## Task 2: 移植 2 个 references 到 design-outline

**Files:**
- Create: `.agents/skills/design-outline/references/plot-core-methods.md`
- Create: `.agents/skills/design-outline/references/reversal-toolkit.md`

- [ ] **Step 1: 复制 plot-core-methods.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/plot-core-methods.md \
   .agents/skills/design-outline/references/plot-core-methods.md
```

调整 reference 路径引用。

- [ ] **Step 2: 复制 reversal-toolkit.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/reversal-toolkit.md \
   .agents/skills/design-outline/references/reversal-toolkit.md
```

- [ ] **Step 3: 验证**

```bash
ls -la .agents/skills/design-outline/references/
```

Expected: 7 个 .md 文件（原 5 + 新 2）

- [ ] **Step 4: Commit（使用 commit-msg skill）**

```
feat(design-outline): 移植 2 个情节方法论 references
```

---

## Task 3: 移植 1 个 reference 到 design-character

**Files:**
- Create: `.agents/skills/design-character/references/character-relations.md`

- [ ] **Step 1: 复制 character-relations.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/character-relations.md \
   .agents/skills/design-character/references/character-relations.md
```

- [ ] **Step 2: 验证**

```bash
ls -la .agents/skills/design-character/references/
```

Expected: 6 个 .md 文件（原 5 + 新 1）

- [ ] **Step 3: Commit（使用 commit-msg skill）**

```
feat(design-character): 移植角色关系设计 reference
```

---

## Task 4: 移植 1 个 reference 到 golden-chapters

**Files:**
- Create: `.agents/skills/golden-chapters/references/opening-design.md`

- [ ] **Step 1: 复制 opening-design.md 并调整路径**

```bash
cp ../other/oh-story-claudecode/skills/story-long-write/references/opening-design.md \
   .agents/skills/golden-chapters/references/opening-design.md
```

- [ ] **Step 2: 验证**

```bash
ls -la .agents/skills/golden-chapters/references/
```

Expected: 5 个 .md 文件（原 4 + 新 1）

- [ ] **Step 3: Commit（使用 commit-msg skill）**

```
feat(golden-chapters): 移植开篇设计 reference
```

---

## Task 5: 加厚 daily-write SKILL.md

**Files:**
- Modify: `.agents/skills/daily-write/SKILL.md`

- [ ] **Step 1: 读取当前 SKILL.md，定位 Phase 3 写作执行**

```bash
grep -n "Phase 3\|Phase 4\|写作执行" .agents/skills/daily-write/SKILL.md
```

- [ ] **Step 2: 加厚 Phase 3 写作执行**

将 Phase 3 从 ~20 行替换为 ~100 行，加入完整 13 步写作流程：

1. 写前准备（状态筛选 → 模块召回 → 文风确认 → 意图确认）
2. 写作（三维度揉进 → 对话差异化 → 情绪弧线执行 → 格式遵守）
3. 字数验证（wc -m → 欠账定位 → 重写/收敛）

每个子步骤引用对应的新 reference 文件。

- [ ] **Step 3: 微调 Phase 4 确定性检查**

在现有脚本检测后加入：
- 引用 `style-craft.md` 做风格检查
- 引用 `hooks-paragraph.md` 做段落级钩子检查

- [ ] **Step 4: 微调 Phase 5 LLM 评估**

在现有评估步骤后加入：
- 引用 `dialogue-mastery.md` 做对话质量评估
- 引用 `format-and-structure.md` 做格式合规检查

- [ ] **Step 5: 验证行数**

```bash
wc -l .agents/skills/daily-write/SKILL.md
```

Expected: ~420 行（原 228 + ~190）

- [ ] **Step 6: Commit（使用 commit-msg skill）**

```
feat(daily-write): 加厚 SKILL.md Phase 3-5 流程到可执行级别
```

---

## Task 6: 加厚 design-outline SKILL.md

**Files:**
- Modify: `.agents/skills/design-outline/SKILL.md`

- [ ] **Step 1: 读取当前 SKILL.md，定位 Phase 3-4**

```bash
grep -n "Phase 3\|Phase 4\|Phase 5\|出口条件" .agents/skills/design-outline/SKILL.md
```

- [ ] **Step 2: 加入卷级大纲模板**

在 Phase 3 末尾加入：

```markdown
### 卷级大纲模板

#### 第X卷：{卷名}（约 {N} 万字，{M} 章）
- 功能：{铺垫/起步/第一个大爽点}
- 核心事件：{一句话}
- 起始状态 → 结束状态：{主角从 {A} 变成 {B}}
- 对标结构坐标：{1/4 · 中点 · 3/4 关键情节锚点}
```

- [ ] **Step 3: 加入细纲蓝图模板**

在 Phase 3-4 之间加入细纲蓝图格式（内容概括五段式 + 情节安排多线 + 人物关系出场顺序 + 情节细化 + 结尾设定和钩子）。

- [ ] **Step 4: 加入大纲五检清单**

```markdown
### 大纲五检（每卷/每章设计前必答）

1. 本卷交付什么情绪？什么剧情模式能可靠交付？
2. 本卷核心冲突是什么？
3. 卷节奏（起承转合）哪段加速哪段减速？
4. 本卷需要新埋设的伏笔有哪些？上一卷待回收的伏笔如何处理？
5. 章节定位分布是否有高低层次？低压+过场是否克制（合计 ≤15%）？
```

- [ ] **Step 5: 引用新 references**

在相关步骤中加入：
- 引用 `plot-core-methods.md`（高潮构建蓄能→假胜→崩解）
- 引用 `reversal-toolkit.md`（反转设计自检清单）

- [ ] **Step 6: 验证行数**

```bash
wc -l .agents/skills/design-outline/SKILL.md
```

Expected: ~320 行（原 174 + ~146）

- [ ] **Step 7: Commit（使用 commit-msg skill）**

```
feat(design-outline): 加厚 SKILL.md 加入大纲模板和五检清单
```

---

## Task 7: 加厚 design-character SKILL.md

**Files:**
- Modify: `.agents/skills/design-character/SKILL.md`

- [ ] **Step 1: 读取当前 SKILL.md，定位 Phase 2-4**

```bash
grep -n "Phase 2\|Phase 3\|Phase 4\|Phase 5" .agents/skills/design-character/SKILL.md
```

- [ ] **Step 2: 加厚 Phase 2 主角设计**

加入完整设计流程：
- 三层标签反差人设法（身份标签 → 表现标签 → 内核标签）
- 九维深化步骤
- 动机链建立（起因→意图→约束→风险）
- 语言风格档案 7 维度建立步骤（引用 dialogue-mastery.md）

- [ ] **Step 3: 加厚 Phase 3 反派设计**

加入：
- 反派层级设计流程（小反派→中等反派→大弧Boss→最终Boss）
- 反派建立四要素（引用 villain-design.md）
- 镜像关系设计

- [ ] **Step 4: 加厚 Phase 4 配角与关系网络**

加入：
- 四种关系类型设计流程（冲突型/联盟型/亲密型/权威型）
- 好感度阶段建立
- 关系弧线设计要求
- 引用新 reference `character-relations.md`

- [ ] **Step 5: 验证行数**

```bash
wc -l .agents/skills/design-character/SKILL.md
```

Expected: ~310 行（原 198 + ~112）

- [ ] **Step 6: Commit（使用 commit-msg skill）**

```
feat(design-character): 加厚 SKILL.md 加入角色设计完整流程
```

---

## Task 8: 加厚 golden-chapters SKILL.md

**Files:**
- Modify: `.agents/skills/golden-chapters/SKILL.md`

- [ ] **Step 1: 读取当前 SKILL.md，定位 Phase 1-4**

```bash
grep -n "Phase 1\|Phase 2\|Phase 3\|Phase 4\|Phase 5" .agents/skills/golden-chapters/SKILL.md
```

- [ ] **Step 2: 加厚 Phase 1 品类适配**

加入：
- 品类适配检查清单（引用 genre-templates.md）
- 开篇策略选择决策树（引用新 reference `opening-design.md`）
- 9 种开头技巧速查

- [ ] **Step 3: 加厚 Phase 2-4 单章锻造**

每章锻造步骤加入：
- 单章锻造检查清单（前100字事件密度 ≥3、核心展示到位、章尾钩子强）
- 微节拍对照（引用 micro-beat-guide.md）
- 品类差异化要求（不同类型的第一/二/三章侧重点）

- [ ] **Step 4: 验证行数**

```bash
wc -l .agents/skills/golden-chapters/SKILL.md
```

Expected: ~310 行（原 211 + ~99）

- [ ] **Step 5: Commit（使用 commit-msg skill）**

```
feat(golden-chapters): 加厚 SKILL.md 加入品类适配和锻造检查
```

---

## Task 9: 更新 3 个 agent 定义的 references 表

**Files:**
- Modify: `.agents/agents/narrative-writer.md`（+6 条目）
- Modify: `.agents/agents/story-architect.md`（+2 条目）
- Modify: `.agents/agents/character-designer.md`（+1 条目）

- [ ] **Step 1: 更新 narrative-writer.md 的参考文件体系表**

在现有 8 个条目后新增 6 个：

```markdown
| `writing-craft.md` | 正文写作（三维度揉进、身体细节、疏密分配）时 | daily-write |
| `dialogue-mastery.md` | 写或审查对话场景（潜台词、权力博弈、差异化）时 | daily-write |
| `emotional-methods.md` | 情绪弧线执行、情绪节拍设计时 | daily-write |
| `style-craft.md` | 风格技法（打斗、装逼、日常写法）时 | daily-write |
| `hooks-paragraph.md` | 段落级钩子设计时 | daily-write |
| `format-and-structure.md` | 格式规范（段落节奏、语气标点谱系）时 | daily-write |
```

- [ ] **Step 2: 更新 story-architect.md 的参考文件体系表**

新增 2 个：

```markdown
| `plot-core-methods.md` | 高潮构建、AB交织法时 | design-outline |
| `reversal-toolkit.md` | 反转设计、嵌套反转、误导技巧时 | design-outline |
```

- [ ] **Step 3: 更新 character-designer.md 的参考文件体系表**

新增 1 个：

```markdown
| `character-relations.md` | 角色关系类型、好感度体系、关系弧线时 | design-character |
```

- [ ] **Step 4: Commit（使用 commit-msg skill）**

```
feat(agents): 同步 agent 定义文件的 references 表
```

---

## Task 10: 最终验证

- [ ] **Step 1: 验证所有新增 references 存在**

```bash
echo "=== daily-write references ==="
ls .agents/skills/daily-write/references/*.md | wc -l  # Expected: 12

echo "=== design-outline references ==="
ls .agents/skills/design-outline/references/*.md | wc -l  # Expected: 7

echo "=== design-character references ==="
ls .agents/skills/design-character/references/*.md | wc -l  # Expected: 6

echo "=== golden-chapters references ==="
ls .agents/skills/golden-chapters/references/*.md | wc -l  # Expected: 5
```

- [ ] **Step 2: 验证 SKILL.md 行数**

```bash
wc -l .agents/skills/daily-write/SKILL.md      # Expected: ~420
wc -l .agents/skills/design-outline/SKILL.md    # Expected: ~320
wc -l .agents/skills/design-character/SKILL.md  # Expected: ~310
wc -l .agents/skills/golden-chapters/SKILL.md   # Expected: ~310
```

- [ ] **Step 3: 验证 agent 定义的 references 表引用正确**

```bash
grep "writing-craft\|dialogue-mastery\|emotional-methods\|style-craft\|hooks-paragraph\|format-and-structure" .agents/agents/narrative-writer.md | wc -l  # Expected: 6
grep "plot-core-methods\|reversal-toolkit" .agents/agents/story-architect.md | wc -l  # Expected: 2
grep "character-relations" .agents/agents/character-designer.md | wc -l  # Expected: 1
```

- [ ] **Step 4: 验证所有 reference 引用解析到实际文件**

```bash
for ref in writing-craft dialogue-mastery emotional-methods style-craft hooks-paragraph format-and-structure plot-core-methods reversal-toolkit character-relations opening-design; do
  found=$(find .agents/skills -name "$ref.md" -type f 2>/dev/null | head -1)
  if [ -n "$found" ]; then echo "✅ $ref"; else echo "❌ $ref MISSING"; fi
done
```

Expected: 10 个全部 ✅

- [ ] **Step 5: 查看最终 git log**

```bash
git log --oneline -6
```

Expected: 5 个 commit（4 个 skill + 1 个 agents）
