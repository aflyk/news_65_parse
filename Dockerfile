FROM python:3.12
WORKDIR /parse
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY poetry.lock .
COPY pyproject.toml .
RUN  pip install --upgrade setuptools pip \
     && pip install poetry --no-cache-dir \
     && poetry config virtualenvs.in-project true \
     && poetry install
COPY . .
RUN chmod +x run_news_parser.sh
ENTRYPOINT ["/parse/run_news_parser.sh"]
