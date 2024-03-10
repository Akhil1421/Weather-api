from functools import wraps

from flask import request, abort

from app.utils.jwt_utils import get_attribute_from_token


def authenticate_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token: str = request.headers.get('token')
        if token is None:
            abort(403, description="No token found. Login to get access.")
        try:
            request.uuid = get_attribute_from_token(
                token=token, attr_name="uuid"
            )
        except Exception:
            abort(403, description="Token is invalid. Login to get access.")
        return func(*args, **kwargs)

    return wrapper
