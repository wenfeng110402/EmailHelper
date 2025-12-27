# 分支同步说明 / Branch Synchronization Guide

## 中文说明

### 概述
本项目已配置自动分支同步功能。当你在 VSCode 中提交代码到 `master` 或 `main` 分支时，GitHub Actions 会自动将更改同步到 `gh-pages` 分支。

### 工作流程

1. **在 VSCode 中提交代码**
   - 修改代码后，使用 VSCode 的 Git 功能提交更改
   - 提交会自动推送到远程仓库（已配置 `git.postCommitCommand`）

2. **自动同步**
   - 当代码推送到 `master` 或 `main` 分支时，GitHub Actions 会自动触发
   - 工作流会将更改合并到 `gh-pages` 分支
   - 整个过程完全自动化，无需手动操作

3. **查看同步状态**
   - 在 GitHub 仓库的 "Actions" 标签页查看工作流运行状态
   - 每次推送后都会显示同步进度和结果

### VSCode 配置

项目包含以下 VSCode 配置：

- **自动获取更新**: Git 会自动从远程仓库获取更新
- **自动推送**: 提交后自动推送到远程仓库
- **智能提交**: 启用智能提交功能

### 可用的 VSCode 任务

在 VSCode 中按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (Mac)，然后选择 "Tasks: Run Task"：

1. **Git: Sync current branch** - 同步当前分支
2. **Git: Push and sync to gh-pages** - 推送并触发自动同步
3. **Git: Manual sync to gh-pages** - 手动同步到 gh-pages
4. **Run Flask Server** - 运行 Flask 服务器

### 手动同步方法

如果需要手动同步分支：

```bash
# 方法 1: 使用 VSCode 任务
# Ctrl+Shift+P -> Tasks: Run Task -> Git: Manual sync to gh-pages

# 方法 2: 使用命令行
git checkout gh-pages
git merge master --no-edit
git push origin gh-pages
git checkout master
```

### 注意事项

- 只有推送到 `master` 或 `main` 分支才会触发自动同步
- 如果 `gh-pages` 分支不存在，同步会跳过
- 可以在 GitHub Actions 中手动触发同步（workflow_dispatch）

---

## English Guide

### Overview
This project is configured with automatic branch synchronization. When you commit code to the `master` or `main` branch in VSCode, GitHub Actions will automatically sync the changes to the `gh-pages` branch.

### Workflow

1. **Commit Code in VSCode**
   - After modifying code, use VSCode's Git feature to commit changes
   - Commits are automatically pushed to the remote repository (configured via `git.postCommitCommand`)

2. **Automatic Synchronization**
   - When code is pushed to `master` or `main` branch, GitHub Actions triggers automatically
   - The workflow merges changes into the `gh-pages` branch
   - The entire process is fully automated, no manual intervention needed

3. **Check Sync Status**
   - View workflow run status in the "Actions" tab of your GitHub repository
   - Each push displays sync progress and results

### VSCode Configuration

The project includes the following VSCode settings:

- **Auto-fetch**: Git automatically fetches updates from remote
- **Auto-push**: Automatically pushes to remote after commit
- **Smart Commit**: Enables smart commit functionality

### Available VSCode Tasks

Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac) in VSCode, then select "Tasks: Run Task":

1. **Git: Sync current branch** - Sync current branch
2. **Git: Push and sync to gh-pages** - Push and trigger auto-sync
3. **Git: Manual sync to gh-pages** - Manually sync to gh-pages
4. **Run Flask Server** - Run the Flask server

### Manual Sync Methods

If manual synchronization is needed:

```bash
# Method 1: Use VSCode Task
# Ctrl+Shift+P -> Tasks: Run Task -> Git: Manual sync to gh-pages

# Method 2: Use command line
git checkout gh-pages
git merge master --no-edit
git push origin gh-pages
git checkout master
```

### Important Notes

- Auto-sync only triggers when pushing to `master` or `main` branches
- If `gh-pages` branch doesn't exist, sync will be skipped
- You can manually trigger sync in GitHub Actions (workflow_dispatch)

### Troubleshooting

**Issue**: Code isn't syncing to gh-pages
- Check the Actions tab in GitHub for error messages
- Ensure you pushed to the correct branch (`master` or `main`)
- Verify that `gh-pages` branch exists

**Issue**: VSCode isn't auto-pushing
- Check that VSCode settings are loaded correctly
- Manually push once: `git push origin <branch-name>`
- Restart VSCode to reload settings
