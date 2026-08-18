from fastapi import FastAPI

from src.schemas import (
    FlightPredictionRequest,
    FlightPredictionResponse,
)
from src.predictor import predict_flight_delay


app = FastAPI(
    title="Flight Delay Prediction API",
    description=(
        "Machine Learning API for predicting whether "
        "a scheduled flight will be delayed."
    ),
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Flight Delay Prediction API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model": "loaded",
    }

@app.post(
    "/predict",
    response_model=FlightPredictionResponse
)
def predict(request: FlightPredictionRequest):
    return predict_flight_delay(request)
