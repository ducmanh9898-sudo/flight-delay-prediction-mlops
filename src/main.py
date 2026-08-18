import time
from opentelemetry import trace

from src.telemetry import setup_telemetry
from fastapi import FastAPI, Response
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

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
setup_telemetry(app)

tracer = trace.get_tracer(__name__)

# =========================
# Prometheus Metrics
# =========================

prediction_requests_total = Counter(
    "prediction_requests_total",
    "Total number of prediction requests",
)

prediction_results_total = Counter(
    "prediction_results_total",
    "Total prediction results by label",
    ["label"],
)

prediction_latency_seconds = Histogram(
    "prediction_latency_seconds",
    "Prediction request latency in seconds",
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


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post(
    "/predict",
    response_model=FlightPredictionResponse,
)
def predict(request: FlightPredictionRequest):
    prediction_requests_total.inc()

    start_time = time.perf_counter()

    with tracer.start_as_current_span(
    "model.inference"
    ):
        result = predict_flight_delay(request)

    latency = time.perf_counter() - start_time
    prediction_latency_seconds.observe(latency)

    prediction_results_total.labels(
        label=result["label"]
    ).inc()

    return result
