FROM apache/airflow:2.10.3-python3.11

ARG POETRY_VERSION=2.2.1

USER airflow

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} poetry-plugin-export

COPY pyproject.toml poetry.lock /opt/airflow/
WORKDIR /opt/airflow

RUN poetry export --format=requirements.txt --without-hashes --without dev > requirements.txt \
    # sed replaces everything after '==' with nothing.
    # s3fs==2024.6.1 => s3fs
    && sed -i 's/==.*$//' requirements.txt \
    # Now pip sees just "s3fs", looks at constraints.txt and installs the version that is guaranteed to work with Airflow 2.10.3.
    && pip install --no-cache-dir -r requirements.txt --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.3/constraints-3.11.txt" \
    && rm requirements.txt
