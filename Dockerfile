FROM python:3.9

ENV PYTHONUNBUFFERED True

RUN apt-get update
RUN apt-get install -y node-npm

WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock package.json package-lock.json /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

RUN npm install

COPY CongressActivity/ CongressActivity

RUN npm run build

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 CongressActivity.app:app