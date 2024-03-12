import requests
import json
import os

from flask import request
from flask_restx import Namespace, Resource, reqparse
from sqlalchemy import and_
from dotenv import load_dotenv

import app.database.query_manager as query_manager
from app.middleware.auth import authenticate_user
from app.utils.city_data_utils import get_required_attributes
from app.responses.weather_responses import WeatherApiResponses
from app.database.models.user import User
from app.database.models.city import CityAssociatedWithUser
from app.requests.weather_requets import WeatherApiRequests
import app.cache.cache as cache


load_dotenv()
WEATHER_API_URL = os.getenv("WEATHER_API_URI")
WEATHER_API_AUTH_KEY = os.getenv("WEATHER_API_AUTH_KEY")

weather_api_ns = Namespace("weather", description="APIs for querying weather")


@weather_api_ns.route("")
class AllCitiesWeatherDataApi(Resource):
    @weather_api_ns.marshal_with(
        WeatherApiResponses.get_multi_city_query_response_model(namespace=weather_api_ns)
    )
    @authenticate_user
    def get(self):
        user_uuid = request.uuid
        user = query_manager.query_with_filter(
            model=User, filters=and_(User.uuid == user_uuid)
        )
        if user is None :
            return {
                "error" : "INVALID_USER",
                "message" : "No user with given uuid in database"
            }, 401
        cities_of_user = query_manager.query_all_with_filter(
            model=CityAssociatedWithUser, 
            filters=and_(CityAssociatedWithUser.user_id==user.id)
        )

        cities_data = []
        for city in cities_of_user:
            city_name = city.name    
            try:
                response = requests.get(f"{WEATHER_API_URL}?q={city_name}&key={WEATHER_API_AUTH_KEY}")
                response_dict = json.loads(response.text)
                if 'error' not in response_dict:
                    city_data = get_required_attributes(response_dict)
                    cache.add_or_update_city(city=city, city_data=city_data)
                    city_data['id'] = city.id
                    cities_data.append(city_data)
                else :
                    raise requests.exceptions.ConnectionError("Could not fetch data")

            except requests.exceptions.ConnectionError:
                if cache.query_city(city=city) is None:
                    return {
                        "error": "SERVICE_UNREACHABLE",
                        "message": "Service unavailable",
                        "data": []
                    }, 503
                city_data = cache.query_city(city=city)
                city_data['id'] = city.id
                cities_data.append(city_data)

        return {
            "error": None,
            "message": "Data fetched successfully",
            "data": cities_data
        }, 200


@weather_api_ns.route("/city")
class WeatherQueryApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("city", help="Name of city for weather", required=True)

    @weather_api_ns.expect(parser)
    @weather_api_ns.marshal_with(
        WeatherApiResponses.get_single_city_query_response_model(namespace=weather_api_ns)
    )
    def get(self):
        args = self.parser.parse_args()
        city = args["city"]
        try:
            response = requests.get(f"{WEATHER_API_URL}?q={city}&key={WEATHER_API_AUTH_KEY}")
            response_dict = json.loads(response.text)

            if 'error' not in response_dict:
                city_data = get_required_attributes(response_dict)
                cache.add_or_update_city(city=city, city_data=city_data)
                return {
                    "error": None,
                    "message": "Data fetched successfully",
                    "data": city_data
                }, 200

            return {
                "error" : "INVALID_REQUEST",
                "message" : response_dict['error']['message']
            }, 400
        
        except requests.exceptions.ConnectionError as e:
            print(str(e))
            return {
                "error" : "CONNECTION_ERROR",
                "message" : "Network error occurred on server",
                "data" : cache.query_city(city=city)
            },200


