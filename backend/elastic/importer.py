from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import RequestError
from parser import parse
from tqdm import tqdm

import argparse
import logging
import json
import glob
import os


def generate_books(threads):
    for book in tqdm(parse(threads)):
        if "text" in book:
            del book["text"]
        yield {"_type": "book", "_source": book}


def generate_books_from_local(folder):
    folder = os.path.normpath(folder)
    book_files = glob.glob(folder + "/[0-9]*.json")
    for book_file in book_files:
        with open(book_file) as f:
            book = json.load(f)
            if "text" in book:
                del book["text"]
            yield {"_type": "book", "_source": book}


logging.basicConfig(level=logging.INFO)

argparser = argparse.ArgumentParser(description="Import books data into elastic.")
argparser.add_argument(
    "threads", metavar="N", type=int, default=3, nargs="?", help="Number of threads."
)
argparser.add_argument(
    "--host", metavar="H", type=str, default="elasticsearch", help="elasticsearch host"
)
argparser.add_argument(
    "--local", metavar="F", type=str, default="data", help="local data folder"
)
argparser.add_argument(
    "--export",
    action="store_true",
    help="export books from site into --local folder end exit",
)
argparser.add_argument(
    "--offline", action="store_true", help="export books from --local folder"
)

args = argparser.parse_args()

if args.export:
    logging.info("Start exporting books.")
    parse_and_save(args.threads, args.local)
    exit()

es = Elasticsearch(hosts=args.host, request_timeout=180)

logging.info("Сhecking elastic availability.")
status = es.cluster.health(wait_for_status="yellow")
logging.info("Connected to %s with %s status", status["cluster_name"], status["status"])

# Load index settings.
logging.info("Start importing data...")
with open("./elastic-conf/index.json") as f:
    books_index_settings = json.load(f)

# Create books index.
logging.info("Checking and creating search index.")
try:
    es.indices.create(index="books-index", body=books_index_settings)
except RequestError as ex:
    if ex.error == "resource_already_exists_exception":
        logging.info("Index already exists, nothing to do.")
        exit()
    else:
        raise RequestError

# Adding books.
logging.info("Start adding books...")

if not args.offline:
    method = generate_books(args.threads)
else:
    method = generate_books_from_local(args.local)

success, errors = bulk(
    es, method, stats_only=True, index="books-index", chunk_size=10
)
logging.info("Performed %d actions and %d errors", success, errors)
