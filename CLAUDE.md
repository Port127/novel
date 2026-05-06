# Project Rules

## 授权模式

本项目使用**完全授权模式**。Claude 可以自主执行以下操作，无需用户确认：

### Bash 命令
- 所有 Bash/Shell 命令
- Git 操作（commit、push、reset、force push 等）
- 文件系统操作（rm、mv、cp 等）
- 包管理器（npm、yarn、pip 等）
- 任意脚本执行

### 文件操作
- 读取任意文件
- 创建新文件
- 编辑现有文件
- 删除文件

### 网络操作
- Web 搜索
- Web 获取

### 其他操作
- 运行后台任务
- 执行测试
- 部署操作

## 注意事项

- 敏感操作（如 force push、删除文件）仍会显示提示，但 Claude 可自主决定执行
- 如需调整权限，编辑 `.claude/settings.json` 文件