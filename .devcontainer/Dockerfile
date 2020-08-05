FROM python:3.7-stretch

RUN apt update && apt install -y openjdk-8-jdk


RUN mkdir /workspace
WORKDIR /workspace
COPY requirements.txt /workspace/

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN rm requirements.txt