import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FILE = BASE_DIR / "data" / "activity_log.json"


def ensure_log_file():

    if not LOG_FILE.exists():

        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(LOG_FILE, "w", encoding="utf-8") as file:

            json.dump([], file, indent=4)


def write_log(username: str, action: str, description: str):
    ensure_log_file()

    with open(LOG_FILE, "r", encoding="utf-8") as file:

        logs = json.load(file)

    logs.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "action": action,
            "description": description,
        }
    )

    with open(LOG_FILE, "w", encoding="utf-8") as file:

        json.dump(logs, file, indent=4)


def get_logs():

    ensure_log_file()

    with open(LOG_FILE, "r", encoding="utf-8") as file:

        return json.load(file)
