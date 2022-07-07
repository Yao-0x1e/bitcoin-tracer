FROM python:3.9.13-bullseye

COPY requirements.txt /tmp
RUN cd /tmp && pip3 install -r requirements.txt