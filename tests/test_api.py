import pandas as pd

from fastapi.testclient import TestClient

from src.main import app
from src.predictor import model


client = TestClient(app)


VALID_PAYLOAD = {
    "Time": 1235,
    "Length": 80,
    "Airline": "MQ",
    "AirportFrom": "DFW",
    "AirportTo": "CRP",
    "DayOfWeek": 5,
}


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model"] == "loaded"


def test_predict_returns_valid_response():
    response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["prediction"] in [0, 1]
    assert body["label"] in [
        "NOT_DELAYED",
        "DELAYED",
    ]
    assert 0.0 <= body["probability"] <= 1.0


def test_api_prediction_matches_direct_model():
    response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    assert response.status_code == 200

    api_result = response.json()

    model_input = pd.DataFrame(
        [
            {
                "Time": float(VALID_PAYLOAD["Time"]),
                "Length": float(VALID_PAYLOAD["Length"]),
                "Airline": VALID_PAYLOAD["Airline"],
                "AirportFrom": VALID_PAYLOAD["AirportFrom"],
                "AirportTo": VALID_PAYLOAD["AirportTo"],
                "DayOfWeek": str(
                    VALID_PAYLOAD["DayOfWeek"]
                ),
            }
        ]
    )

    direct_prediction = int(
        model.predict(model_input)[0]
    )

    direct_probability = float(
        model.predict_proba(model_input)[0][1]
    )

    assert (
        api_result["prediction"]
        == direct_prediction
    )

    assert (
        api_result["label"]
        == (
            "DELAYED"
            if direct_prediction == 1
            else "NOT_DELAYED"
        )
    )

    assert abs(
        api_result["probability"]
        - round(direct_probability, 4)
    ) < 1e-9


def test_invalid_input_returns_422():
    invalid_payload = {
        "Time": 2000,
        "Length": -10,
        "Airline": "MQ",
        "AirportFrom": "DF",
        "AirportTo": "CRP",
        "DayOfWeek": 9,
    }

    response = client.post(
        "/predict",
        json=invalid_payload,
    )

    assert response.status_code == 422
