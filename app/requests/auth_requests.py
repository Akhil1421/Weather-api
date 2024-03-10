from flask_restx import fields

class AuthApiRequests:
    auth_api_request_model = {
        "uuid" : fields.String(
            required=True, description="UUID generated for session of the user"
        ),
        "username" : fields.String(
            required=True, description="Username of the user"
        )
    }
