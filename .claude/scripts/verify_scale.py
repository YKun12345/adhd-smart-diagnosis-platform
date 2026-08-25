import json
import sys

import requests

BASE = "http://127.0.0.1:8000/api/v1"


def main() -> None:
    login = requests.post(
        f"{BASE}/auth/login",
        json={
            "identifier": "patient@example.com",
            "password": "BrainMap#2026Safe",
            "role": "patient",
        },
        timeout=30,
    )
    print("[login]", login.status_code)
    if login.status_code != 200:
        print(login.text)
        sys.exit(1)

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # ASRS：中度偏高的一组作答（多数题 2~3 分，个别 0/4）
    asrs_answers = [
        3, 2, 3, 2, 3, 2, 3, 2, 3,
        2, 3, 2, 3, 0, 4, 2, 3, 2,
    ]
    r = requests.post(
        f"{BASE}/patient/submit_scale",
        json={
            "scale_type": "ASRS",
            "answers": asrs_answers,
            "respondent_type": "self",
        },
        headers=headers,
        timeout=30,
    )
    print("[submit_scale ASRS]", r.status_code)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
