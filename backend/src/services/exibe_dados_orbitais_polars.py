import requests
import re
import polars as pl
import plotly.graph_objects as go
from io import BytesIO
from typing import Optional, Dict

def get_horizons_vectors(target: str, start_time: str, stop_time: str) -> Optional[pl.DataFrame]:
    """
    Busca vetores de posição (X, Y, Z) da API HORIZONS da NASA usando Polars.

    Args:
        target: O nome ou ID do corpo celeste (ex: 'Apophis', '399' para Terra).
        start_time: Data de início no formato 'YYYY-MM-DD'.
        stop_time: Data de fim no formato 'YYYY-MM-DD'.

    Returns:
        Um DataFrame do Polars com as coordenadas X, Y, Z ou None em caso de erro.
    """
    api_url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    
    params = {
        'format': 'json',
        'COMMAND': target,
        'OBJ_DATA': 'NO',
        'MAKE_EPHEM': 'YES',
        'EPHEM_TYPE': 'VECTORS',
        'CENTER': '@sun',
        'START_TIME': start_time,
        'STOP_TIME': stop_time,
        'STEP_SIZE': '1d',
        'VEC_TABLE': '2',
    }

    try:
        print(f"Buscando dados de trajetória para: {target}...")
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'result' not in data:
            print(f"Erro: Resposta da API não contém a chave 'result' para {target}.")
            print(f"Resposta da API:\n---\n{data}\n---")
            return None

        eph_text = data['result']
        
        # Extrai as linhas de dados
        lines = eph_text.split('\n')
        
        # Encontra o início e o fim dos dados
        try:
            start_index = lines.index('$$SOE') + 1
            end_index = lines.index('$$EOE')
        except ValueError:
            print(f"Erro: Marcadores $$SOE/$$EOE não encontrados para {target}.")
            print(f"Resposta da API:\n---\n{eph_text}\n---")
            return None

        data_lines = lines[start_index:end_index]
        
        # Processa os dados em blocos de 3 linhas
        records = []
        for i in range(0, len(data_lines), 3):
            line1 = data_lines[i]
            line2 = data_lines[i+1]
            line3 = data_lines[i+2]

            # Extrai JDTDB e CalendarDate
            dt_part, date_part = line1.split('=')
            jdt_db = float(dt_part.strip())
            calendar_date = date_part.replace('A.D.', '').strip()

            # Extrai X, Y, Z
            pos_values = re.findall(r'[-+]?\d*\.\d+E[-+]?\d+', line2)
            x, y, z = [float(v) for v in pos_values]

            # Extrai VX, VY, VZ
            vel_values = re.findall(r'[-+]?\d*\.\d+E[-+]?\d+', line3)
            vx, vy, vz = [float(v) for v in vel_values]

            records.append({
                "JDTDB": jdt_db,
                "CalendarDate": calendar_date,
                "X": x,
                "Y": y,
                "Z": z,
                "VX": vx,
                "VY": vy,
                "VZ": vz,
            })

        if not records:
            print(f"Nenhum registro de efeméride encontrado para {target}.")
            return None

        df = pl.DataFrame(records)

        # Converte km para AU
        au_km = 149597870.7
        for col_name in ["X", "Y", "Z"]:
            df = df.with_columns((pl.col(col_name) / au_km).alias(col_name))
        
        print(f"Dados para {target} obtidos com sucesso!")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para {target}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao processar dados para {target}: {e}")
        
    return None

def plot_orbits_3d(trajectories: Dict[str, pl.DataFrame], dates: pl.Series):
    """
    Plota múltiplas trajetórias em um gráfico 3D interativo a partir de dados Polars.

    Args:
        trajectories: Dicionário onde a chave é o nome do objeto e o valor é o DataFrame Polars.
        dates: Uma Série Polars com as datas da simulação para usar no slider.
    """
    initial_traces = []

    initial_traces.append(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(color='yellow', size=10, symbol='circle'),
        name='Sol'
    ))

    for name, df in trajectories.items():
        initial_traces.append(go.Scatter3d(
            x=df['X'].head(1).to_list(), y=df['Y'].head(1).to_list(), z=df['Z'].head(1).to_list(),
            mode='lines',
            line=dict(width=3),
            name=f'Órbita {name}',
            uid=f'orbit-line-{name}'
        ))
        initial_traces.append(go.Scatter3d(
            x=df['X'].head(1).to_list(), y=df['Y'].head(1).to_list(), z=df['Z'].head(1).to_list(),
            mode='markers',
            marker=dict(size=6),
            name=name,
            uid=f'orbit-marker-{name}'
        ))

    frames = []
    num_steps = len(dates)

    for k in range(num_steps):
        frame_data = []
        for name, df in trajectories.items():
            frame_data.append(go.Scatter3d(
                x=df['X'].slice(0, k + 1).to_list(), 
                y=df['Y'].slice(0, k + 1).to_list(), 
                z=df['Z'].slice(0, k + 1).to_list(),
                uid=f'orbit-line-{name}'
            ))
            frame_data.append(go.Scatter3d(
                x=[df['X'][k]], 
                y=[df['Y'][k]], 
                z=[df['Z'][k]],
                uid=f'orbit-marker-{name}'
            ))

        frames.append(go.Frame(data=frame_data, name=str(k)))

    fig = go.Figure(data=initial_traces, frames=frames)

    fig.update_layout(
        title='Simulação de Órbitas em 3D ao Redor do Sol (com Polars)',
        template='plotly_dark',
        scene=dict(
            xaxis_title='X (UA)',
            yaxis_title='Y (UA)',
            zaxis_title='Z (UA)',
            aspectmode='data',
            xaxis=dict(range=[-2, 2]),
            yaxis=dict(range=[-2, 2]),
            zaxis=dict(range=[-2, 2]),
        ),
        margin=dict(r=20, l=10, b=10, t=40),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 50, "redraw": False}, "fromcurrent": True}])],
            direction="left", pad={"r": 10, "t": 87}, showactive=False, x=0.1, xanchor="right", y=0, yanchor="top"
        )],
        sliders=[dict(
            steps=[dict(method='animate', args=[[str(k)], {'frame': {'duration': 50, 'redraw': False}, 'mode': 'immediate'}], label=dates[k]) for k in range(num_steps)],
            transition={'duration': 30}, x=0.1, xanchor="left", y=0, yanchor="top"
        )]
    )
    
    print("\nExibindo simulação 3D. Você pode rotacionar, dar zoom e mover o gráfico!")
    fig.show()


if __name__ == "__main__":
    # Define o período da simulação
    start = '2024-01-01'
    end = '2025-01-01'

    # Busca os dados para a Terra e para o asteroide Apophis
    earth_df = get_horizons_vectors('399', start, end)
    apophis_df = get_horizons_vectors('Apophis;', start, end)

    if earth_df is not None and not earth_df.is_empty() and apophis_df is not None and not apophis_df.is_empty():
        # Monta o dicionário de trajetórias para plotagem
        orbits_to_plot = {
            'Terra': earth_df,
            'Asteroide Apophis': apophis_df
        }
        # Usa a segunda coluna (CalendarDate) para o slider.
        plot_orbits_3d(orbits_to_plot, earth_df.get_column("CalendarDate"))
    else:
        print("\nNão foi possível gerar a simulação devido a falha na obtenção dos dados.")
