# backend/auth.py
users_db = {
    "Somik": {"password": "finance123", "role": "finance"},
    "Prakhar": {"password": "marketing123", "role": "marketing"},
    "Vanshika": {"password": "hr123", "role": "hr"},
    "Writo": {"password": "engineering123", "role": "engineering"},
    "Samyak": {"password": "executive123", "role": "executive"},
    "Srishti": {"password": "employee123", "role": "employee"}
}

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None
