FROM python:3.12.0a3-alpine3.17
MAINTAINER Mehran Motmaen

ENV PYTHONUNBUFFERD 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

