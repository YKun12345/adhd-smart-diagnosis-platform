import json
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000/api/v1"

# 用已知 DAC 研究者账号（role=RESEARCHER）验证
login = requests.post(f"{BASE}/auth/login", json={
    "identifier": "researcher@example.com", "password": "BrainMap#2026Safe", "role": "researcher",
}, timeout=30)
print("[researcher login]", login.status_code)
if login.status_code != 200:
    print(login.text)
    sys.exit(1)
token = login.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

b = requests.post(f"{BASE}/doctor/bind_patient", headers=headers,
                 json={"patient_email": "patient@example.com"}, timeout=30)
print("[bind_patient]", b.status_code)
if b.status_code == 200:
    print("  bound patient_id:", b.json().get("patient_id"), "name:", b.json().get("patient_name"))

r = requests.get(f"{BASE}/doctor/patient/1/report", headers=headers, timeout=30)
print("[patient/1/report]", r.status_code)
d = r.json()
for k in ["patient_id", "patient_name", "latest_scale", "latest_model_prediction",
          "tracking_summary", "care_summary"]:
    v = d.get(k)
    if k == "latest_scale":
        v = (v or {}).get("risk_level") if v else None
    elif k == "latest_model_prediction":
        v = (v or {}).get("prediction_label") if v else None
    elif k == "tracking_summary":
        v = (v or {}).get("completed_count") if v else None
    print(f"  {k}: {v}")
