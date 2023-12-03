import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# # Function returns the generated Tokens (JWTs)
# def token_response(token: str):
#     return{
#         "access token": token,
#     }

# # Function used for signing the JWT string
def signJWT(user_id: str):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return{}