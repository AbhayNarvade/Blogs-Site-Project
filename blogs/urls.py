from django.urls import path , include
from .views import *
urlpatterns = [
    path('create/', create_blog , name='create_blog' ),
]