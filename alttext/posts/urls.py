from django.urls import path
from .views import *

app_name="posts"
urlpatterns = [
    path('', shop, name="shop"),
]