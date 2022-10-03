FROM --platform=linux/arm64 python:3.10-slim

WORKDIR /app

RUN apt update
RUN apt install -y curl

ENV POETRY_HOME="/root/.poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$PATH:$POETRY_HOME/bin:/usr/local/bin"
RUN poetry config virtualenvs.create false

RUN curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.8/aws-lambda-rie-arm64 \
    && chmod 755 /usr/local/bin/aws-lambda-rie

COPY poetry.lock pyproject.toml ./

RUN  poetry install --no-root

COPY . .

ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
