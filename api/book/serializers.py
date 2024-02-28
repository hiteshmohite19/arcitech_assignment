from rest_framework.serializers import ModelSerializer, UUIDField

from .models import Book
from api.category.serializers import CategorySerializer
from api.users.serializers import UserBasicDetailsSerializer


class BooksSerializers(ModelSerializer):
    category = CategorySerializer
    author = UserBasicDetailsSerializer

    class Meta:
        model = Book
        fields = "__all__"


class BooksCreateSerializers(ModelSerializer):
    category = UUIDField()
    author = UUIDField()

    class Meta:
        model = Book
        fields = "__all__"
