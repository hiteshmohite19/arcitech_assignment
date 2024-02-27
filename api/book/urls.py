from django.urls import path

from .views import *

urlpatterns = [
    path("", Books.as_view({"post": "books"})),
    path("/<str:id>", Books.as_view({"get": "get_book"})),
    path("", Books.as_view({"post": "add_book"})),
    path("/<str:id>", Books.as_view({"put": "update_book"})),
]
