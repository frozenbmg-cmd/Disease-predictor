import json
import os

FILE = "users.json"

def load_users():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f)

def register(username, password):
    users = load_users()
    if username in users:
        return False

    users[username] = {
        "password": password,
        "history": []
    }

    save_users(users)
    return True

def login(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password

def save_history(username, data):
    users = load_users()
    users[username]["history"].append(data)
    save_users(users)

def get_history(username):
    users = load_users()
    return users[username]["history"]