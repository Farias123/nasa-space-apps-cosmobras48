from pydantic import BaseModel

from src.modules.cbtracking.infrastructure.services.horizons.definitions import Planet

class HorizonDataCustomBodyRequestParams(BaseModel):
    start_time: str
    stop_time: str
    step_size: str
    eccentricity: float
    longitude_of_ascending_node: float
    argument_of_perihelion: float
    mean_anomaly: float
    larger_semi_major_axis: float
    orbital_inclination: float
    object_name: str
    epoch: str
    frame: str


class HorizonDataSolarSystemRequestParams(BaseModel):
    planet_name: Planet | None = None
    initial_date: str
    end_date: str
    step_size: str


class HorizonUnitsMetadata(BaseModel):
    distance: str
    mass: str
    velocity: str


class HorizonMetaData(BaseModel):
    units: HorizonUnitsMetadata

class HorizonData(BaseModel):
    mass: float | None = None
    radius: float | None = None
    x: list[float] | None = None
    y: list[float] | None = None
    z: list[float] | None = None
    vx: list[float] | None = None
    vy: list[float] | None = None
    vz: list[float] | None = None
    dates: list[str] | None = None

class HorizonDataResponse(BaseModel):
    body_name: Planet | None = None
    horizon_data: HorizonData
    metadata: HorizonMetaData
