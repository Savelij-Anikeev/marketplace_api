FROM python:3.10-alpine

COPY requirements.txt /temp/requirements.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/requirements.txt
RUN pip install django-storages[s3]
RUN adduser --disabled-password service-user

USER service-user


