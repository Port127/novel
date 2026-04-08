# 前端文档

> 小说工作台 — 面向网文作者的 AI 写作管理平台。

---

## 第一部分：使用指南

### 快速开始

1. **启动服务**：在终端运行 `cd frontend && ./start.sh`（同时启动前后端）
2. **打开浏览器**：访问 http://localhost:5173
3. **配置 LLM**：首次使用需进入「设置」页面配置大模型 API（详见下方）

### 界面概览

左侧边栏是主导航，分四组：

| 分组 | 包含页面 |
|------|---------|
| 总览 | 仪表板 |
| 创作 | 角色、世界观、大纲、章节、时间线、关系 |
| 质量 | 写作质量、合规检查 |
| 工具 | 流水线、AI 助手、设置 |

侧边栏顶部可切换不同小说项目，底部可切换深色/浅色主题。

---

### 首次配置：接入大模型

进入**设置 → LLM 配置**：

1. **API URL** — 填入大模型的 chat completions 端点，例如：
   - OpenAI: `https://api.openai.com/v1/chat/completions`
   - DeepSeek: `https://api.deepseek.com/v1/chat/completions`
   - 其他兼容 OpenAI 格式的 API 均可
2. **API Token** — 填入对应的 API Key（`sk-...`）
3. **模型名称** — 如 `gpt-4o`、`deepseek-chat` 等
4. **Temperature** — 创意度，建议 0.7（更高更发散，更低更收敛）
5. **Max Tokens** — 单次回复最大长度，建议 4096 或更高
6. 点击**保存配置**，再点击**测试连接**确认可用

> 配置保存在本地浏览器中，不会上传到任何服务器。API Key 通过后端代理调用，不会暴露在浏览器网络请求中。

---

### 各页面使用说明

#### 仪表板

打开即可看到当前项目的全景数据：

- **四张 KPI 卡片**：总字数、章节数、角色数、设定条目数
- **章节状态分布**：以进度条形式展示各状态（想法/大纲/草稿/修订/定稿/已发布）的章节数量
- **最近更新章节**：点击可直接跳转到章节编辑器
- **快捷操作**：一键跳转到新建章节、管理角色、AI 助手、质量检查

#### 角色管理

**角色列表**（`/characters`）
- 以卡片网格展示所有角色
- 卡片颜色和图标按角色类型区分：主角（金色）、配角（蓝色）、反派（红色）、路人（灰色）
- 顶部搜索栏支持按名字搜索
- 点击筛选按钮可按角色类型过滤

**角色详情**（点击角色卡片进入）

四个 Tab 页：
1. **基本信息**：姓名、角色定位、原型、首次登场、外貌、背景故事、能力
2. **心理画像**：五件套 — 致命缺陷、执念、软肋、错误信念、反差习惯，以及说话风格
3. **角色弧光**：成长阶段时间轴
4. **关系**：与其他角色的关系列表

> **编辑角色**：点击右上角「编辑」按钮进入编辑模式，所有字段变为可编辑。修改后点击「保存」提交。

#### 世界观

**设定列表**（`/worldbuilding`）
- 顶部展示核心概念卡片（如世界规则、力量体系）
- 下方以网格展示全部设定条目
- 每个条目显示名称、分类图标、状态标签（tentative/confirmed/deprecated）

**设定详情**（点击条目进入）
- 显示完整描述、规则、约束条件
- 关联角色、关联剧情节点
- 待解决问题列表

#### 大纲

四个 Tab 页切换：
1. **大纲**：Markdown 编辑器，点击「编辑」可直接修改大纲文本，支持实时预览
2. **伏笔追踪**：列出所有已埋设和已回收的伏笔
3. **紧张度曲线**：折线图展示各章节的情感紧张度变化
4. **结构**：按幕/阶段展示故事骨架

#### 章节

**章节看板**（`/chapters`）

Kanban 风格，6 列对应 6 个状态：

| 列 | 状态 | 含义 |
|----|------|------|
| 想法 | idea | 只有灵感片段 |
| 大纲 | outline | 已有章节大纲 |
| 草稿 | draft | 正在写初稿 |
| 修订 | revise | 初稿完成，正在打磨 |
| 定稿 | final | 已定稿 |
| 已发布 | published | 已发布上线 |

每张章节卡显示：编号、标题、视角角色、字数、登场角色标签。点击卡片进入编辑器。

**章节编辑器**（点击章节卡片进入）
- 左侧：Markdown 编辑器，支持「编辑」和「预览」两种模式切换
- 右侧：信息面板
  - 章节摘要
  - 登场角色
  - 已埋伏笔 / 已回收伏笔
  - 字数进度条（当前字数 / 目标字数）
- 编辑完成后点击**保存**按钮

#### 时间线

纵向时间轴视图，每个事件卡片显示：
- 时间标记
- 事件描述
- 所属章节
- 发生地点
- 相关角色标签

