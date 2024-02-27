from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

from uuid import uuid4

# Create your models here.


class UserManager(BaseUserManager):

    def create_superuser(self, email, mobile_no, password, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        self.create_user(email, mobile_no, password, **kwargs)

    def create_user(self, email, mobile_no, password=None, **kwargs):
        user = self.model(
            email=self.normalize_email(email), mobile_no=mobile_no, **kwargs
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
    email = models.EmailField(blank=False, unique=True, null=False)
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
    is_superuser = models.BooleanField(default=False)

    user_manager = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "mobile_no"]

    def __str__(self):
        return self.email
