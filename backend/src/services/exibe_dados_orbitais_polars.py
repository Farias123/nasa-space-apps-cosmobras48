import requests
import re
import polars as pl
import plotly.graph_objects as go


def get_horizons_vectors(
    target: str, start_time: str, stop_time: str, step_size: str = "1d"
) -> pl.DataFrame | None:
    """Busca vetores de posição (X, Y, Z) da API HORIZONS da NASA usando Polars.

    Args:
        target: O nome ou ID do corpo celeste (ex: 'Apophis', '399' para Terra).
        start_time: Data de início no formato 'YYYY-MM-DD'.
        stop_time: Data de fim no formato 'YYYY-MM-DD'.
        step_size: O intervalo entre os pontos de dados (ex: '1d', '1mo', '1y').

    Returns:
        Um DataFrame do Polars com as coordenadas X, Y, Z ou None em caso de erro.

    """
    api_url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    params = {
        "format": "json",
        "COMMAND": target,
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "VECTORS",
        "CENTER": "@sun",
        "START_TIME": start_time,
        "STOP_TIME": stop_time,
        "STEP_SIZE": step_size,
        "VEC_TABLE": "2",
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "result" not in data:
            return None

        eph_text = data["result"]

        # Extrai as linhas de dados
        lines = eph_text.split("\n")

        # Encontra o início e o fim dos dados
        try:
            start_index = lines.index("$$SOE") + 1
            end_index = lines.index("$$EOE")
        except ValueError:
            return None

        data_lines = lines[start_index:end_index]

        # Processa os dados em blocos de 3 linhas
        records = []
        for i in range(0, len(data_lines), 3):
            line1 = data_lines[i]
            line2 = data_lines[i + 1]
            line3 = data_lines[i + 2]

            # Extrai JDTDB e CalendarDate
            dt_part, date_part = line1.split("=")
            jdt_db = float(dt_part.strip())
            calendar_date = date_part.replace("A.D.", "").strip()

            # Extrai X, Y, Z
            pos_values = re.findall(r"[-+]?\d*\.\d+E[-+]?\d+", line2)
            x, y, z = [float(v) for v in pos_values]

            # Extrai VX, VY, VZ
            vel_values = re.findall(r"[-+]?\d*\.\d+E[-+]?\d+", line3)
            vx, vy, vz = [float(v) for v in vel_values]

            records.append(
                {
                    "JDTDB": jdt_db,
                    "CalendarDate": calendar_date,
                    "X": x,
                    "Y": y,
                    "Z": z,
                    "VX": vx,
                    "VY": vy,
                    "VZ": vz,
                }
            )

        if not records:
            return None

        df = pl.DataFrame(records)

        # Converte km para AU
        au_km = 149597870.7
        for col_name in ["X", "Y", "Z"]:
            df = df.with_columns((pl.col(col_name) / au_km).alias(col_name))

        return df

    except requests.exceptions.RequestException:
        pass
    except Exception:
        pass

    return None


def plot_orbits_3d(trajectories: dict[str, pl.DataFrame], dates: pl.Series):
    """Plota múltiplas trajetórias em um gráfico 3D interativo a partir de dados Polars.

    Args:
        trajectories: Dicionário onde a chave é o nome do objeto e o valor é o DataFrame Polars.
        dates: Uma Série Polars com as datas da simulação para usar no slider.

    """
    initial_traces = []

    initial_traces.append(
        go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode="markers",
            marker={"color": "yellow", "size": 10, "symbol": "circle"},
            name="Sol",
        )
    )

    for name, df in trajectories.items():
        initial_traces.append(
            go.Scatter3d(
                x=df["X"].head(1).to_list(),
                y=df["Y"].head(1).to_list(),
                z=df["Z"].head(1).to_list(),
                mode="lines",
                line={"width": 3},
                name=f"Órbita {name}",
                uid=f"orbit-line-{name}",
            )
        )
        initial_traces.append(
            go.Scatter3d(
                x=df["X"].head(1).to_list(),
                y=df["Y"].head(1).to_list(),
                z=df["Z"].head(1).to_list(),
                mode="markers",
                marker={"size": 6},
                name=name,
                uid=f"orbit-marker-{name}",
            )
        )

    frames = []
    num_steps = len(dates)

    for k in range(num_steps):
        frame_data = []
        for name, df in trajectories.items():
            frame_data.append(
                go.Scatter3d(
                    x=df["X"].slice(0, k + 1).to_list(),
                    y=df["Y"].slice(0, k + 1).to_list(),
                    z=df["Z"].slice(0, k + 1).to_list(),
                    uid=f"orbit-line-{name}",
                )
            )
            frame_data.append(
                go.Scatter3d(
                    x=[df["X"][k]],
                    y=[df["Y"][k]],
                    z=[df["Z"][k]],
                    uid=f"orbit-marker-{name}",
                )
            )

        frames.append(go.Frame(data=frame_data, name=str(k)))

    fig = go.Figure(data=initial_traces, frames=frames)

    fig.update_layout(
        title="Simulação de Órbitas em 3D ao Redor do Sol (com Polars)",
        template="plotly_dark",
        scene={
            "xaxis_title": "X (UA)",
            "yaxis_title": "Y (UA)",
            "zaxis_title": "Z (UA)",
            "aspectmode": "data",
            "xaxis": {"range": [-2, 2]},
            "yaxis": {"range": [-2, 2]},
            "zaxis": {"range": [-2, 2]},
        },
        margin={"r": 20, "l": 10, "b": 10, "t": 40},
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 50, "redraw": False},
                                "fromcurrent": True,
                            },
                        ],
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top",
            }
        ],
        sliders=[
            {
                "steps": [
                    {
                        "method": "animate",
                        "args": [
                            [str(k)],
                            {
                                "frame": {"duration": 50, "redraw": False},
                                "mode": "immediate",
                            },
                        ],
                        "label": dates[k],
                    }
                    for k in range(num_steps)
                ],
                "transition": {"duration": 30},
                "x": 0.1,
                "xanchor": "left",
                "y": 0,
                "yanchor": "top",
            }
        ],
    )

    fig.show()


if __name__ == "__main__":
    # --- PARÂMETROS DE VERIFICAÇÃO ---
    # Foco na aproximação do Apophis em Abril de 2029
    start = "2029-04-10"
    end = "2029-04-16"
    step = "1h"  # Passo de 1 hora para alta resolução

    # Busca os dados para a Terra e para o asteroide Apophis com o formato de ID que funciona
    earth_df = get_horizons_vectors("399", start, end, step_size=step)
    apophis_df = get_horizons_vectors('"DES= 2099942;"', start, end, step_size=step)

    if (
        earth_df is not None
        and not earth_df.is_empty()
        and apophis_df is not None
        and not apophis_df.is_empty()
    ):
        # Calcula a distância entre a Terra e o Apophis para cada ponto no tempo
        distances = (
            (earth_df["X"] - apophis_df["X"]) ** 2
            + (earth_df["Y"] - apophis_df["Y"]) ** 2
            + (earth_df["Z"] - apophis_df["Z"]) ** 2
        ).sqrt()

        # Encontra a distância mínima e a data correspondente
        min_dist_au = distances.min()
        min_dist_km = min_dist_au * 149597870.7
        min_index = distances.arg_min()
        closest_date = earth_df["CalendarDate"][min_index]

    else:
        pass
