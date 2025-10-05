import requests
import json
import logging
import pathlib
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

# Define o diretório base do script para salvar o log na mesma pasta
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# Configuração do logger para salvar em arquivo
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(BASE_DIR / 'execucao.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Constantes
API_URL = "https://ssd-api.jpl.nasa.gov/cad.api"
DEFAULT_PARAMS = {
    'date-min': 'now',
    'date-max': '+60',
    'dist-max': '0.05',  # Distância máxima em unidades astronômicas (UA)
    'sort': 'date'       # Ordenar os resultados por data
}

# Índices dos dados retornados pela API para maior clareza
IDX_DESIGNATION = 0
IDX_CLOSE_APPROACH_DATE = 3
IDX_DISTANCE_AU = 4
IDX_VELOCITY_KMS = 7

@dataclass
class CloseApproachObject:
    """Representa os dados de um objeto em aproximação."""
    designation: str
    close_approach_date: str
    distance_au: str
    velocity_kms: str

    @classmethod
    def from_list(cls, item: List[str]) -> 'CloseApproachObject':
        """Cria uma instância a partir da lista de dados da API."""
        return cls(
            designation=item[IDX_DESIGNATION],
            close_approach_date=item[IDX_CLOSE_APPROACH_DATE],
            distance_au=item[IDX_DISTANCE_AU],
            velocity_kms=item[IDX_VELOCITY_KMS]
        )

def get_nasa_close_approach_data() -> Optional[List[CloseApproachObject]]:
    """
    Busca dados de aproximação de objetos próximos à Terra na API da NASA.
    Retorna uma lista de objetos CloseApproachObject ou None em caso de erro.
    """
    try:
        logger.info("--- INICIANDO NOVA EXECUÇÃO ---")
        logger.info(f"Filtros utilizados na busca: {json.dumps(DEFAULT_PARAMS)}")
        logger.info("Fazendo a requisição para a API da NASA...")
        # Faz a requisição GET para a API com os parâmetros definidos
        response = requests.get(API_URL, params=DEFAULT_PARAMS)

        # Verifica se a requisição foi bem-sucedida (código de status 200)
        response.raise_for_status()

        logger.info("Requisição bem-sucedida!")
        # Converte a resposta JSON em um dicionário Python
        data: Dict[str, Any] = response.json()

        count: int = data.get('count', 0)
        logger.info(f"Total de objetos encontrados: {count}")

        if not data.get('data'):
            logger.warning("Nenhum dado de aproximação encontrado para os critérios especificados.")
            return []
        
        return [CloseApproachObject.from_list(item) for item in data['data']]

    except requests.exceptions.RequestException as e:
        logger.error(f"Ocorreu um erro ao fazer a requisição para a API: {e}")
    except json.JSONDecodeError:
        logger.error(f"Ocorreu um erro ao decodificar a resposta JSON. Resposta recebida: {response.text}")
    
    return None

if __name__ == "__main__":
    objects = get_nasa_close_approach_data()
    if objects:
        # Encontra o objeto com a menor distância de aproximação (convertendo a distância para float)
        closest_object = min(objects, key=lambda obj: float(obj.distance_au))

        # Loga o objeto mais próximo com um nível de alerta para destaque
        logger.warning(
            f"ALERTA DE PROXIMIDADE: O objeto '{closest_object.designation}' "
            f"terá a maior aproximação em {closest_object.close_approach_date} "
            f"a uma distância de {closest_object.distance_au} UA.\n"
        )

        for obj in objects:
            print("-" * 30)
            print(f"Objeto: {obj.designation}")
            print(f"Data da Aproximação: {obj.close_approach_date}")
            print(f"Distância (UA): {obj.distance_au}")
            print(f"Velocidade Relativa (km/s): {obj.velocity_kms}")
    else:
        print("Não foi possível obter os dados.")
