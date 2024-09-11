import jwt
import time
from Instruments.Config import public_key, secret_key

async def generate_token():
    token_lifetime = 86400
    time_now = int(time.time())

    payload = {
        "iss": "api.ilovepdf.com",
        "aud": "",
        "iat": time_now,
        "nbf": time_now,
        "exp": time_now + token_lifetime,
        "jti": public_key
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
