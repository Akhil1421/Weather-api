from flask_restx import fields

class AuthApiResponse:
    auth_api_response_model = {
        "error" : fields.String(),
        "message" : fields.String(),
        "jwt" : fields.String(
            description="JWT signed based on UUID provided"
        )
    }
