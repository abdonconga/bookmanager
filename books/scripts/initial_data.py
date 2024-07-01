# books/scripts/initial_data.py

from django.conf import settings
from pymongo import MongoClient


def run():
    client = MongoClient(settings.MONGO_DB_URI)
    db = client[settings.MONGO_DB_NAME]

    books = [
        {
            "title": "Book One",
            "author": "Author One",
            "published_date": "2018-5-17",
            "genre": "Fiction",
            "price": 19.99,
        },
        {
            "title": "Book Two",
            "author": "Author Two",
            "published_date": "2018-6-20",
            "genre": "Non-Fiction",
            "price": 29.99,
        },
        {
            "title": "Book Three",
            "author": "Author Three",
            "published_date": "2020-7-22",
            "genre": "Science Fiction",
            "price": 24.99,
        },
        {
            "title": "Book Four",
            "author": "Author Four",
            "published_date": "2019-8-15",
            "genre": "Fantasy",
            "price": 14.99,
        },
        {
            "title": "Book Five",
            "author": "Author Five",
            "published_date": "2021-9-10",
            "genre": "Mystery",
            "price": 21.99,
        },
        {
            "title": "Book Six",
            "author": "Author Six",
            "published_date": "2021-10-11",
            "genre": "Romance",
            "price": 31.19,
        },
        {
            "title": "Book Seven",
            "author": "Author Seven",
            "published_date": "2021-9-10",
            "genre": "BestSeller",
            "price": 11.90,
        },
        {
            "title": "Book Eight",
            "author": "Author Eight",
            "published_date": "2022-9-10",
            "genre": "BestSeller",
            "price": 11.90,
        },
        {
            "title": "Book Nine",
            "author": "Author Nine",
            "published_date": "2022-5-17",
            "genre": "Fiction",
            "price": 19.99,
        },
        {
            "title": "Book Ten",
            "author": "Author Ten",
            "published_date": "2022-6-20",
            "genre": "Non-Fiction",
            "price": 29.99,
        },
        {
            "title": "Book Eleven",
            "author": "Author Eleven",
            "published_date": "2022-7-22",
            "genre": "Science Fiction",
            "price": 24.99,
        },
        {
            "title": "Book Twelve",
            "author": "Author Twelve",
            "published_date": "2022-8-15",
            "genre": "Fantasy",
            "price": 14.99,
        },
    ]

    db.books.insert_many(books)
