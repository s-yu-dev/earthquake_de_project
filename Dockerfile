FROM apache/airflow:2.10.3-python3.11

USER airflow

RUN pip install poetry poetry-plugin-export

COPY pyproject.toml poetry.lock /opt/airflow/
WORKDIR /opt/airflow

RUN poetry export --format=requirements.txt --without-hashes --without dev > requirements.txt

# sed replaces everything after '==' with nothing.
# s3fs==2024.6.1 => s3fs
RUN sed -i 's/==.*$//' requirements.txt

# 3. Устанавливаем зависимости.
# Now pip sees just "s3fs", looks at constraints.txt and installs the version that is guaranteed to work with Airflow 2.10.3.
RUN pip install -r requirements.txt --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.3/constraints-3.11.txt"
