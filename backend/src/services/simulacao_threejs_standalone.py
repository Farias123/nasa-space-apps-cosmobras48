import requests
import re
import polars as pl
import json
import random

from orbit_simulation import simulate_fictional_asteroid

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

        lines = eph_text.split("\n")

        try:
            start_index = lines.index("$$SOE") + 1
            end_index = lines.index("$$EOE")
        except ValueError:
            return None

        data_lines = lines[start_index:end_index]

        records = []
        for i in range(0, len(data_lines), 3):
            line1 = data_lines[i]
            line2 = data_lines[i + 1]
            line3 = data_lines[i + 2]

            dt_part, date_part = line1.split("=")
            jdt_db = float(dt_part.strip())
            calendar_date = date_part.replace("A.D.", "").strip()

            pos_values = re.findall(r"[-+]?\d*\.\d+E[-+]?\d+", line2)
            x, y, z = [float(v) for v in pos_values]

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

        au_km = 149597870.7
        for col_name in ["X", "Y", "Z"]:
            df = df.with_columns((pl.col(col_name) / au_km).alias(col_name))

        return df

    except requests.exceptions.RequestException:
        pass
    except Exception:
        pass

    return None


def plot_orbits_3d_threejs(
    trajectories: dict[str, pl.DataFrame],
    output_filename: str = "orbit_simulation.html",
):
    """Gera um arquivo HTML com uma simulação 3D interativa das órbitas usando three.js.

    Args:
        trajectories: Dicionário onde a chave é o nome do objeto e o valor é o DataFrame Polars
                      com as colunas 'X', 'Y', 'Z' e 'CalendarDate'.
        output_filename: O nome do arquivo HTML a ser gerado.

    """
    plot_data = {}
    max_steps = 0
    # Encontra o número máximo de passos entre todas as trajetórias primeiro
    for _, df in trajectories.items():
        if not df.is_empty():
            max_steps = max(max_steps, len(df))

    for name, df in trajectories.items():
        if df.is_empty():
            continue

        # Adiciona a lista de datas para CADA objeto
        plot_data[name] = {
            "x": df["X"].to_list(),
            "y": df["Y"].to_list(),
            "z": df["Z"].to_list(),
            "dates": df["CalendarDate"].to_list(),  # Adiciona datas individuais
            "startDate": df["CalendarDate"][0] if not df.is_empty() else None,
            "color": df["color"][0],
            "size": df["size"][0],
            "type": df["type"][0],
            "close_approach_date": df["close_approach_date"][0] if "close_approach_date" in df.columns else None,
            "magnitude": df["magnitude"][0] if "magnitude" in df.columns else None,
            "velocity_kms": df["velocity_kms"][0] if "velocity_kms" in df.columns else None,
        }

    if not plot_data or max_steps == 0:
        return

    json_data = json.dumps(plot_data, indent=2)

    html_template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulação de Órbita 3D com Three.js</title>
    <style>
        body {{ margin: 0; background-color: #000; color: #fff; font-family: sans-serif; overflow: hidden; }}
        canvas {{ display: block; }}
        #info-panel {{
            position: absolute; top: 10px; left: 10px;
            background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px;
        }}
        #target-info-panel {{
            position: absolute; top: 10px; right: 10px;
            background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px;
            display: none; /* Começa oculto */
        }}
        #controls {{
            position: absolute; bottom: 20px; left: 50%;
            transform: translateX(-50%); display: flex; align-items: center;
            background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px;
        }}
        #controls button, #controls input, #controls label {{ margin: 0 10px; }}
        .label {{
            color: #FFF;
            font-family: sans-serif;
            padding: 2px 5px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none; /* Para não interferir com os controles do mouse */
        }}
    </style>
