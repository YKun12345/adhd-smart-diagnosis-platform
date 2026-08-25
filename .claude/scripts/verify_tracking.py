import json
import sqlite3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import requests

BASE = "http://127.0.0.1:8000/api/v1"

def login():
    r = requests.post(f"{BASE}/auth/login", json={
        "identifier": "patient@example.com",
        "password": "BrainMap#2026Safe",
        "role": "patient",
    })
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}

def count_logs(patient_id, day_index):
    conn = sqlite3.connect("backend/app.db")
    n = conn.execute("SELECT COUNT(*) FROM tracking_logs WHERE patient_id=? AND day_index=?", (patient_id, day_index)).fetchone()[0]
    conn.close()
    return n

def get_log(patient_id, day_index):
    conn = sqlite3.connect("backend/app.db")
    row = conn.execute("SELECT mood_tag, focus_minutes, note FROM tracking_logs WHERE patient_id=? AND day_index=?", (patient_id, day_index)).fetchone()
    conn.close()
    return row

headers = login()

payload1 = {
    "day_index": 1,
    "mood_tag": "good",
    "focus_minutes": 50,
    "note": "first submit",
    "test_score": 0.8,
    "activities": "reading",
    "is_medication": True,
    "medication_dosage": "10mg",
    "attention_rating": 4,
    "hyperactivity_rating": 2,
    "impulsivity_rating": 3,
    "emotion_rating": 4,
    "task_completion_rating": 4,
    "sleep_quality": "good",
    "appetite_quality": "normal",
    "has_conflict": False,
    "was_criticized": False,
}

r1 = requests.post(f"{BASE}/patient/submit_daily_log", json=payload1, headers=headers)
print("[first submit]", r1.status_code, "id", r1.json().get("id"), "mood", r1.json().get("mood_tag"))
print("DB after first insert:", get_log(1, 1), "count:", count_logs(1, 1))

payload2 = dict(payload1, mood_tag="bad", focus_minutes=10, note="upserted")
r2 = requests.post(f"{BASE}/patient/submit_daily_log", json=payload2, headers=headers)
print("[second submit]", r2.status_code, "id", r2.json().get("id"), "mood", r2.json().get("mood_tag"))
print("DB after second submit:", get_log(1, 1), "count:", count_logs(1, 1))
