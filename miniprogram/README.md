# 小程序接入说明（API 客户端指南）

本说明面向「智绘脑图」小程序（`miniprogram/`）开发者。小程序不是独立后端，而是 FastAPI 后端（`backend/`）的 HTTP 客户端，复用前端 HTML/JS 完全相同的 REST API。

## 一、前置

1. 后端已启动（见 `.claude/start.bat` 或 `backend/docs`）。
2. 先在微信开发者工具中勾选「不校验合法域名」（开发期），或配置好 HTTPS 合法域名（正式，见 `backend/docs/内网访问方案.md`）。
3. base URL 指向后端地址，如 `http://127.0.0.1:8000`，或 `https://<你的穿透域名>`。

## 二、统一 base URL

在 `miniprogram/utils/` 下新增 `config.js` 集中管理，避免散落各处：

```js
// miniprogram/utils/config.js
module.exports = {
  BASE_URL: 'http://127.0.0.1:8000/api/v1',
};
```

各页面 `require('../../utils/config.js')` 读取即可。

## 三、认证流程

登录接口返回 `access_token`（JWT）与 `user`。后续所有请求在请求头携带：

```
Authorization: Bearer <access_token>
```

### 登录

```
POST /api/v1/auth/login
```

请求体：

```
{"identifier": "adult@demo.com", "password": "Demo#2026", "role": "patient"}
```

> 注意字段名是 `identifier`（邮箱或用户名），不是 `email`。

响应关键字段：`access_token`、`token_type`、`user.patient_profile.id`（`patient_id`，后续接口用到）。

```js
const res = await wx.request({
  url: `${BASE_URL}/auth/login`,
  method: 'POST',
  data: { identifier, password, role: 'patient' },
  header: { 'Content-Type': 'application/json' },
});
const { access_token, user } = res.data;
wx.setStorageSync('token', access_token);
wx.setStorageSync('patient_id', user.patient_profile.id);
```

## 四、核心业务接口（患者）

| 动作 | Method + Path | 说明 |
|---|---|---|
| 提交量表结果 | `POST /patient/submit_scale` | ASRS(成人18题) / SNAP_IV(儿童26题)，返回 total_score / risk_level / radar_scores 五项 |
| 提交认知测试 | `POST /patient/submit_cognitive_test` | test_type 支持反应时/stroop/trail/flanker/nback/digit 等，结果统一放 result_json |
| 提交每日日志 | `POST /patient/submit_daily_log` | 同天重复提交为 upsert（只保留一条并更新字段） |
| 获取首页看板 | `GET /patient/dashboard_status` | 含 logs（逐日 focus_minutes+5 项 rating+day_index）供绘制 14 天趋势曲线 |
| 获取综合报告 | `GET /patient/comprehensive_report` | 聚合五维：资料/量表/认知/追踪/影像+预测 |
| AI 对话 | `POST /ai/chat` | 无 QWEN_API_KEY 时降级为模板回复（degraded=true） |

所有 `patient` / `ai` 接口都需在请求头带 `Authorization: Bearer <token>`。

## 五、请求示例（wx.request）

```js
wx.request({
  url: `${BASE_URL}/patient/submit_scale`,
  method: 'POST',
  header: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + wx.getStorageSync('token'),
  },
  data: {
    scale_type: 'ASRS',
    respondent_type: 'adult',
    answers: [/* 18 题，每题 0-4 分 */],
  },
  success: (res) => {
    console.log(res.data); // {id, total_score, risk_level, radar_scores, ...}
  },
});
```

## 六、完整接口清单

所有接口在 `backend/docs` 与 Swagger UI 均可查；`/openapi.json` 是机器可读的权威清单。本小程序涉及的集中在：

```
/api/v1/auth/*            认证
/api/v1/patient/*         患者核心业务
/api/v1/ai/*              AI 助手
/api/v1/doctor/*          医生端（非本小程序页面）
/api/v1/care/*           关怀（消息/任务）
/api/v1/security/*        DAC 审计（非本小程序页面）
/api/v1/ai-enhanced/*    增强分析（后台给医生/DAC用）
/api/v1/model/*          影像预测（患者小程序可能需调用 predict_mock）
```

通过运行 `curl http://127.0.0.1:8000/openapi.json` 可随时获取最新路径。
