from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from .views import *

app_name="posts"
urlpatterns = [
    path('', shop, name="shop"),
    path('detail/<int:id>', detail, name="detail"),
]