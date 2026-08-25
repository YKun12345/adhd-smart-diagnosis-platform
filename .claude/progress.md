# 项目进度记录（progress.md）

> 后端改造项目（ADHD 智慧辅助诊断平台 · B 工程师）
> 工作方式：完成一项即追加记录；`tasks.md` 中 `[ ]`→`[x]` 同步。

---

## 2026-08-24 18:43 —— 会话启动 / 前期准备

- **已确认** `.claude/tasks.md` 存在（上一会话已创建，含 21 项任务 + 真实状态标注）。
- **已创建** 本文件 `progress.md`。
- **已细化** `tasks.md`：将若干大任务拆分为可执行子任务（见 tasks.md）。
- **当前决策**：后端已存在约 80%，采用「复用 → 小步改造 → 新增缺口 → 联调」策略。当前数据库为 SQLite（`backend/app.db`）。
- **下一步**：等待指令后开始执行 任务1。

---

## 2026-08-24 —— 完成 任务1.3：实泛起后端

- - [2026-08-24] 完成 [任务1.3]：首次启动后端成功，确认无 import 错误、`/docs`=200、`/api/v1/health`=ok。关键产出：确认启动命令为 `.venv/Scripts/python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`（`uvicorn.exe` 短生命周期秒退 exit1，改为 `python -m` 正常）。
- 后端已以后台进程常驻，供后续任务调用。
- 已完成：1.3（阶段一内第 1 个实步子任务）。

### 当前进度快照
- 已完成：实步子任务 1.3（阶段一内首个）；1.1/1.2 为规划期确认。
- 待决策事项：任务6 是否增补后端下发题库、任务9 是否需要独立趋势接口（均留待联调确认）。

---

## 2026-08-24 —— 完成 任务2.1：建库建表验证
- [2026-08-24] 完成 [任务2.1]：`python -m backend.create_tables` 成功，SQLite 下 `create_all` 建出 17 张表（users/patients/scale_results/cognitive_tests/tracking_logs 等核心表齐备）。关键产出：库内已有 3 个预置演示账号（admin DAC + patient + researcher）。
- 已完成：1.3、2.1。

### 当前进度快照
- 已完成：1.3、2.1、2.2、2.3、2.4（阶段一剩余任务3）。
- 待决策事项：任务6 是否增补后端下发题库、任务9 是否需要独立趋势接口（均留待联调确认）。

---

## 2026-08-24 —— 完成 任务2.2/2.3/2.4：新建 uploads 表模型并注册
- [2026-08-24] 完成 [任务2.2]：新建 `backend/app/models/upload.py`（Upload 模型，uploads 表：id/patient_id/uploader_id/file_name/source_type/file_size/file_hash/status/stored_path/note/created_at）。
- [2026-08-24] 完成 [任务2.3]：注册于 `models/__init__.py`（导入+__all__）与 `db/init_db.py`；补 patient.py（uploads 关系）、user.py（uploads + TYPE_CHECKING）。重跑 `create_tables` 成功建出 uploads 表（11 列）。后端重启 `/health`=200。
- [2026-08-24] 完成 [任务2.4]：`sql/init_mysql.sql` 追加 uploads 表 DDL（含外键/索引/utf8mb4）。
- 已完成：1.3、2.1、2.2、2.3、2.4。

### 当前进度快照
- 已完成：1.3、2.1、2.2、2.3、2.4、3.1、3.2。

### 当前进度快照
- 阶段一已完成：任务1、2、3（全部子任务 `[x]`）。✅ 阶段一收尾。
- 下一实步子任务：阶段二 6.2（量表算分 Swagger 验证）。

---

## 2026-08-24 —— 完成 任务3.1/3.2：CORS 内网 IP 放行
- [2026-08-24] 完成 [任务3.1]：修改 `app/main.py` CORS 正则，放行 localhost/127.0.0.1 及私有网段（10.x / 172.16-31.x / 192.168.x.x）+ 任意端口。`core/config.py` 无需改动（由正则承载）。
- [2026-08-24] 完成 [任务3.2]：重启后端绑 `0.0.0.0:8000`（供局域网访问）。预检验证：Origin `http://192.168.1.50:5500`→200 带 `access-control-allow-origin`；`https://evil.com`→400 拒。内网 H5/小程序真机均可访问。关键产出：`main.py` 正则修改。
- 阶段一全部完成（任务1/2/3）。

