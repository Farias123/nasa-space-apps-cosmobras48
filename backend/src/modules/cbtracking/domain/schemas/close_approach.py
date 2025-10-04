from pydantic import BaseModel
from src.core.fastapi.responses import create_data_model


class CelestialBodyCloseApproachFilterSchema(BaseModel):
    date_min: str | None
    date_max: str | None
    dist_max: float | None
    sort: str | None


class CelestialBodyCloseApproachDataSchema(BaseModel):
    designation: str
    close_approach_date: str
    distance_au: str
    velocity_kms: str


CelestialBodyCloseApproachDetail = create_data_model(
    CelestialBodyCloseApproachDataSchema, custom_single_name="object"
)
CelestialBodyCloseApproachDetails = create_data_model(
    CelestialBodyCloseApproachDataSchema, plural=True, custom_plural_name="objects"
)
