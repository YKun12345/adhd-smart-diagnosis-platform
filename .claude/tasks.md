# B 工程师任务规划 —— ADHD 智慧辅助诊断平台（后端改造）

> 任务性质：**后端已存在约 80%**，本阶段是「复用 → 小步改造 → 新增缺口 → 联调」而非从零搭建。
> 现状数据库：当前用 SQLite（`backend/app.db`，`DATABASE_URL=sqlite:///./backend/app.db`）；对应 MySQL 脚本 `backend/sql/init_mysql.sql`。
> 标记说明：`[ ]` 待办 / `[x]` 已完成；每项含状态（验证/修改/新建）与拆分的子任务 `[ ]`。

---

## 阶段一：基础设施（D1–D2）

### 任务1【验证】梳理 FastAPI 项目骨架 — `backend/app/` 结构已齐全
- [x] 1.1 确认目录结构：`main.py`、`api/router.py`、`api/routes/`、`models/`、`schemas/`、`core/`、`db/`、`services/`（上一会话已核）
- [x] 1.2 确认启动命令：`uvicorn backend.app.main:app --reload`（README 已载明）
- [x] 1.3 实际启动后端一次，确认无 import 错误、能出 `/docs`（`python -m uvicorn backend.app.main:app` 成功，/docs=200，/health=ok；后端保持后台运行）

### 任务2【修改/新建】建库建表 — `Base.metadata.create_all` 自动建表
- [x] 2.1 运行 `python -m backend.create_tables`，确认现有 7+ 张核心表可正常初始化（17 张全建，含预置演示账号）
- [x] 2.2 新建 `backend/app/models/upload.py`（uploads 表：uploads 模型 + patient/user 关系 + __all__ 注册）
- [x] 2.3 在 `models/__init__.py`、`init_db.py` 注册 uploads 模型，确认 create_all 能建（已建出 uploads 表）
- [x] 2.4 同步更新 `sql/init_mysql.sql` 补 uploads 表 DDL（MySQL 模式可重建）

### 任务3【修改】CORS 中间件 — 追加内网 IP 放行
- [x] 3.1 修改 `core/config.py` 的 `BACKEND_CORS_ORIGINS` 与 `main.py` 的正则，放行 `192.168.x.x` 等内网 IP（改 `main.py` 正则：localhost/127 + 私有网段 10/172.16-31/192.168；config.py 无需改）
- [x] 3.2 重启验证：内网段 Origin 放行（192.168.1.50:5500→200 带 ACAO），外部 evil.com→拒。后端改绑 0.0.0.0:8000 供局域网访问


## 阶段二：患者核心业务接口（D3–D7）

### 任务6【验证 + 可选项】量表算分 — `POST /api/v1/patient/submit_scale`（ASRS/SNAP-IV）
- [x] 6.1 确认算分逻辑已实现（ASRS 18 题 / SNAP-IV 26 题、风险分级、雷达图）——上一会话已核
- [x] 6.2 用 Swagger 提交一组答案，验证返回结构完整（执行阶段跑）

### 任务7【验证】认知测试存储 — `POST /api/v1/patient/submit_cognitive_test`
- [x] 7.1 确认已支持多 test_type（reaction/stroop/trail/flanker/nback/digit）——上一会话已核
- [x] 7.2 用 Swagger 提交一条认知结果验证入库

### 任务8【验证】每日日志 — `POST /api/v1/patient/submit_daily_log`
- [x] 8.1 确认字段覆盖 14 天全量 + 同天 upsert——上一会话已核
- [x] 8.2 提交 + 重复提交验证 upsert 行为

### 任务9【部分】14 天趋势
- [x] 9.1 确认 `dashboard_status` 与 `_extract_tracking_summary` 返回内容能否满足小程序趋势曲线 —— 已满足：dashboard_status.logs 逐日含 focus_minutes + 5 项 rating + day_index，足够绘逐日曲线；tracking_summary 提供聚合统计
- [x] 9.2 若需独立每日聚合接口 —— 现判断：无需新增，9.1 已覆盖

### 阶段三 报告与 AI（D8–D11）
- [x] 任务10【验证】综合报告 `GET /api/v1/patient/comprehensive_report`：`.1` 确认聚合五维；`.2` Swagger 验证
- [x] 任务11【验证】AI 助手 `routes/ai.py`（chat / explain_report / generate_reminder）：`.1` 确认 Qwen+降级逻辑；`.2` 无 key 时验证返回模板文本

### 阶段四 医生端与文件处理（D12–D14）
- [x] 任务12【新建】`.1D 上传接口`：`.1` 设计确认（uploads 表/接口定义）；`.2` 建 `models/upload.py` + `routes/upload.py`；`.3` 注册路由；`.4` Swagger 上传 .1D 验证 —— 实际：接口已存在于 `model_inference.py`（`POST /model/predict_fmri`，已注册）；uploads 表已在任务2 建。依赖 torch/dhg（当前 MISSING），真实预测 503，由 mock 兜底
- [x] 任务13【新建】`模拟预测 mock 接口`：`.1` 设计确认（真上传假结果+写 model_predictions）；`.2` 实现独立 `predict_mock`；`.3` 注册；`.4` 验证返回确定性 ADHD 二分类。已实现于 `model_inference.py` 的 `POST /model/predict_mock`
- [x] 任务14【验证】医生端 API：`.1` 确认 `doctor.py` 接口已实现（bind_patient / my_patients / dashboard_stats / patient/{id}/imaging_visualization / patient/{id}/report 共 5 接口）；`.2` 绑定患者后用 `/patient/{id}/report` 验证成功

### 阶段五 部署与演示（D15–D18）
- [x] 任务15【新建】演示数据 seed：`.1` 设计确认（1 成人+1 儿童+全套样本）；`.2` 写 `backend/scripts/seed_demo_data.py`；`.3` 一键执行并验证
- [x] 任务16【新建】内网访问方案文档：`.1` 编写热点/ngrok 步骤；`.2` 说明小程序真机预览配置 —— 产出 `backend/docs/内网访问方案.md`
- [x] 任务17【验证/补】API 文档：`.1` 确认 `/docs` 可用；`.2` 补小程序接入说明 —— 产出 `miniprogram/README.md`
- [x] 任务18【新建】「后端技术实现」报告素材：`.1` 撰写 `backend/docs/后端技术实现.md`

### 协作与收尾
- [x] 任务19 协助 A 完成 Git 协作规范 —— 已 `git init`（分支 `main`）+ 首次提交 344 文件 + `.gitignore`；规范文档 `.claude/Git协作规范.md`（远程推送待建远端仓库）
- [x] 任务20 全链路联调（登录→量表→认知→追踪→报告 + 医生端）—— 产出 `.claude/scripts/integration_test.py`，14/14 通过
- [x] 任务21 修复联调与测试暴露的所有后端 bug —— 本轮联调未发现后端 bug（唯一 422 为测试脚本字段笔误，已修正脚本本身）