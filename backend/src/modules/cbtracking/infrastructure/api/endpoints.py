from fastapi import status
from dependency_injector.wiring import inject

from src.core.fastapi.responses import GenericResponse
from src.modules.cbtracking.infrastructure.services.close_approach.proximity_data import (
    get_nasa_close_approach_data,
    extract_closest_object,
)

from src.modules.cbtracking.domain.schemas.close_approach import (
    CelestialBodyCloseApproachDetail,
    CelestialBodyCloseApproachDetails,
)

from . import cbtracking_api_router as router


@router.get(
    "/proximity_data",
    response_model=GenericResponse[CelestialBodyCloseApproachDetails],  # type: ignore[valid-type, misc]
)
@inject
def retrieve_close_approach_data():
    """Retrieve proximity data for a set of celestial bodies, with respect to Earth."""
    proximity_data = get_nasa_close_approach_data()

    return {"status": status.HTTP_200_OK, "data": {"objects": proximity_data}}


@router.get(
    "/closest_object",
    response_model=GenericResponse[CelestialBodyCloseApproachDetail],  # type: ignore[valid-type, misc]
)
@inject
def retrieve_closest_object():
    """Retrieve proximity data, of the closest celestial body to Earth."""
    proximity_data = get_nasa_close_approach_data()
    closest_object = extract_closest_object(proximity_data)

    return {"status": status.HTTP_200_OK, "data": {"object": closest_object}}
