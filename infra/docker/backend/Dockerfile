FROM python:3.12-slim

ENV WORKDIR=/home/cosmobras48/backend
ENV PYPROJECT_PATH=./backend/pyproject.toml
ENV UV_LOCK_PATH=./backend/uv.lock

# Installing dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update \
    && apt-get install -y \
        ffmpeg \
        libsm6 \
        libxext6

# Installing uv
COPY --from=ghcr.io/astral-sh/uv:0.6.1 /uv /uvx /bin/

# Change the working directory to the "backend" directory
WORKDIR ${WORKDIR}

# Installing dependencies
COPY ./backend/.python-version ./.python-version

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=${UV_LOCK_PATH},target=uv.lock \
    --mount=type=bind,source=${PYPROJECT_PATH},target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
COPY ./backend/src ./src
COPY ./resources/static ./static

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=${UV_LOCK_PATH},target=uv.lock \
    --mount=type=bind,source=${PYPROJECT_PATH},target=pyproject.toml \
    uv sync --locked

# Application entrypoint command
ENTRYPOINT [ "uv", "run" ]
