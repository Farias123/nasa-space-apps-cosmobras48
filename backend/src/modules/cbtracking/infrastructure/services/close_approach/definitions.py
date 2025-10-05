from .models import CelestialBodyCloseApproachFilterParams


# NASA/JPL SBDB Close Approach Data API
API_URL = "https://ssd-api.jpl.nasa.gov/cad.api"


DEFAULT_FILTERS = CelestialBodyCloseApproachFilterParams(
    date_max="+60",
    date_min="now",
    dist_max="0.05",  # Distância máxima em unidades astronômicas (UA)
    sort="date",  # Ordenar os resultados por data
)
