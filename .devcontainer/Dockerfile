FROM python:3.7-stretch

RUN apt update && apt install -y openjdk-8-jdk

RUN pip install --upgrade pip && pip install \
    pyspark==2.4.5 \
    pytest \
    setuptools \
    wheel \
    databricks-cli