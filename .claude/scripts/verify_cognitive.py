import json
import sqlite3

import requests

BASE = "http://127.0.0.1:8000/api/v1"

login = requests.post(
    f"{BASE}/auth/login",
    json={"identifier": "patient@example.com", "password": "BrainMap#2026Safe", "role": "patient"},
    timeout=30,
).json()
token = login["access_token"]
headers = {"Authorization": f"Bearer {token}"}

payload = {
    "test_type": "stroop",
    "result_json": {
        "total_trials": 8,
        "correct": 6,
        "wrong": 2,
        "avg_reaction_ms": 821.6,
    },
}

before = sqlite3.connect("backend/app.db").execute("SELECT COUNT(*) FROM cognitive_tests").fetchone()[0]

r = requests.post(f"{BASE}/patient/submit_cognitive_test", json=payload, headers=headers, timeout=30)

after = sqlite3.connect("backend/app.db").execute("SELECT COUNT(*) FROM cognitive_tests").fetchone()[0]

print("[submit_cognitive_test]", r.status_code)
print(json.dumps(r.json(), ensure_ascii=False, indent=2))
print(f"DB cognitive_tests count: {before} -> {after}")
