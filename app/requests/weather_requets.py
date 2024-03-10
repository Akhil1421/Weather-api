from flask_restx import fields

class WeatherApiRequests:
    add_city_request_model = {
        "name" : fields.String(
            required=True, description="Name of city"
        ),
        "country" : fields.String(
            required=True, description="Name of the country"
        )
    }

    update_city_request_model = {
        "id" : fields.Integer(
            required=True, description="Id of the city to be updated"
        ),
        "name": fields.String(
            required=True, description="Name of the city"
        ),
    }
