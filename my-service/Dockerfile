FROM python:3.12-slim

WORKDIR /my-service

# Install make and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y make && \
    rm -rf /var/lib/apt/lists/*

# We have only one process, install packages globally
ENV POETRY_VIRTUALENVS_CREATE=false

ENV SERVICE_PORT=9000

COPY Makefile poetry.lock pyproject.toml ./

RUN make install/prod

COPY . .

EXPOSE ${SERVICE_PORT}

CMD ["make", "run"]