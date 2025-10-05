import rebound
from scipy.integrate import solve_ivp
import numpy as np
from get_horizons_data import request_data_horizons_solar_system
from datetime import datetime


class NumericalSimulation:
    def full_period_simulation(
        self, mass_meteor, xi, yi, zi, vxi, vyi, vzi, initial_date, end_date, step_size
    ):
        solar_system_data = request_data_horizons_solar_system(
            f"{initial_date}", f"{end_date}", f"{step_size}"
        )

        initial_meteor_configuration = [xi, yi, zi, vxi, vyi, vzi]

        interval_subdivisions = len(solar_system_data["Mercury"]["x"])

        absolute_interval = (
            datetime.strptime(end_date, "%Y-%m-%d")
            - datetime.strptime(initial_date, "%Y-%m-%d")
        ).total_seconds()

        integration_interval = absolute_interval / interval_subdivisions

        full_meteor_configuration = []

        full_meteor_configuration.append(initial_meteor_configuration)

        meteor_dict = {}

        for step in range(interval_subdivisions):
            meteor_configuration = full_meteor_configuration[step]


            planets = [
                "Mercury",
                "Venus",
                "Earth",
                "Mars",
                "Jupiter",
                "Saturn",
                "Uranus",
                "Neptune",
            ]

            data = {
                p: {
                    "mass": solar_system_data[p]["mass"],
                    "x": solar_system_data[p]["x"][step],
                    "y": solar_system_data[p]["y"][step],
                    "z": solar_system_data[p]["z"][step],
                    "vx": solar_system_data[p]["vx"][step],
                    "vy": solar_system_data[p]["vy"][step],
                    "vz": solar_system_data[p]["vz"][step],
                }
                for p in planets
            }

            data["Sun"] = {
                    "mass": solar_system_data["Sun"]["mass"],
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "vx": 0,
                    "vy": 0,
                    "vz": 0,
                }

            # next_step = self.stepsize_simulation(data,mass_meteor,meteor_configuration,integration_interval,sun_mass)
            next_step = self.rgk_solver(
                meteor_configuration, data, integration_interval
            )

            full_meteor_configuration.append(next_step)

            date = solar_system_data["Mercury"]["dates"][step]

            meteor_dict[date] = {
                    "mass": mass_meteor,
                    "x": next_step[0],
                    "y": next_step[1],
                    "z": next_step[2],
                    "vx": next_step[3],
                    "vy": next_step[4],
                    "vz": next_step[5]
                }

        return meteor_dict, solar_system_data

    def acceleration(self, t, meteor_configuration, data):
        G = 6.6743e-17

        celestial_body = [
            "Sun",
            "Mercury",
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
            "Neptune",
        ]

        r = meteor_configuration[:3]
        v = meteor_configuration[3:]
        a = np.zeros(3)
        for p in celestial_body:
            r_planet = np.array([data[p]["x"], data[p]["y"], data[p]["z"]])
            diff = r_planet - r
            dist = np.abs(np.linalg.norm(diff))
            a += (G * float(data[p]["mass"]) / float(dist) ** 3) * diff
        return np.concatenate([v, a])

    def rgk_solver(self, meteor_configuration, data, integration_interval):
        numb_subdiv = 1
        t_eval = np.linspace(0, integration_interval, numb_subdiv)
        time_span = (0, integration_interval)
        sol = solve_ivp(
            self.acceleration,
            time_span,
            meteor_configuration,
            args=(data,),
            method="RK45",
            t_eval=t_eval,
        )

        return [
            sol.y[0][numb_subdiv - 1],
            sol.y[1][numb_subdiv - 1],
            sol.y[2][numb_subdiv - 1],
            sol.y[3][numb_subdiv - 1],
            sol.y[4][numb_subdiv - 1],
            sol.y[5][numb_subdiv - 1],
        ]

    def stepsize_simulation(
        self, data, mass, meteor_configuration, integration_interval, sun_mass
    ):
        x, y, z, vx, vy, vz = meteor_configuration

        sim = rebound.Simulation()
        sim.units = ("Km", "s", "Kg")

        sim.add(m=sun_mass)
        sim.add(
            m=data["Mercury"]["mass"],
            x=data["Mercury"]["x"],
            y=data["Mercury"]["y"],
            z=data["Mercury"]["z"],
            vx=data["Mercury"]["vx"],
            vy=data["Mercury"]["vy"],
            vz=data["Mercury"]["vz"],
        )
        sim.add(
            m=data["Venus"]["mass"],
            x=data["Venus"]["x"],
            y=data["Venus"]["y"],
            z=data["Venus"]["z"],
            vx=data["Venus"]["vx"],
            vy=data["Venus"]["vy"],
            vz=data["Venus"]["vz"],
        )
        sim.add(
            m=data["Mars"]["mass"],
            x=data["Mars"]["x"],
            y=data["Mars"]["y"],
            z=data["Mars"]["z"],
            vx=data["Mars"]["vx"],
            vy=data["Mars"]["vy"],
            vz=data["Mars"]["vz"],
        )
        sim.add(
            m=data["Jupiter"]["mass"],
            x=data["Jupiter"]["x"],
            y=data["Jupiter"]["y"],
            z=data["Jupiter"]["z"],
            vx=data["Jupiter"]["vx"],
            vy=data["Jupiter"]["vy"],
            vz=data["Jupiter"]["vz"],
        )
        sim.add(
            m=data["Saturn"]["mass"],
            x=data["Saturn"]["x"],
            y=data["Saturn"]["y"],
            z=data["Saturn"]["z"],
            vx=data["Saturn"]["vx"],
            vy=data["Saturn"]["vy"],
            vz=data["Saturn"]["vz"],
        )
        sim.add(
            m=data["Uranus"]["mass"],
            x=data["Uranus"]["x"],
            y=data["Uranus"]["y"],
            z=data["Uranus"]["z"],
            vx=data["Uranus"]["vx"],
            vy=data["Uranus"]["vy"],
            vz=data["Uranus"]["vz"],
        )
        sim.add(
            m=data["Neptune"]["mass"],
            x=data["Neptune"]["x"],
            y=data["Neptune"]["y"],
            z=data["Neptune"]["z"],
            vx=data["Neptune"]["vx"],
            vy=data["Neptune"]["vy"],
            vz=data["Neptune"]["vz"],
        )
        sim.add(
            m=data["Earth"]["mass"],
            x=data["Earth"]["x"],
            y=data["Earth"]["y"],
            z=data["Earth"]["z"],
            vx=data["Earth"]["vx"],
            vy=data["Earth"]["vy"],
            vz=data["Earth"]["vz"],
        )
        sim.add(m=mass, x=x, y=y, z=z, vx=vx, vy=vy, vz=vz)

        sim.integrator = "whfast"

        sim.dt = integration_interval / 100
        sim.ri_whfast.corrector = 17
        sim.ri_whfast.safe_mode = 0

        sim.integrate(integration_interval)

        sim.make_standard()

        comet = sim.particles[-1]

        daily_comet_configuration = [
            comet.x,
            comet.y,
            comet.z,
            comet.vx,
            comet.vy,
            comet.vz,
        ]

        return daily_comet_configuration


NumericalSimulation().full_period_simulation(
    1000,
    -1.310740060953714e8,
    1.05417337460535e8,
    -8.172569656297214e6,
    -2.703855870632367e1,
    -1.709143318766929e1,
    2.925250976523674e-2,
    "2015-04-04",
    "2025-04-04",
    "1d",
)
# NumericalSimulation().stepsize_simulation(solar_system_data,1000,-1.310740060953714e8, 1.05417337460535e8,-8.172569656297214e6,-2.703855870632367e1,-1.709143318766929e1, 2.925250976523674e-2)
# NumericalSimulation().two_body_orbit(3e-6, 1.496e8, 0, 0, 0, 9.39e8, 0)
# NumericalSimulation().horizon_api_simulation()
