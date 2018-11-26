FROM python:3
LABEL maintainer="gooppe"

ENV indexer.threads=4

COPY . /elastic-import/
COPY elasticsearch.yml /usr/share/elasticsearch/config/
WORKDIR /elastic-import
RUN pip install -r requirements.txt