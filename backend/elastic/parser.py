import lxml.html
import requests
from multiprocessing import Pool
import re

def get_genres_info():
    response = requests.get('https://royallib.com/genres.html')
    tree = lxml.html.fromstring(response.text)
    genre_pages = tree.xpath('//a[starts-with(@href, "//royallib.com/genre/")]/@href')
    return genre_pages


def get_book_locations(genre):
    response = requests.get('https:' + genre)
    tree = lxml.html.fromstring(response.text)
    return tree.xpath('//a[starts-with(@href,"//royallib.com/book/")]/@href')


def parse_book(book_location):
    response = requests.get('https:' + book_location)
    tree = lxml.html.fromstring(response.text)
    book_info = {}
    book_info['author'] = tree.xpath('//a[preceding-sibling::b[contains(text(), "Автор:")]]/text()')
    book_info['title'] = ' '.join(tree.xpath('//td[./b[contains(text(),"Название:")]]/text()')).strip()
    book_info['year'] = ' '.join(tree.xpath('//td[./b[contains(text(),"Год издания:")]]/text()')).strip()
    book_info['annotation'] = ' '.join(tree.xpath('//td[./b[contains(text(),"Аннотация:")]]/text()')).strip()
    book_info['genre'] = tree.xpath('//a[preceding-sibling::b[contains(text(), "Жанр:")]]/text()')
    book_info = {k: v for k, v in book_info.items() if v}
    if 'author' in book_info.keys():
        book_info['author'] = book_info['author'][0]
    if 'genre' in book_info.keys():
        book_info['genre'] = book_info['genre'][0]
    if 'year' in book_info.keys():
        book_info['year'] = int(re.search(r'\d{4}', book_info['year']).group(0))
    return book_info


def parse(num_threads):
    genre_locations = get_genres_info()
    pool = Pool(processes=num_threads)
    book_locations = []
    for result in pool.imap_unordered(get_book_locations, genre_locations):
        book_locations.extend(result)
    for i in pool.imap_unordered(parse_book, book_locations):
        yield i