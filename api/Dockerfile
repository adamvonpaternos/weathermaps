FROM python:3.10.1-buster AS shared

LABEL maintainer="Adam von Paternos" \
    name="weathermaps"

ENV DEBIAN_FRONTEND=noninteractive \
    DEBCONF_NONINTERACTIVE_SEEN=true

RUN apt-get update && \
    apt-get install -y --no-install-suggests --no-install-recommends \
    build-essential \
    dumb-init \
    software-properties-common && \
    apt-get clean

ENV POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.1.12 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -o /tmp/get-poetry.py && \
    python /tmp/get-poetry.py
ENV PATH=$POETRY_HOME/bin:$PATH

WORKDIR /usr/local/share/apps/weathermaps

COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-dev --no-root
COPY src/ src/
RUN poetry install --no-dev


FROM shared AS app
LABEL env="prod"

RUN useradd -m -s /bin/bash runner

RUN chown -R runner:runner .

USER runner

CMD ["/usr/bin/dumb-init", "--", "uvicorn", "weathermaps.main:app", "--host", "0.0.0.0", "--port", "80"]

FROM shared AS test
LABEL env="unit-test"

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
