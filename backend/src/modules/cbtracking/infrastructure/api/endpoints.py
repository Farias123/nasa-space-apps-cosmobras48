from fastapi import status, Depends

from src.core.fastapi.responses import GenericResponse
from src.core.fastapi.requests import QueryParameters
from src.modules.cbtracking.infrastructure.services.close_approach.proximity_data import (
    get_nasa_close_approach_data,
    extract_closest_object,
)
from src.modules.cbtracking.infrastructure.services.horizons.models import (
    HorizonDataCustomBodyRequestParams,
    HorizonDataSolarSystemRequestParams,
)
from src.modules.cbtracking.infrastructure.services.horizons.definitions import Planet
from src.modules.cbtracking.infrastructure.services.horizons.data_extraction import (
    request_data_horizons_solar_system,
    request_vectors_horizons_custom_body,
)
from src.modules.cbtracking.domain.schemas.horizons import (
    HorizonDataDetail,
    HorizonDataDetails,
)
from src.modules.cbtracking.domain.schemas.close_approach import (
    CelestialBodyCloseApproachDetail,
    CelestialBodyCloseApproachDetails,
)

from . import cbtracking_api_router as router


@router.get(
    "/closest_object",
    response_model=GenericResponse[CelestialBodyCloseApproachDetail],  # type: ignore[valid-type, misc]
)
def retrieve_closest_object():
    """Retrieve proximity data, of the closest celestial body to Earth."""
    proximity_data = get_nasa_close_approach_data()
    closest_object = extract_closest_object(proximity_data)

    return {"status": status.HTTP_200_OK, "data": {"object": closest_object}}


@router.get(
    "/proximity_data",
    response_model=GenericResponse[CelestialBodyCloseApproachDetails],  # type: ignore[valid-type, misc]
)
def retrieve_close_approach_data():
    """Retrieve proximity data for a set of celestial bodies, with respect to Earth."""
    proximity_data = get_nasa_close_approach_data()

    return {"status": status.HTTP_200_OK, "data": {"objects": proximity_data}}


@router.get(
    "/horizon/solar_system/{planet_name}",
    response_model=GenericResponse[HorizonDataDetail],  # type: ignore[valid-type, misc]
)
def retrieve_horizon_data_planet(planet_name: Planet, parameters: QueryParameters = Depends(QueryParameters.parser,),):
    """Retrieve horizon data, given a planet's name."""
    raw_filters = parameters.get("dynamic_fields")
    raw_filters.update({"planet_name": planet_name})

    params = HorizonDataSolarSystemRequestParams(**raw_filters)
    horizon_data = request_data_horizons_solar_system(params)

    return {"status": status.HTTP_200_OK, "data": {"object": horizon_data}}


@router.get(
    "/horizon/solar_system",
    response_model=GenericResponse[HorizonDataDetails],  # type: ignore[valid-type, misc]
)
def list_horizon_data_solar_system(parameters: QueryParameters = Depends(QueryParameters.parser,),):
    """Retrieve horizon data, given a planet's name."""
    raw_filters = parameters.get("dynamic_fields")

    params = HorizonDataSolarSystemRequestParams(**raw_filters)
    horizon_data = request_data_horizons_solar_system(params)

    return {"status": status.HTTP_200_OK, "data": { "objects": horizon_data }}


@router.get(
    "/horizon/custom_body",
    response_model=GenericResponse[HorizonDataDetail],  # type: ignore[valid-type, misc]
)
def retrieve_horizon_custom_body(parameters: QueryParameters = Depends(QueryParameters.parser,),):
    """Retrieve horizon data, given custom celestial body's parameters."""
    raw_filters = parameters.get("dynamic_fields")
    params = HorizonDataCustomBodyRequestParams(**raw_filters)
    horizon_data = request_vectors_horizons_custom_body(params)

    return {"status": status.HTTP_200_OK, "data": {"object": horizon_data}}
