import jwt
import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

SECRET = os.getenv("JWT_SECRET")

def create_token_from_uuid(uuid: str) -> str:
    payload = {
        "uuid": uuid,
    }
    encoded_jwt: str = jwt.encode(payload, SECRET, algorithm="HS256")
    return encoded_jwt

def decode_token(token: str) -> Dict:
    decoded_jwt = jwt.decode(token, SECRET, algorithms=["HS256"])
    return decoded_jwt

def get_attribute_from_token(token: str, attr_name: str) -> str:
    decoded_jwt_dict = decode_token(token=token)

    if attr_name not in decoded_jwt_dict:
        raise RuntimeError(f"{attr_name} not present in JWT")

    return decoded_jwt_dict[attr_name]
