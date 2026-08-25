import io
import json
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000/api/v1"

r = requests.post(f"{BASE}/auth/login", json={
    "identifier": "patient@example.com", "password": "BrainMap#2026Safe", "role": "patient",
})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

r = requests.get(f"{BASE}/patient/comprehensive_report", headers=headers)
print("[comprehensive_report]", r.status_code)
data = r.json()

print("顶层键及是否为空（五维聚合）:")
for key in ["patient_name", "patient_type", "latest_scale", "cognitive_profile",
            "tracking_summary", "latest_imaging_visualization", "latest_model_prediction"]:
    v = data.get(key)
    present = "NONEMPTY" if v not in (None, "", [], {}) else "EMPTY/None"
    print(f"  {key}: {present}")

print("\ncognitive_profile.radar_scores（认知五维）:", json.dumps(data.get("cognitive_profile", {}).get("radar_scores"), ensure_ascii=False))
print("latest_scale.risk_level:", data.get("latest_scale", {}).get("risk_level"))