用于检查故事时间线是否连贯，发现时序矛盾。

#### 关系

- **关系卡片网格**：每张卡片展示一对关系——关系类型（镜像/守护/共生等）、动态描述、张力来源
- **关系强度条**：可视化展示关系当前的亲密/对抗程度
- **关系事件**：侧栏列出关系变化的关键节点（何时关系升温/破裂/重建）

#### 写作质量

展示 AI 痕迹检测结果：
- **总评分**：等级（A-D）+ 百分制分数
- **七维雷达图**：套话、句式、比喻、描写、对白、转折、心理 各维度得分
- **主要问题列表**：标注需要关注的 AI 感段落
- **历史记录**：查看过往检测记录的趋势

#### 合规检查

两个 Tab 页：
1. **风险报告**：按风险等级（高/中/低）列出借鉴风险点，显示涉及章节、相似来源、建议
2. **借鉴登记**：台账式记录每次借鉴的来源、维度（情节/设定/人物/语句）、处理措施

#### 流水线

8 个预置工作流卡片，覆盖写作全流程：

| 流水线 | 用途 | 产出 |
|--------|------|------|
| 大纲初建 | 从草稿/想法推导初版大纲 | 可写大纲 + 基础设定 |
| 大纲优化 | 审查补强已有大纲 | 优化后大纲 |
| 设定整固 | 清理 tentative 设定，补缺口 | 稳定设定集 |
| 笔记分拣 | 混合笔记自动分类归档 | 归档到对应模块 |
| 章节开局 | 创建新章节 + 补全情节点 | 可开写章节 |
| 草稿打磨 | 结构审查 + 声音检查 + 去 AI 感 | 可修订草稿 |
| 连续性闸口 | 关系/时间线/一致性检查 | 修复清单 |
| 合规闸口 | 借鉴登记 + 风险检查 | 发布前闸口 |

点击「运行」按钮会跳转到 AI 助手页面执行对应 Skill。

#### AI 助手

核心交互页面，支持两种模式：

**自由对话模式**
- 直接在输入框输入问题，与大模型自由交流
- 可以咨询写作建议、讨论剧情走向、请求文本改写等
- 对话历史在页面内保持，点击「清空」重置

**Skill 模式**
- 点击右上角「选择技能」下拉菜单
- 55+ 个专业技能按分类分组（章节、角色、大纲、世界观、质量等）
- 选择技能后，输入框变为指令输入
- AI 会按照技能的专业流程执行任务，而非简单对话

> **提示**：如果页面顶部出现黄色提示条"尚未配置 LLM"，请先前往设置页面配置。

使用技巧：
- `Shift + Enter` 可以在输入框内换行
- AI 回复支持 Markdown 格式（表格、代码块、列表等）
- 回复实时流式显示，无需等待全部生成

#### 设置

两个 Tab 页：
1. **LLM 配置**：API 接入参数（见上方"首次配置"）
2. **外观**：深色/浅色模式切换

---

### 典型工作流

#### 写一章新的正文

1. **仪表板** → 点击「新建章节」→ 进入 AI 助手
2. 选择「章节开局」技能，描述这一章的要点
3. AI 返回章节结构后，前往**章节看板**查看新章节
4. 点击章节卡片进入**编辑器**，开始写作
5. 完成初稿后，回到 AI 助手选择「草稿打磨」技能
6. 根据反馈修改，在看板上将状态推进到「修订」→「定稿」

#### 创作新项目

1. 通过 Cursor 中的 AI agent 使用 `/novel-init` 命令创建项目
2. 准备好草稿或灵感笔记
3. 在 AI 助手中运行「大纲初建」流水线
4. 运行「设定整固」流水线确认世界观
5. 开始逐章创作

#### 发布前检查

1. 运行「连续性闸口」→ 检查时间线和关系一致性
2. 运行「合规闸口」→ 检查借鉴风险
3. 查看**写作质量**页面的 AI 痕迹评分
4. 全部通过后，将章节状态推进到「已发布」

---

## 第二部分：技术文档

### 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| React | 18 | UI 框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 8 | 构建工具 + 开发服务器 |
| TailwindCSS | 4 | 原子化 CSS |
| shadcn/ui | latest | 25 个 UI 组件（基于 Radix UI） |
| React Router | 7 | 客户端路由 |
| Zustand | latest | 全局状态管理（persist 到 localStorage） |
| Recharts | latest | 图表（紧张度曲线、七维雷达图） |
| react-markdown | latest | Markdown 渲染 |
| remark-gfm | latest | GitHub Flavored Markdown 支持 |
| Lucide React | latest | 图标库 |
| clsx + tailwind-merge | latest | 条件 className 合并 |

### 目录结构

