FROM python:3.12.0
FROM a3-alpine3.17
MAINTAINER Mehran Motmaen

ENV PYTHONUNBUFFERD 1

COPY ./requirements.txt /requirements.txt
RUN apk update
RUN apk upgrade
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps


RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

