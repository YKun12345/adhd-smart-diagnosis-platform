import os
import sqlite3
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.core.security import get_password_hash

DB = "backend/app.db"
NEW_PASSWORD = "BrainMap#2026Safe"

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (get_password_hash(NEW_PASSWORD), 2))
conn.commit()
print("reset rows:", cur.rowcount)
cur.close()
