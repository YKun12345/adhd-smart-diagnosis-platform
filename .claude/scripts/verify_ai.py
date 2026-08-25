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

s = requests.get(f"{BASE}/ai/status", headers=headers).json()
print("[ai/status] configured =", s.get("configured"), "| message =", s.get("message"))

c = requests.post(f"{BASE}/ai/chat", headers=headers, json={
    "message": "我最近总是走神，很焦虑", "conversation": [], "context_scope": "general",
}).json()
print("[ai/chat] model =", c.get("model"), "| degraded =", c.get("degraded"))
print("  reply:", c.get("reply", "")[:60])

e = requests.post(f"{BASE}/ai/explain_report", headers=headers).json()
print("[ai/explain_report] model =", e.get("model"), "| degraded =", e.get("degraded"))
print("  headline:", e.get("headline"))

g = requests.post(f"{BASE}/ai/generate_reminder", headers=headers).json()
print("[ai/generate_reminder] model =", g.get("model"), "| degraded =", g.get("degraded"))
print("  title:", g.get("title"), "| action_label:", g.get("action_label"))
