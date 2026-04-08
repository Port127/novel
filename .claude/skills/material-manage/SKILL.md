---
name: material-manage
description: 管理当前项目与素材库的关联（关联/取消/列表/可用素材）
when_to_use: 用户想关联素材到项目、取消关联、查看已关联素材或素材库概览
argument-hint: "link [素材ID] | unlink [素材ID] | list | available"
arguments: action
---

# 任务

管理当前项目与素材库（`../novel-material`）之间的引用关系。

## 前置检查

1. 确认 `../novel-material/` 目录存在
2. 读取 `.current.yaml` 获取 `current_path`
3. 读取 `{current_path}/.novel/materials.yaml`（如不存在则自动创建）

## 子命令

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `link` | 关联素材到当前项目 | `/material-manage link nm_novel_20260405_zhbk` |
| `unlink` | 取消素材关联 | `/material-manage unlink nm_novel_20260405_zhbk` |
| `list` | 列出当前项目已关联素材 | `/material-manage list` |
| `available` | 列出素材库中所有可用素材 | `/material-manage available` |

## 执行步骤

### link — 关联素材到当前项目

1. 读取 `../novel-material/data/index.yaml`，校验素材 ID 存在
2. 读取 `../novel-material/data/novels/{material_id}/meta.yaml`，获取名称、作者、状态、场景数
3. 检查 `materials.yaml` 的 `referenced_materials` 中是否已有该 ID
4. 如果已存在，提示并跳过
5. 追加条目并提示用户补充 `relevance`（可选）

### unlink — 取消素材关联

1. 检查 `materials.yaml` 中是否存在该 ID
2. 检查 `compliance/inspiration_log.yaml` 中是否有引用该素材的借鉴记录
3. 如果有借鉴记录，警告但不阻止
4. 从列表中移除

### list — 列出已关联素材

读取 `materials.yaml`，展示所有 `referenced_materials`。

### available — 列出素材库可用素材

读取 `../novel-material/data/index.yaml`，标注哪些已关联到当前项目。

## 输出格式

**link：**
```
素材已关联

{name}（{material_id}）
可用场景：{scenes_available}
已写入：.novel/materials.yaml

检索该素材：/material-search --material {material_id} {需求}
```

**unlink：**
```
素材已取消关联

{name}（{material_id}）
已更新：.novel/materials.yaml
```

**list：**
```
当前项目关联素材（{count} 部）

| # | 素材 | 作者 | 状态 | 场景数 | 关联说明 |
|---|------|------|------|--------|---------|
| 1 | {name} | {author} | {status} | {scenes} | {relevance} |

关联新素材：/material-manage link {id}
```

**available：**
```
素材库可用素材（{total} 部）

| # | 素材 | 作者 | 状态 | 已关联 |
|---|------|------|------|--------|
| 1 | {name} | {author} | {status} | Y/— |

关联素材：/material-manage link {id}
```

## 注意事项

- 只操作 `materials.yaml` 引用列表，不影响素材库本身
- `unlink` 不会删除已有的借鉴记录（`inspiration_log.yaml`）
- 如果素材库不存在，提示用户确认目录结构
