from jwt import JWT, jwk_from_dict, jwk_from_pem
import time
import json
import os

key = os.getenv("PRIVATE_KEY")

public = os.getenv("PUBLIC_KEY")


def generate_jwt_token(message: dict):
    try:
        signing_key = jwk_from_pem(bytes(key, 'utf-8'))
        jwt = JWT()
        data = {
            "session": message,
            "iat": int(time.time()),
            'exp': int(time.time()) + (3 * (24 * 60 * 60))
        }
        d = json.dumps(data, default=str)
        token = jwt.encode(d, signing_key, 'RS256')
        return token
    except Exception as e:
        return ""


def decode_jwt_token(token: str):
    verifying_key = jwk_from_pem(bytes(public.strip(), 'utf-8'))
    jwt = JWT()
    message = jwt.decode(message=token, key=verifying_key, do_verify=False)
    if isinstance(message, dict):
        return message
    else:
        return json.loads(message) or message

def validate_token(data: dict):
    current_time = int(time.time())
    expires_at = data['exp']
    if expires_at < current_time:
        return {"error": True, "message": "token expired"}

    session = data['session']
    return {"error": False}