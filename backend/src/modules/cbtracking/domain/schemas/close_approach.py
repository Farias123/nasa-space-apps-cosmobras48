from src.core.fastapi.responses import create_data_model
from src.modules.cbtracking.infrastructure.services.close_approach.models import (
    CelestialBodyCloseApproachDataSchema,
)


CelestialBodyCloseApproachDetail = create_data_model(
    CelestialBodyCloseApproachDataSchema, custom_single_name="object"
)
CelestialBodyCloseApproachDetails = create_data_model(
    CelestialBodyCloseApproachDataSchema, plural=True, custom_plural_name="objects"
)
