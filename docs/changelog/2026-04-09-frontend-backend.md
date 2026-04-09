# 2026-04-09 会话记录：前后端 Web 界面搭建

## 会话概要

为小说工作台搭建完整的 Web 前后端，实现项目数据的可视化管理界面和 LLM 代理服务。经历了技术选型、前后端全量开发、目录结构调整、问题修复和文档编写。

---

## 一、技术选型与方案设计

**用户需求：**
- 在 `frontend/` 目录下创建 Web 界面
- 实现本项目所有功能的可视化操作
- 支持通过 URL + Token 接入第三方大模型
- 美观大方，使用 React

**最终方案：**
- 前端：React 18 + TypeScript + Vite 8 + TailwindCSS v4 + shadcn/ui + Zustand
- 后端：Python FastAPI + ruamel.yaml + httpx + sse-starlette
- 通信：Vite dev proxy → FastAPI，LLM 调用通过后端代理（保护 API Key）
- 存储：无数据库，直接读写项目目录下的 YAML/MD 文件

> 用户明确要求后端使用 Python 而非 Node.js。

---

## 二、后端开发（FastAPI）

### 核心模块

| 模块 | 文件 | 职责 |
|------|------|------|
| 配置中心 | `backend/config.py` | 项目路径解析、LLM 配置读写 |
| YAML 服务 | `backend/services/yaml_service.py` | ruamel.yaml 读写（保留注释格式） |
| LLM 服务 | `backend/services/llm_service.py` | httpx 流式调用 OpenAI 兼容 API |
| 应用入口 | `backend/main.py` | 路由挂载、CORS 配置 |

### API 路由（11 个模块，30+ 端点）

| 路由模块 | 端点前缀 | 功能 |
|----------|---------|------|
| projects | `/api/projects` | 项目列表、当前项目、切换 |
| characters | `/api/characters` | 角色 CRUD + 索引同步 |
| worldbuilding | `/api/worldbuilding` | 世界观 CRUD + 索引同步 |
| chapters | `/api/chapters` | 章节 CRUD + 正文 + 元数据 |
| plot | `/api/plot` | 大纲 Markdown + YAML 读写 |
| timeline | `/api/timeline` | 时间线事件查询 + 添加 |
| relationships | `/api/relationships` | 关系图谱 + 演进事件 |
| compliance | `/api/compliance` | 借鉴登记 + 风险报告 |
| quality | `/api/quality` | AI 痕迹报告 |
| llm | `/api/llm` | LLM 配置 + SSE 流式对话 |
| skills | `/api/skills` | Skill 扫描 + SSE 流式执行 |

### 关键设计

- **索引 + 详情分离**：角色/世界观/章节均采用索引文件 + 独立详情文件，列表快、写入双写
- **Skill 执行引擎**：复用 `.claude/skills/*/SKILL.md` 作为 prompt 模板，自动注入 meta + state 上下文
- **LLM 代理**：前端不直连 LLM，统一通过后端 SSE 代理，API Key 不暴露给浏览器

---

## 三、前端开发（React）

### 基础设施

| 组件 | 说明 |
|------|------|
| `vite.config.ts` | TailwindCSS 插件 + `/api` 代理到后端 |
| `index.css` | TailwindCSS v4 + shadcn/ui 主题变量（明暗双主题） |
| `components.json` | shadcn/ui 配置（new-york 风格） |
| `stores/app-store.ts` | Zustand 全局状态（项目、LLM 配置、主题），persist 到 localStorage |
| `services/api.ts` | 后端 API 调用层，含响应格式转换（嵌套 JSON → 扁平类型） |
| `types/index.ts` | 全量 TypeScript 类型定义 |
| `hooks/use-fetch.ts` | 通用数据请求 Hook |

### 页面（15 个）

| 页面 | 路由 | 功能 |
|------|------|------|
| 仪表板 | `/dashboard` | KPI 卡片、章节状态分布、最近更新、快捷操作 |
| 角色列表 | `/characters` | 卡片网格 + 类型筛选 + 搜索 |
| 角色详情 | `/characters/:name` | 四 Tab（基本信息/心理画像/弧光/关系）+ 内联编辑 |
| 世界观列表 | `/worldbuilding` | 核心概念卡片 + 条目网格 + 分类筛选 |
| 设定详情 | `/worldbuilding/:id` | 描述/规则/约束/关联角色/关联剧情 |
| 大纲 | `/plot` | 四 Tab（Markdown 编辑器/伏笔追踪/紧张度曲线/结构概览） |
| 章节看板 | `/chapters` | 6 列 Kanban（想法→大纲→草稿→修订→定稿→已发布） |
| 章节编辑器 | `/chapters/:id` | Markdown 编辑/预览 + 侧边信息面板 |
| 时间线 | `/timeline` | 纵向时间轴视图 |
| 关系图谱 | `/relationships` | 关系卡片网格 + 强度条 + 事件列表 |
| 写作质量 | `/quality` | AI 痕迹评分 + 七维雷达图 + 历史记录 |
| 合规检查 | `/compliance` | 风险报告 + 借鉴登记双 Tab |
| 流水线 | `/pipelines` | 8 个预置工作流卡片 |
| AI 助手 | `/skills` | 聊天界面 + 55+ Skill 选择 + SSE 流式输出 |
| 设置 | `/settings` | LLM 配置 + 测试连接 + 深色模式 |

### UI 组件

