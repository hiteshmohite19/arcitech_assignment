from rest_framework.serializers import ModelSerializer

from .models import User


class UsersSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserBasicDetailsSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "full_name"]
