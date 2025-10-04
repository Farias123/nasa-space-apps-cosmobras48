FROM python:3.12-slim

WORKDIR /app

COPY ./infra/docker/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./infra/docker/backend/ .

CMD ["python", "-u", "busca_dados_aproximacao_nasa.py"]
