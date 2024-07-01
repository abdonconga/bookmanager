# books/tests.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from books.mongo_client import get_db, run_aggregation


class BookTests(APITestCase):

    def setUp(self):
        """
        Create a user, authenticate, and insert test books into MongoDB.
        """
        # Create a user and authenticate
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Insert some test books into the MongoDB
        self.db = get_db()
        self.book_data = [
            {
                "title": "Book One",
                "author": "Author One",
                "published_date": "2029-05-17",
                "genre": "Fiction",
                "price": 19.99,
            },
            {
                "title": "Book Two",
                "author": "Author Two",
                "published_date": "2021-06-20",
                "genre": "Non-Fiction",
                "price": 29.99,
            },
            {
                "title": "Book Three",
                "author": "Author Three",
                "published_date": "2029-07-22",
                "genre": "Science Fiction",
                "price": 24.99,
            },
        ]
        self.db.books.insert_many(self.book_data)

    def tearDown(self):
        """
        Clean up the MongoDB collection after each test.
        """
        for book in self.book_data:
            self.db.books.delete_one(
                {
                    "title": book["title"],
                    "author": book["author"],
                    "published_date": book["published_date"],
                }
            )

        # self.db.books.delete_many({})

    def test_book_list(self):
        """
        Ensure we can retrieve the list of books.
        """
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(response.data["results"][0]["title"], "Book One")

    def test_book_list_pagination(self):
        """
        Ensure pagination works correctly.
        """
        url = reverse("book_list") + "?page=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 10
        )  # We have 10 books, 10 per page

    def test_average_price_by_year(self):
        """
        Ensure the average price is calculated correctltest_average_price_by_year_no_booksy for a given year.
        """
        url = reverse("average_price_by_year", args=[2029])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["average_price"], (19.99 + 24.99) / 2)

    def test_average_price_by_year_no_books(self):
        """
        Ensure the average price is 0 if no books were published in the given year.
        """
        url = reverse("average_price_by_year", args=[2030])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["average_price"], 0)

    def test_average_price_by_year_authentication_required(self):
        """
        Ensure the view requires authentication.
        """
        self.client.credentials()  # Remove authentication
        url = reverse("average_price_by_year", args=[2020])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
