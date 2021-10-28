from django.shortcuts import render
from rest_framework import viewsets 
from .models import VideoModel
from .serializers import VideoSerializer
from rest_framework.filters import SearchFilter
# Create your views here.

class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoModel.objects.all()
    serializer_class = VideoSerializer
    pass


# ============================================================
from .serializers import ImagePostSerializer
from .models import ImagePostModel
class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImagePostModel.objects.all()
    serializer_class = ImagePostSerializer

    filter_backends = [SearchFilter]
    search_fields = ('')

    def get_queryset(self):
        images = super().get_queryset()
        
        if self.request.user.is_authenticated:  #인증받은 사용자가 아니면 목록을 보이지 않음
            if self.request.user.is_superuser:  #superuser가 접속할경우엔 모든 글이 보임
                pass
            else:
                images = images.filter(useremail=self.request.name)
        else:
            images = images.none()
        return images    