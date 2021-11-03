from django.contrib import admin
from django.urls import path
from .views import img_processing
urlpatterns = [
    path('', img_processing, name='img-processing'),
]