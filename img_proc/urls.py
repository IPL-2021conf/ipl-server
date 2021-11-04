from django.urls import path
from .views import face_extract, img_processing
urlpatterns = [
    path('', face_extract, name='face-extract'),
    path('upload/', img_processing, name='img-processing'),
]