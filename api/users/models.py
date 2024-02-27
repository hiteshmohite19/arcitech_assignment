from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

from uuid import uuid4
# Create your models here.


class UserManager(BaseUserManager):

    def create_superuser(
        self, email, username, mobile_no, first_name, password, **kwargs
    ):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_admin", True)

        self.create_user(email, username, mobile_no, first_name, password, **kwargs)

    def create_user(
        self, email, username, mobile_no, first_name, password=None, **kwargs
    ):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            mobile_no=mobile_no,
            first_name=first_name,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user


def password_validator(password):

    import re

    if not re.fullmatch(r"[A-Za-z0-9]{8,}", password):
        raise "Password must contain min 8 length, 1 uppercase, 1lowercase"


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.CharField(blank=False, unique=True)
    mobile_no = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100, blank=False)
    password = models.CharField(validators=[password_validator])
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=10, null=False, blank=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    user_manager = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email", "full_name"]

    def __str__(self):
        return self.email
