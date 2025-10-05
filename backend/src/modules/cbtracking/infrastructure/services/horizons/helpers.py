from typing import Any, cast
from datetime import datetime

import numpy as np
from astroquery.jplhorizons import Horizons


def parse_date(date_string, format: str = "%Y-%b-%d %H:%M:%S"):
    """Parse datetime string to datetime object."""
    return datetime.strptime(
        date_string.replace("A.D. ", "").split(".")[0], format
    )


def parse_dt_string(dtobject: datetime | Any, format: str = "%Y-%b-%d %H:%M:%S"):
    """Parse datetime object into string."""
    sanitized = cast(datetime, dtobject) if type(dtobject).__name__ != 'datetime' else dtobject

    return cast(datetime, sanitized).strftime(format)


def parse_date_line(time_line):
    """Parse date line."""
    parts = time_line.split('= ')
    return parse_date(parts[1])


def parse_pos(pos_line):
    """Parse position line."""
    x = float(pos_line.split('X =')[1].split(' Y')[0])
    y = float(pos_line.split('Y =')[1].split(' Z')[0])
    z = float(pos_line.split('Z =')[1].strip())
    return [x, y, z]


def parse_speed(speed_line):
    """Parse speed data."""
    vx = float(speed_line.split('VX=')[1].split(' VY')[0])
    vy = float(speed_line.split('VY=')[1].split(' VZ')[0])
    vz = float(speed_line.split('VZ=')[1].strip())
    return [vx, vy, vz]


def parse_other(other_line):
    """Parse other kind of data."""
    lt = float(other_line.split('LT=')[1].split(' RG')[0])
    rg = float(other_line.split('RG=')[1].split(' RR')[0])
    rr = float(other_line.split('RR=')[1].strip())
    return [lt, rg, rr]


def format_vectors(vectors_string):
    """Format vector string."""
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


def request_data_horizons_existing_body(planet_id, location, initial_date, end_date, step_size):
    """Request data horizons from an existing body."""

    res = Horizons(
        id=planet_id,
        location=location,
        epochs={ 'start': initial_date, 'stop': end_date,'step': step_size }
    )

    return res