</head>
<body>
    <div id="info-panel">
        <h2>Simulação de Órbita</h2>
        <div id="date-display">Data:</div>
    </div>

    <div id="target-info-panel">
        <h3 id="target-name"></h3>
        <p>
            <span id="target-close-approach-label">Maior Aproximação: </span>
            <a href="#" id="target-close-approach-date" style="color: #87CEFA; text-decoration: underline;"></a>
        </p>
        <p id="target-magnitude"></p>
        <p id="target-velocity"></p>
        <p id="target-distance-earth"></p>
    </div>

    <div id="controls">
        <button id="play-pause-btn">Play</button>
        <label for="timeline-slider">Timeline:</label>
        <input type="range" id="timeline-slider" min="0" max="{max_steps - 1}" value="0" step="1" style="width: 300px;">
    </div>

    <script type="importmap">
    {{
        "imports": {{
            "three": "https://unpkg.com/three@0.159.0/build/three.module.js",
            "three/addons/": "https://unpkg.com/three@0.159.0/examples/jsm/"
        }}
    }}
    </script>

    <script type="module">
        import * as THREE from 'three';
        import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
        import {{ CSS2DRenderer, CSS2DObject }} from 'three/addons/renderers/CSS2DRenderer.js';

        const simData = {json_data};

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.01, 1000);
        camera.position.set(1.8, 1.8, 1.8);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Renderizador para as etiquetas de texto (labels)
        const labelRenderer = new CSS2DRenderer();
        labelRenderer.setSize(window.innerWidth, window.innerHeight);
        labelRenderer.domElement.style.position = 'absolute';
        labelRenderer.domElement.style.top = '0px';
        labelRenderer.domElement.style.pointerEvents = 'none'; // Permite que cliques passem através do container de labels
        document.body.appendChild(labelRenderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        const sunGeometry = new THREE.SphereGeometry(0.05, 32, 32);
        const sunMaterial = new THREE.MeshBasicMaterial({{ color: 0xffff00 }});
        const sun = new THREE.Mesh(sunGeometry, sunMaterial);
        scene.add(sun);

        scene.add(new THREE.AmbientLight(0x606060));

        const celestialObjects = {{}};

        for (const name in simData) {{
            if (name === 'dates') continue;

            const bodyData = simData[name];
            const color = bodyData.color;

            const bodyGeometry = new THREE.SphereGeometry(bodyData.size, 20, 20);
            const bodyMaterial = new THREE.MeshBasicMaterial({{ color: color }});
            const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
            body.userData = {{ name: name, type: bodyData.type }}; // Armazena dados para o clique
            scene.add(body);

            // Cria a etiqueta com o nome do corpo celeste
            const labelDiv = document.createElement('div');
            labelDiv.className = 'label';
            labelDiv.textContent = name;
            labelDiv.style.color = new THREE.Color(color).getStyle();

            const nameLabel = new CSS2DObject(labelDiv);
            nameLabel.position.set(0, 0.03, 0); // Desloca um pouco acima do objeto
            body.add(nameLabel); // Anexa a etiqueta ao corpo celeste

            // Cria a geometria da órbita com todos os pontos
            const orbitPoints = [];
            for(let i=0; i < bodyData.x.length; i++) {{
                orbitPoints.push(new THREE.Vector3(bodyData.x[i], bodyData.y[i], bodyData.z[i]));
            }}
            const orbitGeometry = new THREE.BufferGeometry().setFromPoints(orbitPoints);
            const orbitMaterial = new THREE.LineBasicMaterial({{ color: color, opacity: 0.5, transparent: true }});
            const orbit = new THREE.Line(orbitGeometry, orbitMaterial);

            // Órbitas de asteroides começam invisíveis
            if (bodyData.type === 'asteroid') {{
                orbit.visible = false;
            }}
            scene.add(orbit);

            celestialObjects[name] = {{ body, orbit, data: bodyData }};
        }}

        const playPauseBtn = document.getElementById('play-pause-btn');
        const slider = document.getElementById('timeline-slider');
        const dateDisplay = document.getElementById('date-display');
        
        const targetInfoPanel = document.getElementById('target-info-panel');
        const targetName = document.getElementById('target-name');
        const targetDistanceEarth = document.getElementById('target-distance-earth');
        const targetCloseApproachDate = document.getElementById('target-close-approach-date');
        const targetMagnitude = document.getElementById('target-magnitude');
        const targetVelocity = document.getElementById('target-velocity');

        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        // Converte a data de início da simulação principal para um objeto Date
        const simStartDate = new Date(simData['Terra'].dates[0].split(' ')[0]);
        const oneDay = 1000 * 60 * 60 * 24; // Milissegundos em um dia

        let currentStep = 0;
        let isPlaying = false;
        let targetToFollow = null; // Variável para guardar o nome do objeto a ser seguido

        function updateScene(step) {{
            currentStep = Math.max(0, Math.min(step, {max_steps - 1}));
            slider.value = currentStep;

            // Atualiza a data usando a Terra como referência, se disponível
            if (simData['Terra'] && simData['Terra'].dates[currentStep]) {{
                dateDisplay.textContent = 'Data: ' + simData['Terra'].dates[currentStep];
            }}

            for (const name in celestialObjects) {{
                const obj = celestialObjects[name];
                const data = obj.data;

                // Calcula o deslocamento (offset) para este objeto
                const bodyStartDate = new Date(data.startDate.split(' ')[0]);
                const offsetDays = Math.round((bodyStartDate - simStartDate) / oneDay);
                
                // Calcula o índice correto para este objeto, considerando o offset
                const stepForObject = currentStep - offsetDays;

                if (stepForObject < 0 || stepForObject >= data.x.length) continue; // Pula se estiver fora do intervalo de dados

                const x = data.x[stepForObject];
                const y = data.y[stepForObject];
                const z = data.z[stepForObject];
                obj.body.position.set(x, y, z);
            }}

            // Atualiza o painel de informações do alvo, se houver um
            if (targetToFollow && celestialObjects[targetToFollow]) {{
                const targetObj = celestialObjects[targetToFollow];
                const earthObj = celestialObjects['Terra'];

                if (targetObj && earthObj) {{
                    const distance = targetObj.body.position.distanceTo(earthObj.body.position);
                    // Converte de AU para km para exibição
                    const distanceKm = (distance * 149597870.7).toLocaleString('pt-BR', {{ maximumFractionDigits: 0 }});
                    const distanceAu = distance.toFixed(4);
                    targetDistanceEarth.textContent = 'Distância Terra: ' + distanceAu + ' AU (' + distanceKm + ' km)';
                }}
            }} else {{
                // Esconde o painel se não houver alvo
                targetInfoPanel.style.display = 'none';
            }}
        }}

        playPauseBtn.addEventListener('click', () => {{
            isPlaying = !isPlaying;
            playPauseBtn.textContent = isPlaying ? 'Pause' : 'Play';
        }});

        slider.addEventListener('input', (e) => {{
            isPlaying = false;
            playPauseBtn.textContent = 'Play';
            updateScene(parseInt(e.target.value));
        }});

        function onMouseClick(event) {{
            // Normaliza as coordenadas do mouse
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(scene.children);

            for (let i = 0; i < intersects.length; i++) {{
                const clickedObject = intersects[i].object;
                if (clickedObject.userData.type === 'asteroid') {{
                    const clickedName = clickedObject.userData.name;
                    const wasVisible = celestialObjects[clickedName].orbit.visible;

                    // Primeiro, esconde todas as órbitas de asteroides
                    for (const name in celestialObjects) {{
                        if (celestialObjects[name].data.type === 'asteroid') {{
                            // Esconde a órbita
                            celestialObjects[name].orbit.visible = false;
                            // Se não for o clicado, esconde o corpo também
                            if (name !== clickedName) {{
                                celestialObjects[name].body.visible = false; // Esconde o corpo
                                celestialObjects[name].body.children[0].visible = false; // Esconde a etiqueta
                            }}
                        }}
                    }}

                    // Define ou limpa o alvo a ser seguido
                    if (wasVisible) {{
                        targetToFollow = null; // Clicou no mesmo de novo, para de seguir e esconde o painel
                        targetInfoPanel.style.display = 'none';
                        // Mostra todos os asteroides novamente
                        for (const name in celestialObjects) {{
                            if (celestialObjects[name].data.type === 'asteroid') {{
                                celestialObjects[name].body.visible = true; // Mostra o corpo
                                celestialObjects[name].body.children[0].visible = true; // Mostra a etiqueta
                            }}
                        }}
                    }} else {{
                        celestialObjects[clickedName].orbit.visible = true; // Mostra a órbita do clicado
                        targetToFollow = clickedName; // Define novo alvo
                        // Mostra e atualiza o painel de informações
                        const targetData = celestialObjects[clickedName].data;
                        const approachDate = targetData.close_approach_date;
                        targetName.textContent = clickedName;
                        targetMagnitude.textContent = 'Magnitude Absoluta (H): ' + targetData.magnitude;
                        targetVelocity.textContent = 'Velocidade Relativa: ' + targetData.velocity_kms + ' km/s';
                        targetCloseApproachDate.textContent = approachDate;
                        targetCloseApproachDate.dataset.date = approachDate; // Armazena a data para o clique
                        targetInfoPanel.style.display = 'block';
                    }}
                    break; // Para após encontrar o primeiro asteroide
                }}
            }}
        }}

        targetCloseApproachDate.addEventListener('click', (e) => {{
            e.preventDefault(); // Impede que o link '#' navegue
            const jumpDateStr = e.target.dataset.date;
            if (!jumpDateStr) return;

            // Encontra o índice correspondente na linha do tempo principal (da Terra)
            const targetIndex = simData['Terra'].dates.findIndex(d => d.startsWith(jumpDateStr));

            if (targetIndex !== -1) {{
                // Para a animação e pula para a data
                isPlaying = false;
                playPauseBtn.textContent = 'Play';
                updateScene(targetIndex);
                console.log('Pulando para a data: ' + jumpDateStr + ' (índice: ' + targetIndex + ')');
            }}
        }});

        function animate() {{
            requestAnimationFrame(animate);

            if (isPlaying) {{
                let nextStep = currentStep + 1;
                if (nextStep >= {max_steps}) {{
                    nextStep = 0; // Reinicia a animação
                }}
                updateScene(nextStep);
            }}

            // Lógica para seguir o alvo
            if (targetToFollow && celestialObjects[targetToFollow]) {{
                const targetObject = celestialObjects[targetToFollow];
                const targetPosition = targetObject.body.position;

                // Calcula a posição desejada da câmera (um pouco atrás e acima)
                const desiredPosition = new THREE.Vector3().copy(targetPosition).add(new THREE.Vector3(0.3, 0.3, 0.3));

                // Move suavemente a câmera e o ponto de foco
                camera.position.lerp(desiredPosition, 0.05);
                controls.target.lerp(targetPosition, 0.05);
            }}

            controls.update();
            renderer.render(scene, camera);
            labelRenderer.render(scene, camera); // Renderiza as etiquetas
        }}

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            labelRenderer.setSize(window.innerWidth, window.innerHeight);
        }});

        // Se o usuário interagir com os controles, para de seguir o objeto
        controls.addEventListener('start', () => {{
            targetToFollow = null;
            // Mostra todos os asteroides novamente
            for (const name in celestialObjects) {{
                if (celestialObjects[name].data.type === 'asteroid') {{
                    celestialObjects[name].body.visible = true; // Mostra o corpo
                    celestialObjects[name].body.children[0].visible = true; // Mostra a etiqueta
                }}
            }}
            targetInfoPanel.style.display = 'none';
        }});

        window.addEventListener('click', onMouseClick);
        updateScene(0);
        animate();
    </script>
