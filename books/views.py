# books/views.py
from bson.objectid import ObjectId
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .mongo_client import get_db, run_aggregation
from .serializers import BookSerializer


@swagger_auto_schema(
    method="get",
    operation_description="Retrieve a list of books, with pagination support.",
    responses={200: BookSerializer(many=True)},
    manual_parameters=[
        openapi.Parameter(
            "page",
            openapi.IN_QUERY,
            description="Page number",
            type=openapi.TYPE_INTEGER,
        )
    ],
)
@swagger_auto_schema(
    method="post",
    operation_description="Create a new book.",
    request_body=BookSerializer,
    responses={201: openapi.Response("Created", BookSerializer)},
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def book_list(request):
    db = get_db()
    if request.method == "GET":
        books = list(db.books.find().sort("published_date"))
        for book in books:
            book["_id"] = str(book["_id"])

        # Paginación
        page = request.GET.get("page", 1)
        paginator = Paginator(books, 10)  # 10 libros por página
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        serializer = BookSerializer(books, many=True)

        return Response(
            {
                "count": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "results": serializer.data,
            }
        )

    elif request.method == "POST":
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            result = db.books.insert_one(serializer.validated_data)
            return Response(str(result.inserted_id), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    operation_description="Retrieve a book by its ID.",
    responses={200: BookSerializer, 404: "Book not found"},
)
@swagger_auto_schema(
    method="put",
    operation_description="Update a book by its ID.",
    request_body=BookSerializer,
    responses={200: BookSerializer, 400: "Invalid data", 404: "Book not found"},
)
@swagger_auto_schema(
    method="delete",
    operation_description="Delete a book by its ID.",
    responses={204: "No Content", 404: "Book not found"},
)
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    db = (
        get_db()
    )  # Asumiendo que `get_db()` devuelve una conexión a la base de datos MongoDB

    try:
        book = db.books.find_one({"_id": ObjectId(pk)})
        if not book:
            return Response(status=status.HTTP_404_NOT_FOUND)

        book["_id"] = str(book["_id"])

        if request.method == "GET":
            return Response(book)

        elif request.method == "PUT":
            serializer = BookSerializer(instance=book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            db.books.delete_one({"_id": ObjectId(pk)})
            return Response(status=status.HTTP_204_NO_CONTENT)

    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    operation_description="Get the average price of books published in a specific year.",
    manual_parameters=[
        openapi.Parameter(
            "year",
            openapi.IN_QUERY,
            description="Year of publication",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    responses={
        200: openapi.Response(
            "OK",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "year": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "average_price": openapi.Schema(
                        type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT
                    ),
                },
            ),
        )
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def average_price_by_year(request, year):
    db = get_db()
    try:
        # Create pipeline
        pipeline = [
            {"$match": {"published_date": {"$regex": f"^{year}"}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}},
        ]
        result = list(db.books.aggregate(pipeline))

        if result:
            return Response(result[0], status=status.HTTP_200_OK)
        else:
            return Response({"average_price": 0}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
