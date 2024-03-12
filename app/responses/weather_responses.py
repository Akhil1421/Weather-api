from flask_restx import fields

class WeatherApiResponses:

    @classmethod
    def get_single_city_query_response_model(cls, namespace):
        city_model = namespace.model(
            "CityModel",{
                "id": fields.String(),
                "name": fields.String(),
                "country": fields.String(),
                "temperature": fields.Float(),
                "humidity": fields.Integer(),
                "condition": fields.String(),
                "icon": fields.String()
            }
        )

        single_city_query_response_model = {
            "error" : fields.String(),
            "message": fields.String(),
            "data": fields.Nested(city_model)
        }

        return namespace.model(
            "SingleCityQueryResponseModel", single_city_query_response_model
        )

    @classmethod
    def get_add_new_city_model(cls, namespace):
        city_model = namespace.model(
            "CityModel",{
                "name": fields.String(),
                "country": fields.String(),
                "id": fields.Integer(),
            }
        )
        single_city_query_response_model = {
            "error" : fields.String(),
            "message": fields.String(),
            "data": fields.Nested(city_model)
        }

        return namespace.model(
            "AddCityQueryResponseModel", single_city_query_response_model
        )

    @classmethod
    def update_existing_city_model(cls, namespace):
        city_model = namespace.model(
            "CityModel",{
                "name": fields.String(),
                "country": fields.String(),
                "id": fields.Integer(),
            }
        )
        update_city_response_model = {
            "error" : fields.String(),
            "message": fields.String(),
            "data": fields.Nested(city_model)
        }
        return namespace.model(
            "UpdateCityResponseModel", update_city_response_model
        )

    @classmethod
    def get_multi_city_query_response_model(cls, namespace):
        city_model = namespace.model(
            "CityModel",{
                "id": fields.String(),
                "name": fields.String(),
                "country": fields.String(),
                "temperature": fields.Float(),
                "humidity": fields.Integer(),
                "condition": fields.String(),
                "icon": fields.String()
            }
        )
        multi_city_query_response_model = {
            "error" : fields.String(),
            "message": fields.String(),
            "data": fields.List(fields.Nested(city_model))
        }

        return namespace.model(
            "MultiCityResponseModel", multi_city_query_response_model
        )
