FROM python:3.9.5-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip 

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]