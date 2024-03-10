from flask import request
from flask_restx import Namespace, Resource
from app.requests.auth_requests import AuthApiRequests
from app.responses.auth_responses import AuthApiResponse
from app.utils.jwt_utils import create_token_from_uuid
import app.database.query_manager as query_manager
from app.database.models.user import User

auth_api_ns = Namespace("auth", description="APIs for creating user session")

@auth_api_ns.route("/jwt")
class Authentication(Resource):
    add_user_request = auth_api_ns.model(
        "AuthApiRequest", AuthApiRequests.auth_api_request_model
    )

    add_user_response = auth_api_ns.model(
        "AuthApiResponse", AuthApiResponse.auth_api_response_model
    )

    @auth_api_ns.expect(add_user_request, validate=True)
    @auth_api_ns.marshal_with(add_user_response)
    def post(self):
        request_data = request.json
        uuid = request_data['uuid']
        username = request_data['username']
        if len(uuid) == 0:
            return {
                "error": "INVALID_UUID",
                "message": "UUID can't be empty",
                "token": None
            }, 400

        user = User(uuid=uuid, username=username)
        query_manager.insert_single_object(user)
        token = create_token_from_uuid(uuid=uuid)
        return {
            "error": None,
            "message": "Token created for session successfully",
            "jwt" : token
        }
