# syntax=docker/dockerfile:1
FROM python:3.9
RUN apt-get update

COPY requirements_consumer.txt /src/requirements.txt

WORKDIR /src
RUN pip install -r requirements.txt
COPY consumerB consumerB

# CMD celery -A consumerA.consumer worker --loglevel=debug -Q consumer.A --without-gossip --without-mingle --without-heartbeat --autoscale 1,1