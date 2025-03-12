# FROM python:3.10.12-slim-bookworm
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y software-properties-common curl gnupg && add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get -y install python3.13 python3-pip

# # Fix para Circutor
RUN sed -i 's/CipherString = DEFAULT:@SECLEVEL=2/CipherString = DEFAULT:@SECLEVEL=0/g' /etc/ssl/openssl.cnf

RUN  curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc

RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install pip --upgrade

RUN pip install -r requirements.txt

COPY . /app

CMD ["python3", "main.py"]