</body>
</html>
"""

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_template)
    except OSError:
        pass


def _calculate_asteroid_size_from_magnitude(h: float) -> float:
    """
    Calcula um tamanho de esfera para a simulação a partir da magnitude absoluta (H) do asteroide.
    A fórmula D(km) = 1329 / 10^(0.2*H) estima o diâmetro.
    Esta função mapeia esse diâmetro para uma escala visualmente apropriada para a simulação.
    Quanto menor 'h', maior o asteroide.

    Args:
        h: A magnitude absoluta do asteroide.

    Returns:
        O raio da esfera para a simulação.
    """
    if h is None:
        return 0.005  # Tamanho padrão mínimo

    # Mapeia a magnitude para um tamanho. Ajuste os valores para um melhor resultado visual.
    # Magnitudes menores (objetos maiores) resultarão em esferas maiores.
    return max(0.005, 0.1 / (h**2))


def get_asteroid_targets(end_date_str: str) -> dict:
    """Busca uma lista de asteroides que farão aproximação da Terra (fly-by).

    usando a API JPL Small-Body Database.

    Args:
        end_date_str: A data final para a busca de aproximações, no formato 'YYYY-MM-DD'.

    Returns:
        Um dicionário de alvos de asteroides.

    """
    # Busca por asteroides com futuras aproximações da Terra
    api_url = f"https://ssd-api.jpl.nasa.gov/cad.api?dist-max=0.05AU&date-min={start_date}now&date-max={end_date_str}&sort=dist&limit=200"
    asteroid_targets = {}

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if "data" not in data or not data["data"]:
            return {}

        # O campo 'des' (designation) é o nome do asteroide.
        # O campo 'fullname' pode conter caracteres que a API HORIZONS não gosta.
        for item in data["data"]:
            designation = item[0]  # Campo 'des'
            close_approach_date_str = item[3]  # Campo 'cd' (calendar date)
            velocity_kms = item[7]  # Campo 'v_rel'
            magnitude = float(item[8]) if item[8] else None  # Campo 'h'

            target_id = f'"DES={designation};"'  # Formata o ID para a API HORIZONS

            # Calcula o tamanho com base na magnitude e gera uma cor aleatória
            size = _calculate_asteroid_size_from_magnitude(magnitude)
            asteroid_targets[designation] = {
                "id": target_id,
                "close_approach_date": close_approach_date_str.split(" ")[
                    0
                ],  # Pega apenas a parte YYYY-MM-DD
                "color": random.randint(0x888888, 0xFFFFFF),  # Cores claras
                "size": size,
                "type": "asteroid",
                "velocity_kms": velocity_kms,
                "magnitude": magnitude,
            }

        return asteroid_targets

    except requests.exceptions.RequestException:
        return {}


def get_closest_approach_target(days_ahead: int = 60) -> dict:
    """Busca o único objeto com a maior aproximação da Terra em um determinado período.

    Args:
        days_ahead: O número de dias no futuro para buscar a aproximação.

    Returns:
        Um dicionário contendo o alvo de maior aproximação, ou um dicionário vazio.

    """
    api_url = "https://ssd-api.jpl.nasa.gov/cad.api"
    params = {
        "date-min": "now",
        "date-max": f"+{days_ahead}",
        "dist-max": "0.05AU",
        "sort": "dist",  # Ordena pelo mais próximo primeiro
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" not in data or not data["data"]:
            return {}

        # Como a API já está ordenada por distância ('sort=dist'), o primeiro item é o mais próximo.
        closest_item = data["data"][0]
        designation = closest_item[0]  # Campo 'des' (designation)
        target_id = f'"DES={designation};"' # Formata o ID para a API HORIZONS

        return {
            designation: {
                "id": target_id,
                "color": 0xFF00FF,
                "size": 0.012,
                "type": "asteroid",
            }  # Cor magenta para destaque
        }
    except requests.exceptions.RequestException:
        return {}


if __name__ == "__main__":
    # --- PARÂMETROS DA SIMULAÇÃO ---
    from datetime import datetime, timedelta
    start_date = "2025-01-01" # Data de início da simulação
    end_date = "2035-10-01"  # Data final da simulação
    output_file = "simulacao_orbita_threejs.html"

    # --- PARÂMETROS DO ASTEROIDE FICTÍCIO ---
    # Defina aqui os dados iniciais do seu asteroide para simular a colisão
    # As coordenadas (x,y,z) e velocidades (vx,vy,vz) devem estar em km e km/s
    fictional_asteroid_params = {
        "name": "Meteoro Fictício",
        "initial_conditions": {
            "radius": 0.5, # em km
            "mass": 1e9, # em kg
            # Posição inicial (exemplo: perto da órbita de Marte)
            "x": -2.2e8, "y": 0, "z": 0,
            # Velocidade inicial (exemplo: em direção à Terra)
            "vx": 20, "vy": 20, "vz": 0,
        },
        "display": {
            "color": 0xFF4500, # Laranja avermelhado
            "size": 0.02,
            "type": "asteroid",
        }
    }

    # Calcula a trajetória do asteroide fictício
    print(f"Calculando trajetória para '{fictional_asteroid_params['name']}'...")
    df_fictional = simulate_fictional_asteroid(
        fictional_asteroid_params["initial_conditions"],
        start_date,
        end_date,
        "1d" # Usando passo diário para a simulação
    )

    # 1. Define os alvos principais (planetas)
    all_targets = {
        "Mercurio": {"id": "199", "color": 0x8C8C8C, "size": 0.015, "type": "planet"},
        "Venus": {"id": "299", "color": 0xD8A868, "size": 0.02, "type": "planet"},
        "Terra": {"id": "399", "color": 0x00AAFF, "size": 0.022, "type": "planet"},
        "Marte": {"id": "499", "color": 0xFF5733, "size": 0.018, "type": "planet"},
        "Jupiter": {"id": "599", "color": 0xC99039, "size": 0.04, "type": "planet"},
        "Saturno": {"id": "699", "color": 0xE3D9B1, "size": 0.035, "type": "planet"},
        "Urano": {"id": "799", "color": 0xA2E465, "size": 0.03, "type": "planet"},
        "Netuno": {"id": "899", "color": 0x3F54BA, "size": 0.03, "type": "planet"},
        "Plutao": {"id": "999", "color": 0xBFB5A6, "size": 0.01, "type": "planet"},
    }

    # 2. Busca dinamicamente os asteroides com aproximação da Terra
    print("Buscando asteroides com aproximação da Terra...")
    asteroid_targets = get_asteroid_targets(end_date)
    all_targets.update(asteroid_targets)

    # Adiciona o asteroide fictício ao dicionário de alvos se a simulação foi bem-sucedida
    if df_fictional is not None and not df_fictional.is_empty():
        print(f"'{fictional_asteroid_params['name']}' adicionado à simulação.")
        trajectories_data = {
            fictional_asteroid_params['name']: {
                "dataframe": df_fictional,
                **fictional_asteroid_params['display']
            }
        }

    # --- EXECUÇÃO ---
    print(f"Iniciando busca de dados para {len(all_targets)} corpos celestes...")
    trajectories_data = {}
    
    for name, params in all_targets.items():
        # Busca os dados para todos os corpos usando o mesmo período de simulação geral.
        print(f"  - Buscando dados para '{name}' de {start_date} a {end_date}")
        df = get_horizons_vectors(
            params["id"], start_date, end_date, step_size="1d"
        )

        if df is not None and not df.is_empty():
            trajectories_data[name] = { # Adiciona os dados dos corpos reais
                "dataframe": df,
                "color": params["color"],
                "size": params["size"],
                "type": params["type"],
                "close_approach_date": params.get("close_approach_date"), # Adiciona a data de aproximação
                "velocity_kms": params.get("velocity_kms"),
                "magnitude": params.get("magnitude"),
            }

    if trajectories_data:
        plot_input = {
            name: data["dataframe"].with_columns(
                pl.lit(data["color"]).alias("color"), pl.lit(data["size"]).alias("size")
            )
            .with_columns(pl.lit(data["type"]).alias("type"))
            .with_columns(
                pl.lit(data["close_approach_date"]).alias("close_approach_date")
            )
            .with_columns(pl.lit(data["velocity_kms"]).alias("velocity_kms"))
            .with_columns(
                pl.lit(data["magnitude"]).alias("magnitude")
            )
            for name, data in trajectories_data.items() 
        }
        plot_orbits_3d_threejs(plot_input, output_file)
        print(f"\nSimulação gerada com sucesso! Abra o arquivo: {output_file}")
    else:
        print("Nenhum dado de trajetória foi obtido. A simulação não foi gerada.")
