from pydantic import BaseModel, Field


class FlightPredictionRequest(BaseModel):
    Time: int = Field(
        ...,
        ge=0,
        le=1439,
        description="Scheduled departure time in minutes after midnight",
        examples=[1235],
    )

    Length: float = Field(
        ...,
        gt=0,
        description="Scheduled flight length in minutes",
        examples=[80.0],
    )

    Airline: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Two-character airline code",
        examples=["MQ"],
    )

    AirportFrom: str = Field(
        ...,
        pattern=r"^[A-Z]{3}$",
        description="Three-letter origin airport code",
        examples=["DFW"],
    )

    AirportTo: str = Field(
        ...,
        pattern=r"^[A-Z]{3}$",
        description="Three-letter destination airport code",
        examples=["CRP"],
    )

    DayOfWeek: int = Field(
        ...,
        ge=1,
        le=7,
        description="Day of week: 1=Monday, ..., 7=Sunday",
        examples=[5],
    )


class FlightPredictionResponse(BaseModel):
    prediction: int
    label: str
    probability: float