### 当前进度快照
- 阶段一 ✅ 完成；准备进入阶段二（患者核心业务接口，验证类为主）。

---

## 2026-08-25 —— 完成 任务6.2：量表算分 Swagger 验证
- [2026-08-25] 完成 [任务6.2]：通过 `POST /api/v1/patient/submit_scale` 提交 18 题 ASRS 答案，返回 201 + 完整结构（id/scale_type/respondent_type/total_score/risk_level/radar_scores 五维/sub_scores/summary/recommendations/created_at）。风险分级为 high。关键产出：`.claude/scripts/verify_scale.py`。
- 过程中发现 demo 密码与 README 不一致，按优先级 2 用 `.claude/scripts/reset_patient_password.py` 重置为 `BrainMap#2026Safe` 再验证（见 `.claude/scripts/`）。

### 当前进度快照
- 阶段二 实步子任务 6.2 ✅。下一项：7.2（认知测试入库 Swagger 验证）。

---

## 2026-08-25 —— 完成 任务7.2：认知测试入库验证
- [2026-08-25] 完成 [任务7.2]：通过 `POST /api/v1/patient/submit_cognitive_test` 提交 test_type=stroop，返回 201 + `{id,test_type,result_json,created_at}`；DB `cognitive_tests` 计数 0→1 确认入库。关键产出：`.claude/scripts/verify_cognitive.py`。

### 当前进度快照
- 阶段二 实步子任务 6.2、7.2 ✅。下一项：8.1/8.2（每日日志 submit_daily_log）。

---

## 2026-08-25 —— 完成 任务8.2：每日日志 upsert 验证
- [2026-08-25] 完成 [任务8.2]：`POST /api/v1/patient/submit_daily_log` 首次插入 1 条记录（id=1，mood=good/focus=50）；重复提交（mood=bad/focus=10/note=upserted）后 DB 仍为 1 条、字段已更新，确认 upsert 正确。关键产出：`.claude/scripts/verify_tracking.py`。

### 当前进度快照
- 阶段二实步子任务 6.2、7.2、8.2 ✅。下一项：9.1（14 天趋势：核对 dashboard_status 与 _extract_tracking_summary 内容）。

---

## 2026-08-25 —— 完成 任务9.1：14 天趋势接口核对
- [2026-08-25] 完成 [任务9.1]：核对 `GET /api/v1/patient/dashboard_status` 与 comprehensive_report 的 `_extract_tracking_summary`。结论：**现有接口已满足小程序趋势曲线** —— dashboard_status.logs 逐日返回 focus_minutes + 5 项 rating + day_index（可直接绘逐日折线）；tracking_summary 提供聚合统计（average_focus_minutes/average_mood/completed_days/completion_status）。关键产出：`.claude/scripts/verify_dashboard_trend.py`。
- 数据验证：插入 day 1-5 后，dashboard_status 返回 logs 完整逐日序列；tracking_summary 返回平均专注 40.0、平均情绪 4.0、完成度 building_baseline。
- 任务9.2（新增独立 trend 接口）现判断：**无需**（9.1 已覆盖），待联调最终确认。

### 当前进度快照
- 阶段二实步子任务 6.2、7.2、8.2、9.1 ✅。下一项：任务10（综合报告 comprehensive_report：10.1 确认聚合五维；10.2 Swagger 验证）。

---

## 2026-08-25 —— 完成 任务10：综合报告验证
- [2026-08-25] 完成 [任务10]：`GET /api/v1/patient/comprehensive_report` 返回 200。聚合五维确认：patient_name/patient_type ✅、latest_scale（ASRS risk=high）✅、cognitive_profile（radar_scores 四维）✅、tracking_summary ✅、latest_imaging_visualization + latest_model_prediction（当前为空，待任务12-14补齐后回填）。关键产出：`.claude/scripts/verify_comprehensive_report.py`。

