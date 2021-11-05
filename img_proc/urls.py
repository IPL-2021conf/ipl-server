from django.urls import path
from .views import face_extrac_video, face_extract_img, img_processing, vdo_processing
urlpatterns = [
    path('image/', face_extract_img, name='img-face-extract'),
    path('image/mosaic/', img_processing, name='img-processing'),
    path('video/', face_extrac_video, name='vdo-face-extract'),
    path('video/mosaic/', vdo_processing, name='vdo-face-extract'),
]