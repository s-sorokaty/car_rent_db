FROM python:3.12-slim
WORKDIR /script

# install system dependencies
RUN apt-get update \
  && apt-get clean \
# install poetry
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

# install python dependencies
COPY poetry.lock pyproject.toml /script/
RUN poetry install --no-root