# 未完成任务与 A 协作事项

> 说明：本文件由 B 工程师整理，供协作对接使用。
> 内容来源：`.claude/tasks.md` 中仍未关闭的内容，以及需要 A 端（前端）协作的事项。
> 更新日期：2026-08-25。

---

## 一、未完全完成的内容

截至 2026-08-25，`tasks.md` 中 21 项任务已完成 20 项（`[x]`），**仅剩 1 项未完成**：

### 任务19 —— 协助 A 完成 Git 协作规范

- **状态**：⏸ 待 A 就位，当前无法由 B 独立推进。
- **性质**：跨职能协作任务，需要 A（前端工程师）共同参与。
- **说明**：等 A 就位后，由双方协商 git 分支策略、commit 规范等协作约定。

> 除任务19 外，其余 20 项后端任务（阶段一~五 + 全链路联调 + 修复检查）均已完成。后端功能可用、接口齐全、文档齐备。

---

## 二、需要 A 协作的内容

### （一）Git 协作规范（任务19，直接依赖 A）

见上文，需 A 共同制定。

### （二）前端/小程序对接后端（后端已就绪，等 A 接入）

后端接口已全部可用并用脚本验证通过，等待 A 端实际接入：

1. **小程序接入**：`miniprogram/` 目前是脚手架（仅 login、home 两页空壳）。A 端需：
   - 写入 base URL 配置（建议新增 `miniprogram/utils/config.js`，指向 `http://<电脑IP>:8000/api/v1`）；
   - 实现登录页（调 `POST /auth/login`，字段名 `identifier`，返回 `access_token`）；
   - 接入核心业务接口（量表/认知/日志/看板/报告/AI）。
   - 详细说明见 B 端已写好的 `miniprogram/README.md`。

2. **H5 前端遗留待办**（见根 `README.md` 的 Team Todo-List，属 A 端）：
   - `patient_test.html` 引入 `jsPsych` 库，挂载真实 N-back / Go-NoGo 认知刺激范式；
   - 用 `html2canvas` 编写 `printPdf()`，一键导出患者可视化报告单；
   - 与 Python 端打通云端审计 TPA 探针长连接（EventSource/SSE）面板推流。

### （三）已由 B 判断「无需后端改动」、但需 A 端确认的遗留决策

| 编号 | 事项 | B 端判断 | 待 A 确认 |
|---|---|---|---|
| 任务9 | 14 天趋势是否需要独立 `GET /patient/trend` 接口 | 无需：`dashboard_status.logs` 已逐日含 focus_minutes + 5 项 rating + day_index，足够绘曲线 | 若 A 端曲线渲染另有数据需求，再议 |
| 任务6 | 量表题库是否由后端下发 | 未新增下发接口，当前题库由前端自带 | 若 A 端希望后端统一下发题库，需 B 端新增 |

---

## 三、补充说明（对接时可参考）

- 后端启动：`.venv\Scripts\python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000`
- 接口文档：`http://127.0.0.1:8000/docs`（Swagger）/ `/openapi.json`
- 演示账号：

  | 角色 | 账号 | 密码 |
  |---|---|---|
  | 患者（成人） | `adult@demo.com` | `Demo#2026` |
  | 患者（儿童） | `child@demo.com` | `Demo#2026` |
  | 研究者 | `doctor@demo.com` | `Demo#2026` |
  | 通用演示患者 | `patient@example.com` | `BrainMap#2026Safe` |
