# books/mongo_client.py
from django.conf import settings
from pymongo import MongoClient


def get_db():
    client = MongoClient(settings.MONGO_DB_URI)
    return client[settings.MONGO_DB_NAME]


def run_aggregation(db, pipeline):
    return list(db.books.aggregate(pipeline))