---

## 2026-08-25 —— 完成 任务11：AI 助手验证
- [2026-08-25] 完成 [任务11]：`routes/ai.py` 三个接口 chat/explain_report/generate_reminder 均可用。确认 Qwen 接入后以 `_provider_or_fallback_*` 模式启用 provider；无 key 情况下降级为 `heuristic_*` 模板，degraded=True，model=fallback-template。
- 实测无 key 环境：三接口均返回模板文本，且内容基于患者快照（如 chat reply 提到"成人量表提示核心注意控制与执行启动困难较明显"）。关键产出：`.claude/scripts/verify_ai.py`。

### 当前进度快照
- 阶段二 + 任务10 + 任务11 ✅。下一项：任务12（.1D 上传接口，新建 uploads 模型+routes）。

---

## 2026-08-25 —— 完成 任务12：.1D 上传接口确认
- [2026-08-25] 完成 [任务12]：确认上传+真实预测接口已存在（`POST /model/predict_fmri`，位于 `model_inference.py`，已注册 router），而非 `routes/upload.py`。uploads 表已在任务2 建。该接口依赖 torch/dhg，当前环境 MISSING → 真实调用 503，由任务13 mock 兜底。

## 2026-08-25 —— 完成 任务13：mock 预测接口实现
- [2026-08-25] 完成 [任务13]：在 `model_inference.py` 新增 `POST /model/predict_mock`，基于 (patient_id, file_name) 的 sha256 生成确定性 ADHD 概率（0.60~0.90），写 model_predictions 表（source_type=mock）。实测返回 200，label=ADHD，prob=0.664。关键产出：`model_inference.py` 改动 + `.claude/scripts/verify_mock.py`。
- 决策：采用确定性而非随机，保证演示结果稳定可复现。

### 当前进度快照
- 阶段二 + 任务10/11/12/13 ✅。下一项：任务14（医生端 API 验证）。

---

## 2026-08-25 —— 完成 任务14：医生端 API 验证
- [2026-08-25] 完成 [任务14]：`doctor.py` 实际含 5 接口（bind_patient/my_patients/dashboard_stats/patient/{id}/imaging_visualization/patient/{id}/report）。
- [2026-08-25] 完成 [任务14.2]：researcher@example.com（id=3，已绑定 patient id=1）登录后 `GET /doctor/patient/1/report` 返回 200 + 完整报告（latest_scale=high、latest_model_prediction=ADHD、tracking_summary completed 5/14、care_summary 3 条）。关键产出：`.claude/scripts/verify_doctor.py`。
- 期间发现 admin（DAC，id=1）无法绑定已归属 researcher@example.com 的患者（409），改用 researcher@example.com 登录验证成功。

---

## 2026-08-25 —— 完成 任务15：演示数据 seed
- [2026-08-25] 完成 [任务15]：新建 `backend/scripts/seed_demo_data.py`，一键生成独立演示账号 + 全套样本。设计确认：成人 ASRS 高风险（ADHD）+ 儿童 SNAP-IV 低风险（Control）+ 研究者绑定（用户确认全新独立账号）。
- 账号：adult@demo.com（成人高风险）/ child@demo.com（儿童 Control）/ doctor@demo.com（研究者），密码 Demo#2026。
- 数据验证：成人=ASRS high(59)、儿童=SNAP_IV low(10)；各含认知 6 类、追踪 14 天、影像 2 条(nifti+gifti)、模型预测(mock ADHD/Control)。关键产出：`backend/scripts/seed_demo_data.py` + `backend/scripts/__init__.py`。

### 当前进度快照
- 阶段二 + 任务10/11/12/13/14/15 ✅。下一项：任务16（内网访问方案文档）。

---

