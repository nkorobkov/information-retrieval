FROM python:3
LABEL maintainer="gooppe"

ENV indexer.threads=4

COPY . /elastic-import/
WORKDIR /elastic-import
RUN pip install -r requirements.txt