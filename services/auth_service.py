import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

USERS_FILE = BASE_DIR / "data" / "users.json"


def load_users():

    if not USERS_FILE.exists():

        return []

    with open(USERS_FILE, "r", encoding="utf-8") as file:

        return json.load(file)

def save_users(users):

        with open(USERS_FILE, "w", encoding="utf-8") as file:

            json.dump(users, file, indent=4)

def login(username, password):

        users = load_users()

        for user in users:

            if user["username"] == username and user["password"] == password:

                return True

        return False

def register_user(username, password, email):

        users = load_users()

        users.append({"username": username, "password": password, "email": email})

        save_users(users)
