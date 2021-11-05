from rest_framework import serializers
from .models import ImgFaceModel, ImgProcModel, VdoFaceModel, VdoProcModel
class ImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(use_url=True)
    class Meta:
        model = ImgProcModel
        fields = ['image',]

class FaceImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(use_url=True)
    class Meta:
        model = ImgFaceModel
        fields = ['image',]

class VideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=True)
    class Meta:
        model = VdoProcModel
        fields = ['video',]

class FaceVideoSerializer(serializers.ModelSerializer):
    video_face = serializers.FileField(use_url=True)
    class Meta:
        model = VdoFaceModel
        fields = ['video_face',]