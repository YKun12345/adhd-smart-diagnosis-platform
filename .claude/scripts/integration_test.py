import json
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000/api/v1"

PASSED = []
FAILED = []


def check(name, cond, detail=""):
    if cond:
        PASSED.append(name)
        print(f"  [PASS] {name} {detail}")
    else:
        FAILED.append(name)
        print(f"  [FAIL] {name} {detail}")


def login(identifier, password, role):
    r = requests.post(f"{BASE}/auth/login", json={
        "identifier": identifier, "password": password, "role": role,
    }, timeout=30)
    return r


def main():
    # 1. 登录（患者）
    r = login("adult@demo.com", "Demo#2026", "patient")
    check("登录(患者)", r.status_code == 200, f"status={r.status_code}")
    if r.status_code != 200:
        print(r.text)
        sys.exit(1)
    pat_token = r.json()["access_token"]
    pat_h = {"Authorization": f"Bearer {pat_token}"}
    pat_user = r.json()["user"]
    pat_id = pat_user["patient_profile"]["id"]
    print(f"  患者: {pat_user['full_name']} user_id={pat_user['id']} patient_id={pat_id}")

    # 2. 量表
    asrs = [3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 0, 4, 2, 3, 2]
    r = requests.post(f"{BASE}/patient/submit_scale", headers=pat_h, json={
        "scale_type": "ASRS", "answers": asrs, "respondent_type": "self",
    }, timeout=30)
    ok = r.status_code in (200, 201)
    check("量表算分", ok, f"status={r.status_code} risk={r.json().get('risk_level') if ok else r.text}")

    # 3. 认知测试
    r = requests.post(f"{BASE}/patient/submit_cognitive_test", headers=pat_h, json={
        "test_type": "stroop", "result_json": {"total_trials": 48, "correct": 40, "accuracy": 0.833},
    }, timeout=30)
    ok = r.status_code in (200, 201)
    check("认知测试", ok, f"status={r.status_code}")

    # 4. 每日日志
    r = requests.post(f"{BASE}/patient/submit_daily_log", headers=pat_h, json={
        "day_index": 5, "mood_tag": "good", "focus_minutes": 55,
        "attention_rating": 4, "impulsivity_rating": 2,
        "note": "integration test",
    }, timeout=30)
    ok = r.status_code in (200, 201)
    detail = r.json().get("mood_tag") if ok else r.text
    check("每日日志", ok, f"status={r.status_code} {detail}")

    # 5. 看板状态（趋势）
    r = requests.get(f"{BASE}/patient/dashboard_status", headers=pat_h, timeout=30)
    ok = r.status_code == 200 and isinstance(r.json().get("logs"), list)
    check("看板状态(趋势)", ok, f"status={r.status_code} logs={len(r.json().get('logs', [])) if ok else '-'}")

    # 6. 综合报告（聚合五维）
    r = requests.get(f"{BASE}/patient/comprehensive_report", headers=pat_h, timeout=30)
    ok = r.status_code == 200
    check("综合报告", ok, f"status={r.status_code}")
    if ok:
        d = r.json()
        for dim in ["patient_name", "latest_scale", "cognitive_profile", "tracking_summary"]:
            present = dim in d
            check(f"  报告含{ dim }", present, "")

    # 7. 医生端
    r = login("doctor@demo.com", "Demo#2026", "researcher")
    check("登录(研究者)", r.status_code == 200, f"status={r.status_code}")
    dr_h = {"Authorization": f"Bearer {r.json()['access_token']}"}

    b = requests.post(f"{BASE}/doctor/bind_patient", headers=dr_h,
                     json={"patient_email": "adult@demo.com"}, timeout=30)
    check("医生绑定患者", b.status_code in (200, 409), f"status={b.status_code}")

    r = requests.get(f"{BASE}/doctor/my_patients", headers=dr_h, timeout=30)
    ok = r.status_code == 200
    check("我的患者列表", ok, f"status={r.status_code}")

    r = requests.get(f"{BASE}/doctor/patient/{pat_id}/report", headers=dr_h, timeout=30)
    ok = r.status_code == 200
    check("医生端患者报告", ok, f"status={r.status_code}")

    print("\n" + "=" * 50)
    print(f"全链路联调结果：{len(PASSED)} 通过 / {len(FAILED)} 失败")
    if FAILED:
        print("失败项:", FAILED)
        sys.exit(1)
    print("✅ 全链路联调通过")


if __name__ == "__main__":
    main()
