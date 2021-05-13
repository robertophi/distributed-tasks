# syntax=docker/dockerfile:1
FROM python:3.9
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor

COPY requirements_publisher.txt /src/requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
WORKDIR /src
RUN pip install -r requirements.txt
COPY api api

EXPOSE 8000
# CMD ["/usr/bin/supervisord"]