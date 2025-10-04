from pydantic import BaseModel


# NASA/JPL SBDB Close Approach Data API
API_URL = "https://ssd-api.jpl.nasa.gov/cad.api"


# Índices dos dados retornados pela API para maior clareza
IDX_DESIGNATION = 0
IDX_CLOSE_APPROACH_DATE = 3
IDX_DISTANCE_AU = 4
IDX_VELOCITY_KMS = 7


class CelestialBodyCloseApproachObject(BaseModel):
    """Representa os dados de um objeto em aproximação."""

    designation: str
    close_approach_date: str
    distance_au: str
    velocity_kms: str

    @classmethod
    def from_list(cls, item: list[str]) -> "CelestialBodyCloseApproachObject":
        """Cria uma instância a partir da lista de dados da API."""
        return cls(
            designation=item[IDX_DESIGNATION],
            close_approach_date=item[IDX_CLOSE_APPROACH_DATE],
            distance_au=item[IDX_DISTANCE_AU],
            velocity_kms=item[IDX_VELOCITY_KMS],
        )


class CelestialBodyCloseApproachFilterParams(BaseModel):
    date_min: str | None
    date_max: str | None
    dist_max: str | None
    sort: str | None


DEFAULT_FILTERS = CelestialBodyCloseApproachFilterParams(
    **{
        "date-min": "now",
        "date-max": "+60",
        "dist-max": "0.05",  # Distância máxima em unidades astronômicas (UA)
        "sort": "date",  # Ordenar os resultados por data
    }
)
