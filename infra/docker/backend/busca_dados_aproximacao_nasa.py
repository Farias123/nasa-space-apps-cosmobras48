import requests
import json
import logging
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constantes
API_URL = "https://ssd-api.jpl.nasa.gov/cad.api"
DEFAULT_PARAMS = {
    'date-min': 'now',
    'date-max': '+60',
    'dist-max': '0.05',  # Distância máxima em unidades astronômicas (UA)
    'sort': 'date'       # Ordenar os resultados por data
}

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
            designation=item[0],
            close_approach_date=item[3],
            distance_au=item[4],
            velocity_kms=item[7]
        )

def get_nasa_close_approach_data() -> Optional[List[CloseApproachObject]]:
    """
    Busca dados de aproximação de objetos próximos à Terra na API da NASA.
    Retorna uma lista de objetos CloseApproachObject ou None em caso de erro.
    """
    try:
        logging.info("Fazendo a requisição para a API da NASA...")
        # Faz a requisição GET para a API com os parâmetros definidos
        response = requests.get(API_URL, params=DEFAULT_PARAMS)

        # Verifica se a requisição foi bem-sucedida (código de status 200)
        response.raise_for_status()

        logging.info("Requisição bem-sucedida!")
        # Converte a resposta JSON em um dicionário Python
        data: Dict[str, Any] = response.json()

        count: int = data.get('count', 0)
        logging.info(f"Encontrados {count} objetos com aproximação nos próximos 60 dias.")

        if not data.get('data'):
            logging.warning("Nenhum dado de aproximação encontrado para os critérios especificados.")
            return []
        
        return [CloseApproachObject.from_list(item) for item in data['data']]

    except requests.exceptions.RequestException as e:
        logging.error(f"Ocorreu um erro ao fazer a requisição para a API: {e}")
    except json.JSONDecodeError:
        logging.error("Ocorreu um erro ao decodificar a resposta JSON.")
    
    return None

if __name__ == "__main__":
    objects = get_nasa_close_approach_data()
    if objects:
        for obj in objects:
            print("-" * 30)
            print(f"Objeto: {obj.designation}")
            print(f"Data da Aproximação: {obj.close_approach_date}")
            print(f"Distância (UA): {obj.distance_au}")
            print(f"Velocidade Relativa (km/s): {obj.velocity_kms}")
    else:
        print("Não foi possível obter os dados.")
