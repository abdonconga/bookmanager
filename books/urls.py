# books/urls.py
from django.urls import path

from .views import average_price_by_year, book_detail, book_list

urlpatterns = [
    path("books/", book_list, name="book_list"),
    path("books/<str:pk>/", book_detail, name="book_detail"),
    path(
        "books/average-price/<int:year>/",
        average_price_by_year,
        name="average_price_by_year",
    ),
]
