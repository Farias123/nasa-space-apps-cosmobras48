from datetime import datetime
from astroquery.jplhorizons import Horizons
from astropy import units as u
import requests
import numpy as np


def _parse_date(date_string):
    return datetime.strptime(
        date_string.replace("A.D. ", "").split(".")[0], "%Y-%b-%d %H:%M:%S"
    )

def request_data_horizons_existing_body(planet_id, location, initial_date, end_date, step_size):
    res = Horizons(id=planet_id, location=location,
                   epochs={'start': initial_date, 'stop': end_date,
                           'step': step_size})
    return res

def request_data_horizons_solar_system(initial_date, end_date, step_size):
    """Request JPL horizons data for all planets of the solar system. Sun is fixed at (0,0,0)"""
    # initial_date, end_date format: yyyy-MM-dd
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

    data_planets = {
        "Sun": {"mass": 1_988_500e24, "radius": 695_700},
        "meta": {"units": {"radius": "km", "mass": "kg"}}
                    }
    for name_planet, id_planet in dict_planets.items():
        obj = request_data_horizons_existing_body(id_planet, center_body, initial_date, end_date, step_size)
        vec = obj.vectors()

        parsed_dates = [_parse_date(x) for x in vec.columns["datetime_str"]]
        data_planets[name_planet] = {
            "mass": mass_planets[name_planet],
            "radius": radius_planets[name_planet],
            "position_km": {
                "x": np.array(vec.columns["x"].to(u.km)),
                "y": np.array(vec.columns["y"].to(u.km)),
                "z": np.array(vec.columns["z"].to(u.km))
            },
            "velocity_km_s": {
                "vx": np.array(vec.columns["vx"].to(u.km / u.s)),
                "vy": np.array(vec.columns["vy"].to(u.km / u.s)),
                "vz": np.array(vec.columns["vz"].to(u.km / u.s))
            },
            "position_UA": {
                "x": np.array(vec.columns["x"]),
                "y": np.array(vec.columns["y"]),
                "z": np.array(vec.columns["z"])
            },
            "velocity_UA_D": {
                "vx": np.array(vec.columns["vx"]),
                "vy": np.array(vec.columns["vy"]),
                "vz": np.array(vec.columns["vz"])
            },
            "dates": parsed_dates,
        }

    return data_planets


def parse_date_line(time_line):
    parts = time_line.split('= ')
    return _parse_date(parts[1])

def parse_pos(pos_line):
    x = float(pos_line.split('X =')[1].split(' Y')[0])
    y = float(pos_line.split('Y =')[1].split(' Z')[0])
    z = float(pos_line.split('Z =')[1].strip())
    return [x, y, z]

def parse_speed(speed_line):
    vx = float(speed_line.split('VX=')[1].split(' VY')[0])
    vy = float(speed_line.split('VY=')[1].split(' VZ')[0])
    vz = float(speed_line.split('VZ=')[1].strip())
    return [vx, vy, vz]

def parse_other(other_line):
    lt = float(other_line.split('LT=')[1].split(' RG')[0])
    rg = float(other_line.split('RG=')[1].split(' RR')[0])
    rr = float(other_line.split('RR=')[1].strip())
    return [lt, rg, rr]

def format_vectors(vectors_string):
    vectors = vectors_string.split("\n")

    start = vectors.index("$$SOE") + 1
    end = vectors.index("$$EOE")

    vectors = vectors[start:end]
    n_steps = int(len(vectors) / 4)

    times = [None]*n_steps
    positions = np.zeros((n_steps, 3))
    speeds = np.zeros((n_steps, 3))
    others = np.zeros((n_steps, 3))

    for i, step in enumerate(range(0, len(vectors), 4)):
        times[i] = parse_date_line(vectors[step])
        positions[i] = parse_pos(vectors[step + 1])
        speeds[i] = parse_speed(vectors[step + 2])
        others[i] = parse_other(vectors[step + 3])

    return times, positions, speeds, others


def request_vectors_horizons_custom_body(start_time, stop_time, step_size, eccentricity, longitude_of_ascending_node,
                                         argument_of_perihelion, mean_anomaly, larger_semi_major_axis,
                                         orbital_inclination, object_name, EPOCH, FRAME):
    """

    Exemplo de entrada testada:
    start_time='2025-01-01', stop_time='2025-02-01', step_size='1 d', eccentricity=0.000151,
                                         longitude_of_ascending_node=-123.817587, argument_of_perihelion=305.152266,
                                         mean_anomaly=78.639573, larger_semi_major_axis=1.064364962718066,
                                         orbital_inclination=0.052376, object_name="Test",
                                         EPOCH="2451545.0", FRAME="J2000"



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
           f"EPOCH='{EPOCH}'EPHEM_TYPE='VECTORS'&START_TIME='{start_time}'&STOP_TIME='{stop_time}'"
           f"&STEP_SIZE='{step_size}'&OBJECT='{object_name}'&FRAME='{FRAME}'&EC='{eccentricity}'"
           f"&OM='{longitude_of_ascending_node}'&W='{argument_of_perihelion}'&MA='{mean_anomaly}'"
           f"&A='{larger_semi_major_axis}'&IN='{orbital_inclination}'")

    response = requests.get(url)

    if response.status_code == 200:
        res = response.text
        vectors_string = res.split("*******************************************************************************")[9]
        times, positions, speeds, others = format_vectors(vectors_string)
        x, y, z = positions[:,0], positions[:,1], positions[:,2]
        vx, vy, vz = speeds[:,0], speeds[:,1], speeds[:,2]
        data_bodies = {"x": x, "y": y, "z": z, "vx": vx, "vy": vy, "vz": vz, "dates": times}
        return data_bodies
    else:
        print("Error:", response.status_code)
        return f"Error with request: {response.text}, errorcode: {response.status_code}"


if __name__ == "__main__":
    res = request_data_horizons_solar_system("2015-04-04","2025-04-04","1 d")
    print()