# 名字解析协议（Name Resolution Protocol）

> 本协议适用于所有生成或改写文本的 skill（chapter-draft、anti-ai-rewrite、rewrite、voice-check 对白示例等）。

## 核心原则

**称呼是叙事行为，不是数据库查询。** 选择哪个称呼取决于"谁在看/想"，而不是角色卡上写了什么。

## 1. 称呼选择规则（生成/改写时）

### 1a. 已有草稿的改写场景

**保留作者已用的称呼，不做任何替换。**（重申 `draft-primacy.md` 的称呼保留规则）

- 作者写"老王"→ 保留"老王"
- 作者写"那个女人"→ 保留
- 作者写绰号/外号/代称 → 全部保留
- 发现同一角色多种称呼 → 在报告中提一句，不统一

### 1b. 无草稿的新生成场景（chapter-draft 等）

按以下优先级选择称呼：

1. **读取该章节 POV 角色与目标角色的关系**（`relations.yaml`）
2. **按亲疏度映射称呼形式**：

| 关系亲疏 | 称呼选择 | 示例 |
|----------|---------|------|
| 亲密/信任 | aliases 中的昵称，或名字中的单字 | "老赵"、"小宋"、"阿声" |
| 普通/同级 | 全名或姓+称谓 | "赵宋"、"纪微" |
| 疏远/敌对 | 姓+称谓或蔑称 | "赵先生"、"那个人"、"庄家的人" |
| POV 角色的内心独白 | 最自然的称呼，可以是"他/她" | 按情绪变化切换 |

3. **同一段落内保持称呼一致**，跨段落可因情绪变化切换
4. 如果角色 `aliases` 为空，用全名（不要编造昵称）

### 1c. 对白中的称呼

对白中的称呼由说话者决定，不由叙述者决定：
- 粗人叫别人 → 可能用外号/简称
- 尊长叫晚辈 → 可能用小名或单字
- 敌人之间 → 可能用姓氏或蔑称

## 2. 命名规范（character-add 起名时）

### 2a. 读取项目命名配置

从 `{current_path}/.novel/meta.yaml` 的 `naming` 区块读取：

```yaml
naming:
  era: modern         # modern / ancient / fantasy / mixed
  culture: chinese    # chinese / western / japanese / mixed
  style_notes: ""     # 自由备注
  forbidden_patterns: []
```

### 2b. 命名原则

| 配置 | 命名策略 |
|------|---------|
| modern + chinese | 常见姓名：张明、李向前、王妮、赵宋。不用生僻字、不用四字名（除非有剧情原因）、不用过度文艺的名字 |
| ancient + chinese | 可用文雅名，但仍优先辨识度：陆渊、沈知、白鹤龄。避免"X天X"/"X云X"等烂大街仙侠名 |
| fantasy | 可创造，但要求念起来顺口、有记忆点。避免一眼看不出怎么念的名字 |
| mixed | 按角色所属文化圈分别处理 |

### 2c. 验证

- 检查 `forbidden_patterns`（正则匹配）
- 检查已有角色名单，避免同音不同字（"赵松" vs "赵宋"需提示）
- 用户没有特别要求时，**默认走 modern + chinese 策略**

## 3. 重命名协议（character-edit --rename 时）

### 3a. 第一步：影响预览（Dry-run）

扫描以下文件，列出所有匹配项：

| 文件类型 | 搜索内容 |
|---------|---------|
| `characters/{old_name}.yaml` | 文件名本身 |
| `characters/character_index.yaml` | name 和 file 字段 |
| `characters/relations.yaml` | 所有 character 字段 |
| `characters/relation_events.yaml` | 角色名出现 |
| `chapters/*.md` | 正文中**确切名字**出现（不含代词/代称/描述性称呼） |
| `plot/outline.md` | 名字出现 |
| `timeline/main.yaml` | characters 字段 |
| `worldbuilding/entries/*.yaml` | character_links 中的名字 |

输出影响报告：

```
📝 重命名影响预览：张三 → 张树

  结构化文件（自动替换）：
  - characters/张三.yaml → 重命名为 characters/张树.yaml
  - character_index.yaml → 1 处
  - relations.yaml → 3 处
  - relation_events.yaml → 2 处
  - outline.md → 4 处
  - timeline/main.yaml → 1 处
  - entries/rule_001.yaml → 1 处

  章节正文（仅替换确切名字，不动代称）：
  - ch001.md → "张三" 出现 12 次
  - ch003.md → "张三" 出现 8 次
  - ⚠️ "三哥"、"老张" 等别称不会被替换，需手动检查

  不会被替换：
  - 代词（他/她/那个人）
  - aliases 中的别称（需手动更新 aliases 列表）

确认执行？(Y/N)
```

### 3b. 第二步：确认后批量执行

用户确认后，按上述清单依次替换。每个文件替换后校验格式正确性。

### 3c. 第三步：提示后续

```
✅ 重命名完成

💡 建议检查以下内容：
- aliases 列表是否需要更新（当前：["三哥", "老张"]）
- 是否有别称也需要跟着改
```

## 引用此协议的 skill

- `chapter-draft`（步骤 5 对白约束之前）
- `anti-ai-rewrite`（步骤 2D 对白口语化之前）
- `character-add`（步骤 2 起名时）
- `character-edit`（重命名时）
- `rewrite`（改写文本时）