```
frontend/
├── src/
│   ├── main.tsx                # 入口：BrowserRouter + TooltipProvider + Toaster
│   ├── App.tsx                 # 路由表（15 个页面）+ 深色模式切换
│   ├── index.css               # TailwindCSS v4 + shadcn 主题变量
│   │
│   ├── types/index.ts          # 全量 TypeScript 类型
│   ├── stores/app-store.ts     # Zustand 全局状态
│   ├── services/api.ts         # 后端 API 调用层（含响应格式转换）
│   ├── hooks/use-fetch.ts      # 通用数据请求 Hook
│   │
│   ├── layouts/
│   │   └── AppLayout.tsx       # 侧边栏 + 面包屑 + 主内容区
│   │
│   ├── components/
│   │   ├── app-sidebar.tsx     # 侧边栏导航 + 项目切换器
│   │   ├── stat-card.tsx       # KPI 统计卡片
│   │   ├── status-badge.tsx    # 状态标签
│   │   └── ui/                 # shadcn/ui 组件（25 个）
│   │
│   └── pages/
│       ├── Dashboard.tsx
│       ├── characters/         # CharacterList + CharacterDetail
│       ├── worldbuilding/      # WorldbuildingList + SettingDetail
│       ├── chapters/           # ChapterBoard + ChapterEditor
│       ├── plot/               # PlotOutline
│       ├── timeline/           # TimelineView
│       ├── relationships/      # RelationshipGraph
│       ├── quality/            # QualityDashboard
│       ├── compliance/         # ComplianceReport
│       ├── pipelines/          # PipelineList
│       ├── skills/             # SkillRunner
│       └── settings/           # Settings
│
├── vite.config.ts              # Vite 配置（Tailwind 插件 + API proxy）
├── components.json             # shadcn/ui 配置
├── tsconfig.json               # TypeScript 配置（路径别名 @/ → src/）
├── package.json
└── start.sh                    # 一键启动前后端
```

### 路由表

| 路由 | 组件 | 说明 |
|------|------|------|
| `/` | → `/dashboard` | 重定向到仪表板 |
| `/dashboard` | Dashboard | 仪表板 |
| `/characters` | CharacterList | 角色列表 |
| `/characters/:name` | CharacterDetail | 角色详情 |
| `/worldbuilding` | WorldbuildingList | 世界观列表 |
| `/worldbuilding/:id` | SettingDetail | 设定详情 |
| `/plot` | PlotOutline | 大纲编辑器 |
| `/chapters` | ChapterBoard | 章节看板 |
| `/chapters/:id` | ChapterEditor | 章节编辑器 |
| `/timeline` | TimelineView | 时间线 |
| `/relationships` | RelationshipGraph | 关系图谱 |
| `/quality` | QualityDashboard | 写作质量 |
| `/compliance` | ComplianceReport | 合规检查 |
| `/pipelines` | PipelineList | 流水线列表 |
| `/skills` | SkillRunner | AI 助手 |
| `/settings` | Settings | 设置 |

### 全局状态 (Zustand)

```typescript
interface AppState {
  currentProject: ProjectListItem | null
  projects: ProjectListItem[]
  sidebarOpen: boolean
  darkMode: boolean
  llmConfig: LLMConfig
}
```

- 存储键名：`novel-app-store`
- 自动持久化到 `localStorage`（darkMode 和 llmConfig 跨刷新保留）
- LLM 配置默认 `api_url` 为 `https://api.openai.com/v1/chat/completions`

### API 调用层

`src/services/api.ts` 封装所有后端请求，核心职责：

1. **基础 HTTP 封装**：`get()`, `post()`, `put()`, `del()` 函数
2. **响应格式转换**：后端返回的嵌套 JSON → 前端扁平化类型

转换示例：
| 后端返回 | 前端接收 |
|---------|---------|
| `{entries: [...], total: N}` | `CharacterEntry[]` |
| `{chapters: [...]}` | `ChapterMeta[]` |
| `{markdown: "...", structured: {...}}` | `PlotOutline` |

3. **LLM 配置映射**：前端 `api_token` → 后端 `api_key`

### Vite 代理配置

开发环境中，Vite 将 `/api` 请求代理到后端：

```typescript
// vite.config.ts
server: {
  proxy: {
    "/api": {
      target: "http://localhost:8000",
      changeOrigin: true,
    }
  }
}
```

### 添加新页面

1. 在 `src/pages/xxx/` 创建组件
2. 在 `src/App.tsx` 添加 `<Route path="/xxx" element={<XxxPage />} />`
3. 在 `src/components/app-sidebar.tsx` 的 `navGroups` 中添加导航项
4. 在 `src/layouts/AppLayout.tsx` 的 `titleMap` 中添加面包屑标题

### 添加新 UI 组件

```bash
npx shadcn@latest add button    # 示例：添加 button 组件
```

组件会安装到 `src/components/ui/`，可直接导入使用。
