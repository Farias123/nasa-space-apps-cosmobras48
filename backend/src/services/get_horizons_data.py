# https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY
from datetime import datetime
from astroquery.jplhorizons import Horizons

import numpy as np


def parse_date(date_string):
    return datetime.strptime(date_string.replace('A.D. ', '').split('.')[0],"%Y-%b-%d %H:%M:%S")


def request_horizons_data(initial_date, end_date, step_size):
    # initial_date, end_date format: yyyy-MM-dd
    center_body = "500@10" # Sun

    dict_planets = {"Mercury": 199, "Venus": 299, "Earth": 399, "Mars": 499, "Jupiter": 599, "Saturn": 699,
                    "Uranus": 799, "Neptune": 899}
    mass_planets = {"Mercury": 0.33010e24, "Venus": 4.8673e24, "Earth": 5.9722e24, "Mars": 0.64169e24, "Jupiter": 1898.13e24, "Saturn": 568.32e24,
                    "Uranus": 86.811e24, "Neptune": 102.409e24}
    radius_planets = {"Mercury": 2439.7, "Venus": 6051.8, "Earth": 6371, "Mars": 3389.5, "Jupiter": 69_911, "Saturn": 58_232,
                    "Uranus": 25_362, "Neptune": 24_622}

    data_planets = {"Sun": {"mass": 1_988_500e24, "radius": 695_700},
                    "meta": {"units": {"distance": "km", "mass": "kg", "velocity": "km/s"}}
                    }
    for name_planet, id_planet in dict_planets.items():
        obj = Horizons(id= id_planet, location= center_body,
                       epochs={'start': initial_date, 'stop': end_date,
                               'step': step_size})
        vec = obj.vectors()

        parsed_dates = [parse_date(x) for x in vec.columns["datetime_str"]]
        data_planets[name_planet] = {"mass": mass_planets[name_planet], "radius": radius_planets[name_planet],
                                     'x': np.array(vec.columns['x']), 'y': np.array(vec.columns['y']),
                                     'z': np.array(vec.columns['z']), "vx": np.array(vec.columns["vx"]),
                                     "vy": np.array(vec.columns["vy"]), "vz": np.array(vec.columns["vz"]),
                                     "dates": parsed_dates
                                     }

    return data_planets