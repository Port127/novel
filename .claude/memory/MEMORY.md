# Memory Index

> 记忆系统索引，自动维护

## User

用户偏好和画像记忆。

<!-- 在 user/ 目录下创建记忆文件 -->

## Feedback

用户反馈和指导记忆。

<!-- 在 feedback/ 目录下创建记忆文件 -->

## Project

项目级别的决策和进度记忆。

<!-- 在 project/ 目录下创建记忆文件 -->

## Reference

外部资源引用记忆。

<!-- 在 reference/ 目录下创建记忆文件 -->

---

## 记忆类型说明

| 类型 | 用途 | 示例 |
|------|------|------|
| user | 用户画像、写作偏好 | "用户喜欢简洁文风" |
| feedback | 用户纠正、指导 | "不要用emoji" |
| project | 项目决策、进度 | "第一章已写完" |
| reference | 外部资源引用 | "素材库在 ../novel-material/data/" |

## 记忆文件格式

```markdown
---
name: 记忆名称
description: 一行描述
type: user | feedback | project | reference
---

记忆内容

**Why**: 为什么记录这条
**How to apply**: 如何应用
```