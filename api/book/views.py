from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from .models import Book
from .serializers import BooksSerializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.


class Books(ViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAdminUser, IsAuthenticated)

    def books(self, request):
        user = request.user.is_staff
        filter = request.data
        
        if IsAdminUser:
            filter["author"] = user
            print(2, filter)
            # books = Book.objects.filter(**request.filter)

        books = Book.objects.all().filter(**filter)
        
        serializer = BooksSerializers(books, many=True)
        books = serializer.data
        return Response(data=books, status=status.HTTP_200_OK)

    def get_book(self, request, id):

        user = request.email
        request = request.data
        if IsAdminUser:
            book = Book.objects.get(id=id).filter(**request.filter)
        elif IsAuthenticated:
            book = Book.objects.get(author__email=user, id=id).filter(**request.filter)
        else:
            pass  # redirect to all books
        if not book:
            return Response(data="No book found", status=status.HTTP_200_OK)
        serializer = BooksSerializers(book)
        book = serializer.data
        return Response(data=book, status=status.HTTP_200_OK)

    def add_book(self, request):
        return request
        book = request.data
        serializer = self.serializer(book)
        if not serializer.is_valid():
            return Response(
                {"success": False, "message": "Book data is in incorrect format"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()
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
