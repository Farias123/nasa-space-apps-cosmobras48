from src.common.utils.enums import BaseEnum


class Planet(BaseEnum):
    MERCURY = "Mercury"
    VENUS = "Venus"
    EARTH = "Earth"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    SUN = "Sun"


center_body = "500@10"  # Sun


dict_planets = {
    "Mercury": 199,
    "Venus": 299,
    "Earth": 399,
    "Mars": 499,
    "Jupiter": 599,
    "Saturn": 699,
    "Uranus": 799,
    "Neptune": 899,
}

mass_planets = {
    "Mercury": 0.33010e24,
    "Venus": 4.8673e24,
    "Earth": 5.9722e24,
    "Mars": 0.64169e24,
    "Jupiter": 1898.13e24,
    "Saturn": 568.32e24,
    "Uranus": 86.811e24,
    "Neptune": 102.409e24,
}

radius_planets = {
    "Mercury": 2439.7,
    "Venus": 6051.8,
    "Earth": 6371,
    "Mars": 3389.5,
    "Jupiter": 69_911,
    "Saturn": 58_232,
    "Uranus": 25_362,
    "Neptune": 24_622,
}

default_horizon_metadata = {
    "units": {
        "distance": "km",
        "mass": "kg",
        "velocity": "km/s"
    }
}

default_horizon_planets = [
    {
        "body_name": "Sun",
        "horizon_data": {
            "mass": 1_988_500e24,
            "radius": 695_700,
        },
        "metadata": default_horizon_metadata,
    }
]
