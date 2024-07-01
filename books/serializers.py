# books/serializers.py
import datetime

from django.contrib.auth.models import User
from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    published_date = serializers.DateTimeField()
    genre = serializers.CharField(max_length=50)
    price = serializers.FloatField()