## 2026-08-25 —— 完成 任务16：内网访问方案文档
- [2026-08-25] 完成 [任务16]：新建 `backend/docs/内网访问方案.md`，覆盖三部分：① 先决条件（后端须绑 `0.0.0.0`，CORS 已内置放行私有网段）；② 方案 A（手机热点/局域网，免公网，推荐真机联调）+ 方案 B（ngrok/cpolar/natapp 公网穿透）；③ 小程序真机预览（开发期勾选「不校验合法域名」+ 正式发布需 HTTPS 合法域名 + request 白名单）。含方案对比表与选择建议。
- ✅ 自检通过（文档与当前实际实现一致：后端确绑 0.0.0.0、CORS 正则确含私有网段、miniprogram 确为脚手架仅两页、appid 确为 wx5fc79e35c64730d9）。
- 期间发现并修正两个错标：tasks.md 中任务9.2 与任务11 仍为 `[ ]` 但实际已完结，补标为 `[x]`。

### 当前进度快照
- 阶段二 + 任务10/11/12/13/14/15/16 ✅。下一项：任务17（API 文档：`/docs` 确认 + 补小程序接入说明）。

---

## 2026-08-25 —— 完成 任务17：API 文档
- [2026-08-25] 完成 [任务17.1]：启动后端后验证 `/docs` 与 `/openapi.json` 均返回 200。
- [2026-08-25] 完成 [任务17.2]：新建 `miniprogram/README.md`（小程序接入说明），含：统一 base URL 配置、认证流程（登录用 `identifier` 字段 + Bearer token）、患者核心业务接口表、`wx.request` 请求示例、完整接口清单归组。
- ✅ 自检通过：登录/鉴权/业务接口均实测返回 200 或正确 JSON；接口清单由 `/openapi.json` 直接导出，与代码一致。

### 当前进度快照
- 阶段二 + 任务10/11/12/13/14/15/16/17 ✅。下一项：任务18（「后端技术实现」报告素材 → `backend/docs/后端技术实现.md`）。

---

## 2026-08-25 —— 完成 任务18：后端技术实现报告素材
- [2026-08-25] 完成 [任务18]：新建 `backend/docs/后端技术实现.md`，覆盖八节：技术栈 / 目录结构 / 数据库设计（12 表 + 双模式）/ 认证鉴权（JWT）/ 核心业务（算分、认知、追踪、综合报告、AI、影像预测）/ 安全体系 / CORS 与部署 / 启动方式。
- ✅ 自检通过：内容依据实际代码与 `/openapi.json` 导出结果撰写，路由/表名/字段与实际一致。

### 当前进度快照
- 阶段二~五 全部单体任务（1~18）✅。下一项：任务19（协助 A 完成 Git 协作规范）。

---

## 2026-08-25 —— 完成 任务20/21：全链路联调 + 修复检查
- [2026-08-25] 完成 [任务20]：编写 `.claude/scripts/integration_test.py` 端到端联调脚本，串联 登录→量表→认知→追踪→看板→综合报告→医生端（绑定/列表/患者报告）完整流程。实测 14/14 全部通过。
- [2026-08-25] 完成 [任务21]：本轮联调未发现后端 bug。唯一失败是脚本自身 `submit_daily_log` 字段笔误（误用 `mood`/`ratings`，实际 schema 为 `day_index`（必填）+ `mood_tag` + `attention_rating` 等），已修正脚本本身，后端代码无需改动。
- ✅ 自检通过：全链路 14/14，覆盖患者与医生两大角色。

### 当前进度快照
- 任务 1~18、20、21 全部 ✅。仅剩 任务19（依赖 A，⏸ 待 A 就位）。

---

## 2026-08-25 —— 任务19 草案产出（Git 协作规范）
- [2026-08-25] 产出 [任务19 草案]：项目尚未 `git init`，A 也未到场。先行起草 `.claude/Git协作规范.md`（仓库初始化 / 分支策略 / commit 规范 / 分工约定 / 常用流程 / 禁忌）并新增根目录 `.gitignore`（忽略 .venv、__pycache__、node_modules、app.db、.env）。
- ⏳ 真正完成需：A 复审通过后，双方执行 `git init` + 首次提交。当前 A 未到场，暂标「待 A 复审」。

### 当前进度快照
- 任务 1~18、20、21 ✅；任务19 草案已就绪，等待 A 复审后执行 git init。