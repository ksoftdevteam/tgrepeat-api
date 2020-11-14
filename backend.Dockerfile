FROM python:3.8


WORKDIR /backend

ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install poetry==1.0.10

COPY poetry.lock pyproject.toml credentials.json token.pickle ./

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --no-dev

COPY app /backend/app

ENV PYTHONPATH=/backend

EXPOSE 5000

CMD ["python", "app/application.py"]