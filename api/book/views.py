from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from .models import Book
from api.category.models import Category
from api.users.models import User
from .serializers import BooksSerializers, BooksCreateSerializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.


class Books(ViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def books(self, request):
        user = request.user
        filter = request.data

        if not user.is_superuser:
            filter["author"] = user

        books = Book.objects.all().filter(**filter)
        serializer = BooksSerializers(books, many=True)
        books = serializer.data
        return Response(data=books, status=status.HTTP_200_OK)

    def get_book(self, request, slug):

        user = request.user
        filter = {}
        filter["slug"] = slug
        if not user.is_superuser:
            filter["author"] = user.id

        book = get_object_or_404(Book, **filter)  # .filter(**filter)

        if not book:
            return Response(data="No book found", status=status.HTTP_200_OK)
        serializer = BooksSerializers(book, many=False)
        book = serializer.data
        return Response(data=book, status=status.HTTP_200_OK)

    def add_book(self, request):
        from uuid import UUID

        user = request.user
        book_data = request.data
        book = {
            "title": book_data["title"],
            "body": book_data["body"],
            "summary": book_data["summary"],
            "pdf_book": book_data["pdf_book"],
            "author": user.id,
        }

        user = User.objects.get(id=user.id)
        book['author']=user
        category = book_data["category"].split(',')
        categories = []
        for cat in category:
            categories.append(Category.objects.get(id=cat))


        book['category'] = categories
        serializer = BooksSerializers(data=book)

        return serializer.is_valid()

        book = Book.objects.create(**book)
        book.category.set(categories)

        return Response(
            {"success": True, "message": "Book saved"}, status=status.HTTP_201_CREATED
        )

    def update_book(self, request, id):

        user = request.email
        request = request.data

        book = self.books.filter(id=id)
        if IsAdminUser:
            pass
        elif IsAuthenticated and book["author"] != user:
            return Response(
                {"success": True, "message": "You cannot make changes to this book"},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            pass

        serializer = self.serializer(book)
        if not serializer.is_valid():
            return Response(
                {"success": False, "message": "Book data is in incorrect format"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()

        return Response(
            {"success": True, "message": "Book updated"}, status=status.HTTP_200_OK
        )
