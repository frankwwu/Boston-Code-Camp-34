from fastapi import File, UploadFile, APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import json
import os


if "MODEL_FILE" in os.environ:  # Docker
    model_file = os.environ["MODEL_FILE"]
else:  # Non Docker
    with open("Config.json", "r") as f:
        cfg = json.load(f)   
    model_file = cfg['MODEL_FILE']

print(model_file)
model = joblib.load(model_file)


class model_input(BaseModel):
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    passenger_count: int


router = APIRouter(prefix="")


@router.post("/predict")
async def predict(data: model_input) -> dict:
    try:
        input_data = data.dict()
        input_df = pd.DataFrame(input_data, index=[0])
        input_df.reset_index(drop=True, inplace=True)
        predicted_log_fare = predict_df(input_df)
        result_json = post_processor(predicted_log_fare)
        return {"Model": model_file, "Result": result_json}
    except Exception as e:
        return {"Model": model_file, "Exception": str(e)}


@router.post("/batch_predict/")
async def batch_predict(uploaded_file: UploadFile = File(...)) -> dict:
    try:
        df = pd.read_csv(
            uploaded_file.file,
            usecols=[
                "pickup_longitude",
                "pickup_latitude",
                "dropoff_longitude",
                "dropoff_latitude",
                "passenger_count",
            ],
            dtype={
                "pickup_longitude": "float64",
                "pickup_latitude": "float64",
                "dropoff_longitude": "float64",
                "dropoff_latitude": "float64",
                "passenger_count": "int64",
            },
        )
        uploaded_file.file.close()
        predicted_log_fare = predict_df(df)
        result_json = post_processor(predicted_log_fare)
        return {"Model": model_file, "Result": result_json}
    except Exception as e:
        return {"Model": model_file, "Exception": str(e)}


def pre_processor(df):
    df["manhattan_distance"] = np.abs(
        df["pickup_longitude"] - df["dropoff_longitude"]
    ) + np.abs(df["pickup_latitude"] - df["dropoff_latitude"])  
    return df


def predict_df(df):
    x = pre_processor(df)
    predicted_fare = model.predict(x.to_numpy())
    return predicted_fare  # return an array


def post_processor(predicted_log_fare):
     predicted_fare = np.exp(predicted_log_fare)
     result_json = pd.Series(predicted_fare).to_json(orient="values")
     return result_json