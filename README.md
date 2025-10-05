#  1. nasa-space-apps-cosmobras48

Plataforma web para monitoramento e simulação de corpos celestes no nosso sistema solar.

## 1.1. TOC

- [1. nasa-space-apps-cosmobras48](#1-nasa-space-apps-cosmobras48)
  - [1.1. TOC](#11-toc)
  - [1.2. Preliminares](#12-preliminares)
  - [1.3. Topologia do projeto (WiP)](#13-topologia-do-projeto-wip)
  - [1.4. Quick reference](#14-quick-reference)
    - [1.4.1. Instalação inicial de dependências](#141-instalação-inicial-de-dependências)
      - [1.4.1.1. Backend](#1411-backend)
      - [1.4.1.2. Frontend](#1412-frontend)
  - [1.5. Manipulação do projeto](#15-manipulação-do-projeto)
  - [1.6. Startup](#16-startup)
  - [1.7. Shutdown](#17-shutdown)
  - [1.8. TL;DR](#18-tldr)
  - [1.9. O que deseja fazer?](#19-o-que-deseja-fazer)

## 1.2. Preliminares

Esse projeto foi desenvolvido utilizando as seguintes ferramentas:

- Python, versão 3.12.9 ou superior:
    - UV Package Manager: Consome os arquivos [`pyproject.toml`](./pyproject.toml) e [`uv.lock`](./uv.lock) para instalar as dependências. Instruções para a instalação do gerenciador encontram-se [aqui](https://docs.astral.sh/uv/getting-started/installation/);
- Node.js, versão 22.13.0 ou superior:
    - [Node Version Manager (`nvm`)](https://github.com/nvm-sh/nvm): v2.2.17 ou superior;
    - [PNPM Package Manager (`pnpm`)](https://pnpm.io/pt/): v10.17.1 ou superior;
- [Docker Engine](https://docs.docker.com/engine/install/ubuntu/): v28.0.1 ou superior:
    - [Comando `docker` sem ser `sudo`](https://docs.docker.com/engine/install/linux-postinstall/). Opcional;
    - [Docker Compose](https://docs.docker.com/compose/install/linux/): v2.29.7-desktop.1 ou superior;
- [GNU Make](https://www.gnu.org/software/make/): v4.3 ou superior.


## 1.3. Topologia do projeto (WiP)

A plataforma de software consiste de serviços, orquestrados via Docker Compose, declarados em um [manifesto](./infra/docker/compose.yml) YML. Os mesmos são:

- `backend`: Um servidor de aplicação HTTP (back-end), escrito em Python, expondo uma API RESTful construída usando FastAPI;
- `frontend`: Uma interface de usuário (front-end), escrita em TypeScript, rodando sobre Node.js, utilizando a biblioteca Vite.js para construção de componentes;
- `database`: Um servidor de banco de dados não-relacional MongoDB;
- `mongo-express`: Um serviço para monitoramento e manipulação do banco de dados, acessível pelo navegador (Mongo Express)

> [!IMPORTANT]
> Por questões de restrição de tempo, o serviço `database` não foi integrado ao `backend`, de modo a implementar os casos de uso associados à manipulação do dashboard de monitoramento de asteróides (e.g. favoritação de cards por usuário, etc.). Com efeito, o cerne do projeto (a base de código usada para gerar a demo submetidda) encontra-se em `backend`;
> 
> A interface de usuario em `frontend` está funcional, porém não integrada com a API RESTful servida por `backend`, pelo mesmo motivo.


Segue abaixo uma representação esquemática:

![topology](./resources/docs/images/docker-topology.png)

## 1.4. Quick reference

### 1.4.1. Instalação inicial de dependências

#### 1.4.1.1. Backend

Para criar o ambiente virtual Python localmente, na versão correta, via UV, execute no terminal: 

```bash
cd backend                                  # Ir para a raíz correta
uv python install 3.12                      # Instala a versão correta do Python
uv venv --python 3.12                       # Cria o diretório ".venv"
source ./venv/bin/activate                  # Monta o virtualenv
uv pip install -r pyproject.toml            # Instala dependência de projeto
```

De modo a gerenciar pacotes individualmente, basta executar na raíz do projeto,

```bash
uv --project backend/pyproject.toml [add | remove] [package-name]           # Instala (ou remove) package de produção
uv --project backend/pyproject.toml [add | remove] --dev [package-name]     # Instala (ou remove) package de desenvolvimento
```

#### 1.4.1.2. Frontend

Para criar uma instalação local de dependências do Node.js, basta executar os seguintes comandos, na raíz do projeto:

```bash
nvm install lts && npm i -g pnpm@latest     # Instala a versão LTS do Node.js e também o gerenciador de pacotes PNPM
pnpm --prefix frontend install              # Instala as dependências de projeto
```

De modo a gerenciar pacotes individualmente, basta executar na raíz do projeto,

```bash
pnpm --prefix frontend [add | remove] [package-name] # Instala (ou remove) pacotes
```


## 1.5. Manipulação do projeto

Através do `make`, via scripts de automação do Docker Compose implementados em um [Makefile](./Makefile), na raíz do projeto. Para conferir a documentação de cada script, basta executar no terminal

```bash
make                                # Sem nenhum comando, executa o fallback 'help'
make help                           # Explicitamente, mostra a documentação
```

## 1.6. Startup

Considerando uma instalação inicial, na raíz do projeto, execute os seguintes comandos:

```bash
$ make build                                    # Realiza o build das imagens de todos os serviços, em ./infra/docker/[nome-do-serviço]/Dockerfile
$ make start c=database                         # Inicia o container do MongoDB
$ make start c=mongo-express                    # Inicia o container do Mongo Express
$ make start c=frontend                         # Inicia o container do frontend
$ make start c=backend                          # Inicia o container do backend
```

> [!NOTE]
> Para se certificar de que as imagens foram geradas pelo processo de build, basta executar o comando `docker image ls`.
> 
> Para se certificar de que os contêineres foram de fato devidamente iniciados e na escuta das portas corretas, basta executar o comando `make ps `.
> 
> Para ver os logs de um conteiner específico, execute `make logs c=[nome-do-serviço]`.


> [!IMPORTANT]
> A documentação da API RESTful pode ser acessada, via browser, em [`http://localhost:8001/api/docs`](http://localhost:8001/api/docs).
> 
> A interface de usuario em `frontend` está funcional, porém não integrada com a API RESTful servida por `backend`.


## 1.7. Shutdown

Similarmente, para ambos os ambientes, de modo a encerrar a execução de todos os contêineres, basta rodar:

```bash
make stop           # Interrompe todos os contêineres
make clean          # Opcional. Remove os contêineres e a network associadas aos serviços do ambiente
```


## 1.8. TL;DR

A equipe [Cosmobras-48](https://www.spaceappschallenge.org/2025/find-a-team/cosmobras-48/?tab=members) é composta por:

- **Damares do Socorro Gonçalves Gaia** (`@damaresgaia`) - frontend
- **Giordano Bruno Ribeiro Chaves Alves** (`@gio_alves`) - backend/integrações/simulações
- **Guilherme Lima Gonçalves** (`@lwglg`) - backend/integrações
- **Henrique de Lima Schweitzer** (`@henrique.schweitzer`) - backend/simulações
- **Vitor Costa Farias** (`@vcfarias` - _Team Owner_) - backend/simulações

Qualquer esclarecimento acerca do projeto pode ser feito entrando em contato com os mesmos.

--- 

## 1.9. O que deseja fazer?

- [Voltar ao topo](#11-toc)
