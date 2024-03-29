<h1>Documentation for Weather API using Flask Restx</h1>

### Deployment Link 
Use link below to view swagger ui documentation of the API.
```
    https://weather-api-5xrq.onrender.com/
```
## Setting Up Environment

### Prerequisities : 
1. Python installed
2. MYSQL installed and setup with a DB

### Setting Up Python Libraries
- After you clone the project, just run
```
    pip install -r requirements.txt
```

## Structure of the project :

### run.py
- This is the main file of the backend from where flask application server is run.

### app
- This is the folder containing the entire application logic. This folder contains following :
    - cache folder :
        - This folder just contains cache.py where cache dictionary is defined along with cron job and queries to fill up, update or get data incase open weather api is down.
        - Cron job will fill up fresh data for cities every 1 hour.
    - middleware folder :
        - This folder contains the middleware used for getting the JWT token for authentication from the request for private routes access.
    - requests folder :
        - This folder contains request models which the api endpoints are expecting from the request from the frontend.
    - responses folder :
        - This folder contains response models which will be sent as results as the response for request on an endpoint.
    - routes folder :
        - This folder contains definitions for different routes.
        - There are 2 main files in this folder :
            - auth_routes.py :
                - This file is where auth route for getting a JWT is set.
            - weather_routes.py :
                - This file is where all the routes for weather queries, CRUD on cities associated with user are setup.
    - database folder :
        - This folder contains following :
            - database_engine.py :
                - This is where connection is set up bw MYSQL DB and flask app.
            - query_manager.py :
                - This is where functions for the queries on DB models are defined.
            - models folder :
                - This directory contains base, city and user models.
     - utils directory :
         - This is where various helping functions are defined.
     - main.py :
         - This is where main flask application setup is done along with exception handling.
     
## Create Session For User (POST)
This route is for creating user session and getting a JWT for authentication.
``` https://weather-api-5xrq.onrender.com/auth/jwt```

Command:
```
curl --location 'https://weather-api-5xrq.onrender.com/auth/jwt' 
--data '{
    "username":"username_of_user_for_session",
    "uuid":"Randomly generated UUID"
}'
```
## Get Weather of cities associated with user (GET)
```https://weather-api-5xrq.onrender.com/weather```

Command:
```
curl --location 'https://weather-api-5xrq.onrender.com/weather'
--header '{
    "token" : "JWT_token_stored_in_local_storage_while_creating_session"
}'
```

## Get Weather of particular city associated with user (GET)
```https://weather-api-5xrq.onrender.com/weather/city/{city_id}```

Command:
```
curl --location 'https://weather-api-5xrq.onrender.com/weather/city/:city_id'
--header '{
    "token" : "JWT_token_stored_in_local_storage_while_creating_session"
}'
```
## Add a new city associated with user (POST)
```https://weather-api-5xrq.onrender.com/weather/city```

Command:
```
curl --location 'https://weather-api-5xrq.onrender.com/weather/city'
--header '{
    "token" : "JWT_token_stored_in_local_storage_while_creating_session"
}'
--data '{
    "name":"City_name",
    "country":"Country of City"
}'
```

## Update an existing city associated with user (PUT)
```https://weather-api-5xrq.onrender.com/weather/city```

Command:
```
curl --location 'https://weather-api-5xrq.onrender.com/weather/city'
--header '{
    "token" : "JWT_token_stored_in_local_storage_while_creating_session"
}'
--data '{
    "name":"New name for the city",
    "id":"Id of the city to be updated"
}'
```
## Delete an existing city associated with user (DELETE)
```https://weather-api-5xrq.onrender.com/weather/city```

Command:
```
curl --location 'https://weather-api-5xrq.onrender.com/weather/city?id=valid_city_id'
--header '{
    "token" : "JWT_token_stored_in_local_storage_while_creating_session"
}'
```

## Run Development Server
Command:
```
    python run.py
```
## Run Production server
Command:
```
    gunicorn run:app
```
