import json
from typing import Any
from loguru import logger

import requests

from src.modules.cbtracking.infrastructure.services.close_approach.definitions import (
    API_URL,
    DEFAULT_FILTERS,
    CelestialBodyCloseApproachObject,
    CelestialBodyCloseApproachFilterParams,
)


def _merge_filter_objects(
    incoming_filters: CelestialBodyCloseApproachFilterParams | None,
) -> CelestialBodyCloseApproachFilterParams:
    if incoming_filters is None:
        return DEFAULT_FILTERS

    for key, value in incoming_filters.__dict__.items():  # type: ignore
        if not value:
            incoming_filters.__dict__.update({key, DEFAULT_FILTERS[key]})  # type: ignore

    return incoming_filters


def get_nasa_close_approach_data(
    incoming_filters: CelestialBodyCloseApproachFilterParams | None = None,
) -> list[CelestialBodyCloseApproachObject] | None:
    """Busca dados de aproximação de objetos próximos à Terra na API da NASA. Retorna uma lista de objetos CloseApproachObject ou None em caso de erro."""

    try:
        logger.info("Fazendo a requisição para a API da NASA...")
        # Faz a requisição GET para a API com os parâmetros definidos
        filters = _merge_filter_objects(incoming_filters)
        response = requests.get(API_URL, params=filters)

        # Verifica se a requisição foi bem-sucedida (código de status 200)
        response.raise_for_status()

        logger.info("Requisição bem-sucedida!")
        # Converte a resposta JSON em um dicionário Python
        data: dict[str, Any] = response.json()

        count: int = data.get("count", 0)
        logger.info(f"Total de objetos encontrados: {count}")

        if not data.get("data"):
            logger.warning(
                "Nenhum dado de aproximação encontrado para os critérios especificados."
            )
            return []

        return [
            CelestialBodyCloseApproachObject.from_list(item) for item in data["data"]
        ]

    except requests.exceptions.RequestException as e:
        logger.error(f"Ocorreu um erro ao fazer a requisição para a API: {e}")
    except json.JSONDecodeError:
        logger.error(
            f"Ocorreu um erro ao decodificar a resposta JSON. Resposta recebida: {response.text}"
        )

    return None


def extract_closest_object(
    proximity_data: list[CelestialBodyCloseApproachObject] | None = None,
) -> CelestialBodyCloseApproachObject | None:
    """Encontra o objeto com a menor distância de aproximação (convertendo a distância para float)."""

    if proximity_data:
        closest_object = min(proximity_data, key=lambda obj: float(obj.distance_au))

        return closest_object

    return None
