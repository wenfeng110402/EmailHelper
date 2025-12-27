# 问题解决方案 / Solution Summary

## 问题 / Problem
"我在vscode提交代码不会同步到另外的这个分支上吗？"

用户在 VSCode 中提交代码后，希望代码能自动同步到其他分支（如 gh-pages）。

## 解决方案 / Solution

### 1. GitHub Actions 自动同步 (Auto-sync with GitHub Actions)

创建了 `.github/workflows/sync-branches.yml` 工作流：
- 当代码推送到 `master` 或 `main` 分支时自动触发
- 自动将更改合并到 `gh-pages` 分支
- 支持手动触发 (workflow_dispatch)

### 2. VSCode 自动推送配置 (VSCode Auto-push)

创建了 `.vscode/settings.json` 配置：
- `git.postCommitCommand: "push"` - 提交后自动推送
- `git.autofetch: true` - 自动获取远程更新
- `git.enableSmartCommit: true` - 启用智能提交
- `git.showPushSuccessNotification: true` - 显示推送成功通知

### 3. VSCode 任务 (VSCode Tasks)

创建了 `.vscode/tasks.json`，提供快捷任务：
- **Git: Sync current branch** - 同步当前分支
- **Git: Push and sync to gh-pages** - 推送并同步到 gh-pages
- **Git: Manual sync to gh-pages** - 手动同步到 gh-pages
- **Run Flask Server** - 运行 Flask 服务器

使用方法：按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (Mac)，选择 "Tasks: Run Task"

### 4. 文档 (Documentation)

创建了详细的中英文文档 `BRANCH_SYNC.md`，包含：
- 完整的工作流程说明
- VSCode 配置详解
- 手动同步方法
- 故障排除指南

### 5. 更新 README

在 README.md 中添加了分支同步功能的说明，并链接到详细文档。

## 使用方式 / How to Use

### 自动同步 (Automatic Sync)
1. 在 VSCode 中修改代码
2. 使用 Git 提交更改（Commit）
3. 代码会自动推送到远程仓库
4. GitHub Actions 会自动同步到 gh-pages 分支

### 手动同步 (Manual Sync)
如果需要手动同步，可以：
1. 使用 VSCode 任务：`Ctrl+Shift+P` -> `Tasks: Run Task` -> `Git: Manual sync to gh-pages`
2. 或使用命令行：
   ```bash
   git checkout gh-pages
   git merge master --no-edit
   git push origin gh-pages
   git checkout master
   ```

## 技术细节 / Technical Details

- **触发条件**: 推送到 `master` 或 `main` 分支
- **同步目标**: `gh-pages` 分支
- **合并策略**: 自动合并，无需编辑器
- **权限**: 使用 GitHub Actions 的内置 token

## 注意事项 / Notes

1. 首次使用时，确保 VSCode 已加载新的配置文件
2. 如果 `gh-pages` 分支不存在，同步会被跳过
3. 可以在 GitHub 的 Actions 标签页查看同步状态
4. 如果遇到问题，请参考 `BRANCH_SYNC.md` 中的故障排除部分
