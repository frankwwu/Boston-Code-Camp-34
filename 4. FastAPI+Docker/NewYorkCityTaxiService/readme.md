# Docker
cd "C:\Users\frank\Documents\GitHub\Boston-Code-Camp-34\4. FastAPI+Docker\NewYorkCityTaxiService"

docker build -t new_york_city_taxi_service.

docker run --env-file=.env --name new_york_city_taxi_service -p 8000:8000 new_york_city_taxi_service

docker run --env MODEL_FILE=new_york_city_taxi_fare_et_100k_log_model.joblib --name new_york_city_taxi_service -p 8000:8000 new_york_city_taxi_service

http://127.0.0.1:8000/docs#/

docker stop new_york_city_taxi_service
