import factory
from .users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = "john@gmail.com"
    full_name = "John Doe"
    password="John@Doe"
    mobile_no = "9898989898"
    pincode = "400001"
    is_active=True
    is_superuser = True
    is_admin=True
