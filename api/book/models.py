from django.db import models
from django.core.validators import FileExtensionValidator
from uuid import uuid4
from django.utils.text import slugify
from api.users.models import User
from api.category.models import Category

# Create your models here.


class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(max_length=30, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=50,blank=True)
    body = models.TextField(max_length=300, blank=False, null=False)
    summary = models.CharField(max_length=60, blank=False, null=False)
    pdf_book = models.FileField(
        upload_to="pdf_book/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["pdf"])],
    )
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ManyToManyField(Category)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self):
        for field in self._meta.fields:
            if field.name == "file":
                field.upload_to = f"pdf_book/{self.category}/"
        self.slug = slugify(str(self.title))
        super().save()
