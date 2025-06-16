# backend/auth.py
users_db = {
    "alice": {"password": "finance123", "role": "finance"},
    "bob": {"password": "marketing123", "role": "marketing"},
    "carol": {"password": "hr123", "role": "hr"},
    "dave": {"password": "engineering123", "role": "engineering"},
    "eve": {"password": "executive123", "role": "executive"},
    "frank": {"password": "employee123", "role": "employee"}
}

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None
