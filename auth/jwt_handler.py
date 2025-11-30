import time
from jose import jwt
from config import JWT_SECRET, JWT_ALGORITHM

def sign_jwt(user_id: str):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded if decoded["expires"] >= time.time() else None
    except:
        return None
