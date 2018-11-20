from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import RequestError
from parser import parse
from tqdm import tqdm

import argparse
import logging
import json


def generate_books(threads):
    for book in tqdm(parse(threads)):
        yield {
            '_type': 'book',
            '_source': book
        }


logging.basicConfig(level=logging.INFO)

argparser = argparse.ArgumentParser(
    description='Import books data into elastic.')
argparser.add_argument('threads', metavar='N', type=int, default=4,
                       nargs='?', help='Number of threads.')

args = argparser.parse_args()
es = Elasticsearch()

logging.info('Сhecking elastic availability.')
status = es.cluster.health(wait_for_status='yellow', request_timeout=180)
logging.info('Connected to %s with %s status',
             status['cluster_name'],
             status['status'])

# Load index settings.
logging.info('Start importing data...')
with open('./elastic-conf/index.json') as f:
    books_index_settings = json.load(f)

# Create books index.
logging.info('Checking and creating search index.')
try:
    es.indices.create(index="books-index", body=books_index_settings)
except RequestError as ex:
    if ex.error == 'resource_already_exists_exception':
        logging.info('Index already exists, nothing to do.')
        exit()
    else:
        raise RequestError

# Adding books.
logging.info('Start adding books...')
success, errors = bulk(es, generate_books(args.threads),
                       stats_only=True, index='books-index')
logging.info('Performed %d actions and %d errors', success, errors)
