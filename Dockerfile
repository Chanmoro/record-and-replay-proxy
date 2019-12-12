FROM python:3.7.4-stretch

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

RUN pip install poetry
RUN poetry config settings.virtualenvs.create false

ADD ./pyproject.toml /app/pyproject.toml
ADD ./poetry.lock /app/poetry.lock
WORKDIR /app
RUN poetry install

ADD . /app

ENV PATH $PATH:/app/bin
ENV RESPONSE_DATA_DIR /app/response_data