@weather_api_ns.route("/city")
class CityApi(Resource):
    add_city_request = weather_api_ns.model(
        "CityApiRequest", WeatherApiRequests.add_city_request_model
    )
    
    @weather_api_ns.expect(add_city_request, validate=True)
    @weather_api_ns.marshal_with(
        WeatherApiResponses.get_add_new_city_model(namespace=weather_api_ns)
    )
    @authenticate_user
    def post(self):
        user_uuid = request.uuid
        request_data = request.json
        user = query_manager.query_with_filter(
            model=User, filters=and_(User.uuid == user_uuid)
        )
        if user is None :
            return {
                "error" : "INVALID_USER",
                "message" : "No user with given uuid in database"
            }, 401
        
        cities_associated_with_user = query_manager.query_all_with_filter(
            model=CityAssociatedWithUser, filters=and_(CityAssociatedWithUser.user_id==user.id)
        )
        
        if len(cities_associated_with_user) == 4 :
            return {
                "error": "INVALID_REQUEST",
                "message": "4 cities are already associated with user"
            }, 400
        
        for city in cities_associated_with_user:
            if city.name == request_data['name']:
                return {
                    "error" : "INVALID_REQUEST",
                    "message": "City with the same name already bounded to user."
                }, 400

        city_curr_data = {}
        try:
            response = requests.get(f"{WEATHER_API_URL}?q={request_data['name']}&key={WEATHER_API_AUTH_KEY}")
            response_dict = json.loads(response.text)

            if 'error' in response_dict:
                return {
                    "error" : "INVALID_REQUEST",
                    "message": "City name is not valid"
                }, 400
            city_curr_data = get_required_attributes(response_dict)
            cache.add_or_update_city(request_data['name'], city_data=city_curr_data)

        except requests.exceptions.ConnectionError :
            raise(Exception("Service unavailable"))

        new_city_added = CityAssociatedWithUser(
            id = len(cities_associated_with_user),
            user_id = user.id,
            name = request_data['name'],
            country = city_curr_data['country'],
        )
        query_manager.insert_single_object(new_city_added)

        return {
            "error": None,
            "message": "City associated with user successfully",
            "data": new_city_added
        },201

    update_city_request = weather_api_ns.model(
        "CityApiUpdateRequest", WeatherApiRequests.update_city_request_model
    )

    @weather_api_ns.expect(update_city_request, validate=True)
    @weather_api_ns.marshal_with(
        WeatherApiResponses.update_existing_city_model(namespace=weather_api_ns)
    )
    @authenticate_user
    def put(self):
        user_uuid = request.uuid
        user = query_manager.query_with_filter(
            model=User, filters=and_(User.uuid == user_uuid)
        )
        if user is None :
            return {
                "error" : "INVALID_USER",
                "message" : "No user with given uuid in database"
            }, 401

        request_data = request.json
        city_id = request_data['id']

        city_dict = query_manager.query_with_filter(
            model=CityAssociatedWithUser, filters=and_(
                CityAssociatedWithUser.user_id==user.id, 
                CityAssociatedWithUser.id==city_id)
        )

        if city_dict is None:
            return {
                "error" : "INVALID_ARGUEMENTS",
                "message" : "User not associated with provided city id"
            }, 400

        cities_associated_with_user = query_manager.query_all_with_filter(
            model=CityAssociatedWithUser, filters=and_(CityAssociatedWithUser.user_id==user.id)
        )

        for city in cities_associated_with_user:
            if city.name == request_data['name']:
                return {
                    "error" : "INVALID_REQUEST",
                    "message": "City with the same name already bounded to user."
                }, 400

        city_curr_data = {}
        try:
            response = requests.get(f"{WEATHER_API_URL}?q={request_data['name']}&key={WEATHER_API_AUTH_KEY}")
            response_dict = json.loads(response.text)

            if 'error' in response_dict:
                return {
                    "error" : "INVALID_REQUEST",
                    "message": "City name is not valid"
                }, 400
            city_curr_data = get_required_attributes(response_dict)
            cache.add_or_update_city(request_data['name'], city_data=city_curr_data)
        
        except requests.exceptions.ConnectionError :
            raise(Exception("Service unavailable"))

        updates = {
            "name": request_data['name']
        }
        updates['country'] =  city_curr_data['country']

        query_manager.update_objects(model=CityAssociatedWithUser, filters=and_(
            CityAssociatedWithUser.user_id==user.id, 
            CityAssociatedWithUser.id==city_id
        ), updates=updates)

        city_data = query_manager.query_with_filter(
            model=CityAssociatedWithUser, 
            filters=and_(
                CityAssociatedWithUser.user_id==user.id, 
                CityAssociatedWithUser.id==city_id
            )
        )
        return {
            "error": None,
            "message": "Data updated successfully",
            "data": city_data
        }, 200


    parser = reqparse.RequestParser()
    parser.add_argument("id", help="Id of city to be deleted", required=True)
    @weather_api_ns.expect(parser, validate=True)
    @authenticate_user
    def delete(self):
        args = self.parser.parse_args()
        city_id = args['id']
        user_uuid = request.uuid
        user = query_manager.query_with_filter(
            model=User, filters=and_(User.uuid == user_uuid)
        )
        if user is None :
            return {
                "error" : "INVALID_USER",
                "message" : "No user with given uuid in database"
            }, 403
        
        city_dict = query_manager.query_with_filter(
            model=CityAssociatedWithUser, filters=and_(
                CityAssociatedWithUser.user_id==user.id, 
                CityAssociatedWithUser.id==city_id)
        )

        if city_dict is None:
            return {
                "error" : "INVALID_ARGUEMENTS",
                "message" : "User not associated with provided city id"
            }, 400

        query_manager.delete_objects(
            model=CityAssociatedWithUser, 
            filters=and_(CityAssociatedWithUser.user_id==user.id,
                CityAssociatedWithUser.id==city_id            
            )
        )

        return {
            "error": None,
            "message": "City deleted successfully",
        }, 200


@weather_api_ns.route("/city/<city_id>")
class WeatherApi(Resource):
    @weather_api_ns.marshal_with(
        WeatherApiResponses.get_single_city_query_response_model(namespace=weather_api_ns)
    )
    @authenticate_user
    def get(self, city_id):
        user_uuid = request.uuid
        user = query_manager.query_with_filter(
            model=User, filters=and_(User.uuid == user_uuid)
        )
        if user is None :
            return {
                "error" : "INVALID_USER",
                "message" : "No user with given uuid in database"
            }, 403

        city_id = int(city_id)
        if city_id >= 4:
            return {
                "error" : "INVALID_ARGUEMENTS",
                "message" : "City id provided is incorrect"
            }, 400
        
        city_dict = query_manager.query_with_filter(
            model=CityAssociatedWithUser, filters=and_(
                CityAssociatedWithUser.user_id==user.id, 
                CityAssociatedWithUser.id==city_id)
        )

        if city_dict is None:
            return {
                "error" : "INVALID_ARGUEMENTS",
                "message" : "User not associated with provided city id"
            }, 400

        city = city_dict.name

        try:
            response = requests.get(f"{WEATHER_API_URL}?q={city}&key={WEATHER_API_AUTH_KEY}")
            response_dict = json.loads(response.text)

            if 'error' not in response_dict:
                city_data = get_required_attributes(response_dict)
                city_data['id'] = city_id
                return {
                    "error": None,
                    "message": "Data fetched successfully",
                    "data": city_data
                }, 200

            return {
                "error" : "INVALID_REQUEST",
                "message" : response_dict['error']['message']
            }, 400

        except requests.exceptions.ConnectionError as error:
            city_data = cache.query_city(city=city)
            if city_data is not None:
                city_data['id'] = city_id
            return {
                "error" : "CONNECTION_ERROR",
                "message" : "Connection error with weather api",
                "data" : city_data
            },200
