from pydantic import BaseModel

from src.common.utils.enums import BaseEnum


class CelestialBodyDataIndex(int, BaseEnum):
    """Índices dos dados retornados pela API para maior clareza."""

    IDX_DESIGNATION = 0
    IDX_CLOSE_APPROACH_DATE = 3
    IDX_DISTANCE_AU = 4
    IDX_VELOCITY_KMS = 7


class CelestialBodyCloseApproachFilterParams(BaseModel):
    date_min: str | None
    date_max: str | None
    dist_max: str | None
    sort: str | None

    def __iter__(self):
        for key in self.__dict__:
            yield key.strip().replace("_", "-"), getattr(self, key)


class CelestialBodyCloseApproachDataSchema(BaseModel):
    designation: str
    close_approach_date: str
    distance_au: str
    velocity_kms: str


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
            designation=item[CelestialBodyDataIndex.IDX_DESIGNATION.value],
            close_approach_date=item[CelestialBodyDataIndex.IDX_CLOSE_APPROACH_DATE.value],
            distance_au=item[CelestialBodyDataIndex.IDX_DISTANCE_AU.value],
            velocity_kms=item[CelestialBodyDataIndex.IDX_VELOCITY_KMS.value],
        )
