FROM python:3.8
LABEL maintainer="Tsatsu Adogla-Bessa Jnr"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

RUN pip install -r requirements.txt
ADD . /code/