安装了 25 个 shadcn/ui 组件（button, card, tabs, dialog, dropdown-menu, sidebar, scroll-area, badge, input, textarea, label, switch, separator, tooltip, avatar, chart 等）。

---

## 四、目录结构调整

**问题**：最初后端代码放在 `frontend/server/`，不符合常规项目结构。

**用户要求**：后端放在 `backend/`，与 `frontend/` 同级。

**执行步骤**：
1. 将 `frontend/server/` 移动到项目根目录的 `backend/`
2. 全局替换 Python 文件中 `from server.xxx` → `from backend.xxx`
3. 修正 `config.py` 的 `WORKSPACE_ROOT` 路径计算
4. 更新 `main.py` 的 uvicorn 启动命令（`backend.main:app`，`reload_dirs=["backend"]`）
5. 更新 `frontend/start.sh` 启动脚本的路径
6. 清理 `__pycache__`，重启验证

---

## 五、问题修复

### 5.1 shadcn/ui 初始化失败

**现象**：`npx shadcn@latest init` 无法检测到 Tailwind 配置
**原因**：TailwindCSS v4 使用新的配置方式，shadcn 检测逻辑不兼容
**修复**：手动创建 `components.json`、`src/lib/utils.ts`，在 `index.css` 中配置 `@import "tailwindcss"` + shadcn 主题变量

### 5.2 后端频繁崩溃

**现象**：后端启动后几秒内自动重启
**原因**：`--reload` 监视了整个 `frontend/` 目录，前端构建触发后端重载
**修复**：添加 `--reload-dir backend` 限制监视范围

### 5.3 仪表板数据为空

**现象**：Dashboard 页面所有 KPI 显示为 0
**原因**：前端 API 层直接返回后端的嵌套响应，未提取内部数组
**修复**：在 `services/api.ts` 中添加响应格式转换，提取 `entries`/`chapters` 等嵌套字段

### 5.4 测试连接按钮无法点击

**现象**：设置页面的"测试连接"按钮始终 disabled
**原因**：`api_url` 默认值为空字符串，disabled 条件判断了 `!form.api_url`
**修复**：设置默认 `api_url` 为 `https://api.openai.com/v1/chat/completions`，调整 disabled 条件

### 5.5 角色编辑按钮无响应

**现象**：角色详情页的"编辑"按钮点击无反应
**原因**：按钮缺少 `onClick` handler
**修复**：实现完整的内联编辑功能（编辑模式切换、表单状态、保存调用）

### 5.6 旧进程占用端口

**现象**：后端返回 404（旧的 `python main.py` 进程占用 8000 端口）
**修复**：`lsof -ti:8000 | xargs kill -9`，然后用正确的命令重启

---

## 六、文档编写

### 新建

| 文件 | 内容 |
|------|------|
| `docs/backend.md` | 后端技术文档：架构、API 规格（全部端点）、核心模块、开发指南 |
| `docs/frontend.md` | 前端文档：**使用指南**（首次配置、各页面操作、典型工作流）+ **技术文档**（技术栈、目录、路由、状态管理） |
| `frontend/README.md` | 前端项目 README |

> 最初写了合并的 `docs/frontend-backend.md`，后按用户要求拆分为独立的 `docs/backend.md` + `docs/frontend.md`，并在前端文档中增加了使用者视角的操作指南。

---

## 文件变更清单

### 新建（90 个文件）

```
backend/
  __init__.py
  config.py
  main.py
  requirements.txt
  routers/__init__.py
  routers/projects.py
  routers/characters.py
  routers/worldbuilding.py
  routers/chapters.py
  routers/plot.py
  routers/timeline.py
  routers/relationships.py
  routers/compliance.py
  routers/quality.py
  routers/llm.py
  routers/skills.py
  services/__init__.py
  services/yaml_service.py
  services/llm_service.py

frontend/
  index.html
  package.json
  package-lock.json
  tsconfig.json
  tsconfig.app.json
  tsconfig.node.json
  vite.config.ts
  components.json
  eslint.config.js
  start.sh
  README.md
  public/favicon.svg
  public/icons.svg
  src/main.tsx
  src/App.tsx
  src/index.css
  src/types/index.ts
  src/stores/app-store.ts
  src/services/api.ts
  src/hooks/use-fetch.ts
  src/lib/utils.ts
  src/layouts/AppLayout.tsx
  src/components/app-sidebar.tsx
  src/components/stat-card.tsx
  src/components/status-badge.tsx
  src/components/ui/  （25 个 shadcn/ui 组件）
  src/pages/Dashboard.tsx
  src/pages/characters/CharacterList.tsx
  src/pages/characters/CharacterDetail.tsx
  src/pages/worldbuilding/WorldbuildingList.tsx
  src/pages/worldbuilding/SettingDetail.tsx
  src/pages/chapters/ChapterBoard.tsx
  src/pages/chapters/ChapterEditor.tsx
  src/pages/plot/PlotOutline.tsx
  src/pages/timeline/TimelineView.tsx
  src/pages/relationships/RelationshipGraph.tsx
  src/pages/quality/QualityDashboard.tsx
  src/pages/compliance/ComplianceReport.tsx
  src/pages/pipelines/PipelineList.tsx
  src/pages/skills/SkillRunner.tsx
  src/pages/settings/Settings.tsx

docs/
  backend.md
  frontend.md
  changelog/2026-04-09-frontend-backend.md  （本文件）
```

### 修改

```
.gitignore  （新增 Python 缓存 + llm_config.json 忽略规则）
```
