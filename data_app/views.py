from django.shortcuts import render
from rest_framework import viewsets 
from .models import VideoModel
from .serializers import VideoPostSerilizer, VideoSerializer
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import AccessToken
# Create your views here.

class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoModel.objects.all()
    serializer_class = VideoPostSerilizer
    
    filter_backends = [SearchFilter]
    search_fields = ('')

    def get_queryset(self):
        access_token = self.request.headers['Authorization'].replace('Bearer ', '')
        access_token = AccessToken(access_token)
        email = access_token.payload.get('email')
        print('email: ', email)
        videos = super().get_queryset()
        
        if self.request.user.is_authenticated:  #인증받은 사용자가 아니면 목록을 보이지 않음
            if self.request.user.is_superuser:  #superuser가 접속할경우엔 모든 글이 보임
                pass
            else:
                images = videos.filter(useremail=email)
        else:
            images = videos.none()
        return images  


# ============================================================
from .serializers import ImagePostSerializer
from .models import ImagePostModel
class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImagePostModel.objects.all()
    serializer_class = ImagePostSerializer

    filter_backends = [SearchFilter]
    search_fields = ('')

    def get_queryset(self):
        access_token = self.request.headers['Authorization'].replace('Bearer ', '')
        access_token = AccessToken(access_token)
        email = access_token.payload.get('email')
        print('email: ', email)
        images = super().get_queryset()
        if self.request.user.is_authenticated:  #인증받은 사용자가 아니면 목록을 보이지 않음
            if self.request.user.is_superuser:  #superuser가 접속할경우엔 모든 글이 보임
                pass
            else:
                images = images.filter(useremail=email)
        else:
            images = images.none()
        return images    

# ====================================================
