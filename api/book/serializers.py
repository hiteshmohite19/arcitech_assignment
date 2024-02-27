from rest_framework.serializers import ModelSerializer

from .models import Book
from api.category.serializers import CategorySerializer
from api.users.serializers import UserBasicDetailsSerializer


class BooksSerializers(ModelSerializer):
    category = CategorySerializer
    author= UserBasicDetailsSerializer

    class Meta:
        model = Book
        fields = "__all__"
