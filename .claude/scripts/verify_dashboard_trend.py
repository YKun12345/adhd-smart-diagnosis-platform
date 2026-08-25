import json
import requests

BASE = "http://127.0.0.1:8000/api/v1"

def login():
    r = requests.post(f"{BASE}/auth/login", json={
        "identifier": "patient@example.com",
        "password": "BrainMap#2026Safe",
        "role": "patient",
    })
    return {"Authorization": f"Bearer {r.json()['access_token']}"}

headers = login()

# 为 day 2-5 插入演示日志，构造逐日趋势数据
for day, focus, att in [(2, 40, 3), (3, 55, 4), (4, 35, 2), (5, 60, 4)]:
    r = requests.post(f"{BASE}/patient/submit_daily_log", json={
        "day_index": day,
        "mood_tag": "4",
        "focus_minutes": focus,
        "attention_rating": att,
        "hyperactivity_rating": 2,
        "impulsivity_rating": 3,
        "emotion_rating": 4,
        "task_completion_rating": 4,
    }, headers=headers)
    assert r.status_code == 201, r.text

# dashboard_status
r = requests.get(f"{BASE}/patient/dashboard_status", headers=headers)
d = r.json()
print("[dashboard_status]", r.status_code)
print("  current_day:", d["current_day"], "completed_days:", d["completed_days"], "total_days:", d["total_days"])
print("  logs 逐日可绘制的字段（day → focus, attention, hyperactivityr, impulsivity, emotion, task_completion）:")
for l in sorted(d["logs"], key=lambda x: x["day_index"]):
    print("   day", l["day_index"], "->", l["focus_minutes"], l["attention_rating"],
          l["hyperactivity_rating"], l["impulsivity_rating"], l["emotion_rating"], l["task_completion_rating"])

# comprehensive_report 的 tracking_summary
r2 = requests.get(f"{BASE}/patient/comprehensive_report", headers=headers)
print("[comprehensive_report]", r2.status_code)
if r2.status_code == 200:
    j = r2.json()
    ts = j.get("tracking_summary")
    print("  tracking_summary:", json.dumps(ts, ensure_ascii=False))
