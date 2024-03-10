import werkzeug
from app.cache.cache import cron_job
from flask import Flask, jsonify
from flask_restx import Api
from apscheduler.schedulers.background import BackgroundScheduler
from app.routes.auth_routes import auth_api_ns
from app.routes.weather_routes import weather_api_ns


app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app)
api.add_namespace(auth_api_ns)
api.add_namespace(weather_api_ns)

scheduler = BackgroundScheduler()
scheduler.add_job(cron_job, 'interval', minutes=60)
scheduler.start()

@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_exception(error):
    response = jsonify({"error": "Requested URL not avilable on server"})
    response.status_code = 404
    return response

@app.errorhandler(Exception)
def handle_exception(error):
    response = jsonify({"error": error.args[0]})
    response.status_code = 500
    return response
