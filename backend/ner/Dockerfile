FROM python:3

ENV PYTHON_VERSION=3.6
RUN apt-get update && apt-get install -y --no-install-recommends \
         python3-pip \
         build-essential \
         cmake \
         git \
         curl \
         wget \
         vim \
         ca-certificates &&\
     rm -rf /var/lib/apt/lists/*

COPY . /ner
WORKDIR /ner

EXPOSE 9301

RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
