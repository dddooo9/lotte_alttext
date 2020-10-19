from django.urls import path
from .views import *

app_name="posts"
urlpatterns = [
    path('', shop, name="shop"),
    path('A_01', A_01, name="A_01"),
]