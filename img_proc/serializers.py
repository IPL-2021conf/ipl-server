from rest_framework import serializers
from .models import ImgFaceModel, ImgProcModel
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