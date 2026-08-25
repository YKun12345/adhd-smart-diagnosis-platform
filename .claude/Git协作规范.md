# Git 协作规范

> 智绘脑图 SmartBrainMap 项目 Git 协作约定草案，由 B（后端）起草，A（前端）复审后生效。

## 一、仓库初始化

1. 在项目根目录执行 `git init`。
2. 首分支建议命名为 `main`（`git checkout -b main`）。
3. 根目录已准备 `.gitignore`（忽略 `.venv/`、`backend/__pycache__/`、`node_modules/`、`backend/app.db` 等）。

## 二、分支策略

| 分支 | 用途 |
|---|---|
| `main` | 稳定主线，随时间推进 |
| `feat/A-*` | A（前端）功能性开发分支，如 `feat/A-jspsych`、`feat/A-printPdf` |
| `feat/B-*` | B（后端）功能性开发分支，如 `feat/B-upload` |

约定：
- 禁止直接向 `main` 提交未测试代码；
- 每完成一个任务，在自己的 `feat/*` 分支上提交，必要时再合并/合并到 `main`。

## 三、commit 信息规范

- 格式：`feat|fix|docs|chore(范围): 简要描述`
- 示例：`feat(patient): 增加 14 天趋势日志字段`、`docs(readme): 补充启动说明`
- 描述使用中文，不超过 50 字。

## 四、分工约定

- A：前端 H5 + 小程序（`*.html`、`js/`、`miniprogram/`）
- B：后端 FastAPI（`backend/`）
- 双方均不修改对方模块的代码，除非已沟通确认。
- 需前置沟通的合并类事项（如表单题库归属、全链联调）另列待办，见 `.claude/未完成与A协作事项.md`。

## 五、常用流程

```bash
# 1. 起点在 main
git checkout main

# 2. 拉最新（已配置远程时）
git pull origin main

# 3. 新建自己的功能分支并切过去
git checkout -b feat/A-jspsych

# 4. 开发 → 提交
git add .
git commit -m "feat(A): 引入 jsPsych 认知范式"

# 5. 合并回 main
git checkout main
git merge feat/A-jspsych
```

## 六、禁忌

- 不提交 `node_modules/`、`.venv/`、`__pycache__/`、`*.pyc`；
- 不提交 `backend/app.db`（运行时动态 sqlite），也不提交含密钥的 `.env`（已存在 `.env.example`）。

## 七、提交到哪里、怎么查看

### 1. 提交到「本地 Git 仓库」

`git commit` 只写入**当前项目文件夹内的 `.git/` 目录**，不上传任何网络平台。
本地查看历史：

```bash
git log --oneline          # 简短列出所有提交
git status                # 看当前有没有改动、已暂存/未暂存
gitk / VS Code 里看 Source Control 面板
```

### 2. 让「其他人」看到：推送到远程仓库（GitHub / Gitee / GitLab）

本地提交只有你自己能看到；别人要看到，需把代码推送到一个远程托管平台：

```bash
# 1. 在 GitHub/Gitee 网页上新建一个「空仓库」，拿到它的地址，形如：
#    https://github.com/<你的名字>/SmartBrainMap.git

# 2. 关联远程（只需一次）
git remote add origin https://github.com/<你的名字>/SmartBrainMap.git

# 3. 推送
git push -u origin main
```

推送后，所有协作者都可以：

```bash
git clone https://github.com/<你的名字>/SmartBrainMap.git
```

然后在网页上（GitHub 的 Code 页）就能看到全部文件、提交历史、每个人的改动。

### 3. 没推远程之前，别人怎么看

- 直接拷贝整个 `源码\源码` 文件夹给对方即可（`.venv`、`app.db` 可删掉，对方按「启动说明.md」重新 `pip install`）。
- 或者压缩时排除 `.venv\`、`node_modules\`、`.git\`，只给源码 + `requirements.txt`。
