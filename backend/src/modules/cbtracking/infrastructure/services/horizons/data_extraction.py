from loguru import logger
import numpy as np
import requests

from src.modules.cbtracking.infrastructure.services.horizons.definitions import (
    mass_planets,
    radius_planets,
    dict_planets,
    default_horizon_metadata,
    default_horizon_planets,
    center_body,
)

from src.modules.cbtracking.infrastructure.services.horizons.helpers import (
    format_vectors,
    parse_date,
    parse_dt_string,
    request_data_horizons_existing_body
)

from src.modules.cbtracking.infrastructure.services.horizons.models import (
    HorizonDataSolarSystemRequestParams,
    HorizonDataCustomBodyRequestParams,
)


def request_data_horizons_solar_system(params: HorizonDataSolarSystemRequestParams):
    """Request JPL horizons data for all planets of the solar system. Sun is fixed at (0,0,0)."""

    planet_name = params.planet_name

    if planet_name is None:
        data_planets = default_horizon_planets

        for name_planet, id_planet in dict_planets.items():
            obj = request_data_horizons_existing_body(id_planet, center_body, params.initial_date, params.end_date, params.step_size)
            vec = obj.vectors()

            parsed_dates = [parse_date(x) for x in vec.columns["datetime_str"]]
            data_planets.append({
                "body_name": name_planet,
                "horizon_data": {
                    "mass": mass_planets[name_planet],
                    "radius": radius_planets[name_planet],
                    "x": np.array(vec.columns["x"]).tolist(),
                    "y": np.array(vec.columns["y"]).tolist(),
                    "z": np.array(vec.columns["z"]).tolist(),
                    "vx": np.array(vec.columns["vx"]).tolist(),
                    "vy": np.array(vec.columns["vy"]).tolist(),
                    "vz": np.array(vec.columns["vz"]).tolist(),
                    "dates": [parse_dt_string(dt) for dt in parsed_dates],
                },
                "metadata": default_horizon_metadata,
            })

        return data_planets

    id_planet = dict_planets.get(planet_name.value)
    obj = request_data_horizons_existing_body(id_planet, center_body, params.initial_date, params.end_date, params.step_size)
    vec = obj.vectors()

    parsed_dates = [parse_date(x) for x in vec.columns["datetime_str"]]

    return {
        "body_name": params.planet_name.value,
        "horizon_data": {
            "mass": mass_planets[params.planet_name.value],
            "radius": radius_planets[params.planet_name.value],
            "x": np.array(vec.columns["x"]).tolist(),
            "y": np.array(vec.columns["y"]).tolist(),
            "z": np.array(vec.columns["z"]).tolist(),
            "vx": np.array(vec.columns["vx"]).tolist(),
            "vy": np.array(vec.columns["vy"]).tolist(),
            "vz": np.array(vec.columns["vz"]).tolist(),
            "dates": [parse_dt_string(dt) for dt in parsed_dates],
        },
        "metadata": default_horizon_metadata,
    }


"""
Exemplo de entrada testada:

Entradas:
    start_time='2025-01-01',
    stop_time='2025-02-01',
    step_size='1 d',
    eccentricity=0.000151,
    longitude_of_ascending_node=-123.817587,
    argument_of_perihelion=305.152266,
    mean_anomaly=78.639573,
    larger_semi_major_axis=1.064364962718066,
    orbital_inclination=0.052376,
    object_name="Test",
    EPOCH="2451545.0",
    FRAME="J2000".
"""

def request_vectors_horizons_custom_body(params: HorizonDataCustomBodyRequestParams):
    """Request JPL horizons data for a custom celestial body.

    Inputs:
        start_time	Data de início da efeméride (ex: '2024-10-01').
        stop_time	Data de término da efeméride (ex: '2024-10-02').
        step_size	Intervalo entre os pontos de dados (ex: '1 h').
        object_name	Nome de identificação do corpo celeste personalizado.
        FRAME	Sistema de referência para os vetores (ex: 'J2000' é um sistema inercial comum).
        EPOCH	Época dos elementos orbitais (data de referência no formato JD).
        A (larger_semi_major_axis) Semi-eixo maior da órbita (distância média, em UA).
        eccentricity	Excentricidade da órbita (0=círculo, 0-1=elipse, ≥1=parábola/hipérbole).
        IN (orbital_inclination) Inclinação orbital (ângulo entre o plano orbital e o plano de referência, em graus).
        OM (longitude_of_ascending_node) Longitude do nodo ascendente (orientação onde a órbita cruza o plano de referência, em graus).
        W (argument_of_perihelion) Argumento do periélio (orientação da órbita em seu próprio plano, em graus).
        MA (mean_anomaly) Anomalia média (posição do corpo na órbita na época, em graus).
    """

    url = ("https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='%3B'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&"
           f"EPOCH='{params.epoch}'EPHEM_TYPE='VECTORS'&START_TIME='{params.start_time}'&STOP_TIME='{params.stop_time}'"
           f"&STEP_SIZE='{params.step_size}'&OBJECT='{params.object_name}'&FRAME='{params.frame}'&EC='{params.eccentricity}'"
           f"&OM='{params.longitude_of_ascending_node}'&W='{params.argument_of_perihelion}'&MA='{params.mean_anomaly}'"
           f"&A='{params.larger_semi_major_axis}'&IN='{params.orbital_inclination}'")

    response = requests.get(url)

    if response.status_code == 200:
        res = response.text

        vectors_string = res.split("*******************************************************************************")[9]

        times, positions, speeds, _ = format_vectors(vectors_string)
        x, y, z = positions[:,0], positions[:,1], positions[:,2]
        vx, vy, vz = speeds[:,0], speeds[:,1], speeds[:,2]

        data_bodies = {
            "horizon_data": {
                "x": x.tolist(),
                "y": y.tolist(),
                "z": z.tolist(),
                "vx": vx.tolist(),
                "vy": vy.tolist(),
                "vz": vz.tolist(),
                "dates": [parse_dt_string(time) for time in times],
            },
            "metadata": default_horizon_metadata,
        }

        return data_bodies

    logger.error(f"Error with request: {response.text}, errorcode: {response.status_code}")

    return None
