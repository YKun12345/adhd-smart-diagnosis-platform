import json
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000/api/v1"

login = requests.post(f"{BASE}/auth/login", json={
    "identifier": "patient@example.com", "password": "BrainMap#2026Safe", "role": "patient",
}, timeout=30).json()
token = login["access_token"]
headers = {"Authorization": f"Bearer {token}"}

r = requests.post(f"{BASE}/model/predict_mock", params={
    "patient_id": 1, "file_name": "demo_fmri.1D",
}, headers=headers, timeout=30)
print("[predict_mock]", r.status_code)
for k, v in r.json().items():
    print(f"   {k}: {v}")
