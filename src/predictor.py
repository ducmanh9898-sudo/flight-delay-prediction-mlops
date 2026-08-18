from pathlib import Path

import joblib
import pandas as pd

from src.schemas import FlightPredictionRequest


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Trained model artifact
MODEL_PATH = PROJECT_ROOT / "models" / "flight_delay_pipeline.joblib"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model artifact not found at: {MODEL_PATH}"
    )

# Load once when the application starts
model = joblib.load(MODEL_PATH)


def predict_flight_delay(request: FlightPredictionRequest) -> dict:
    """
    Predict whether a flight will be delayed.

    Returns:
        prediction: 0 or 1
        label: NOT_DELAYED or DELAYED
        probability: probability of class 1 (delay)
    """

    input_data = pd.DataFrame(
        [
            {
                "Time": float(request.Time),
                "Length": float(request.Length),
                "Airline": request.Airline,
                "AirportFrom": request.AirportFrom,
                "AirportTo": request.AirportTo,
                "DayOfWeek": str(request.DayOfWeek),
            }
        ]
    )

    prediction = int(model.predict(input_data)[0])

    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    label = (
        "DELAYED"
        if prediction == 1
        else "NOT_DELAYED"
    )

    return {
        "prediction": prediction,
        "label": label,
        "probability": round(probability, 4),
    }
