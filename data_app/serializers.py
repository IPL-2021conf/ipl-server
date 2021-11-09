from rest_framework import serializers
from .models import VideoModel, VideoPostModel
from .models import ImagePostModel, ImageModel
class ImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(use_url=True)
    class Meta:
        model = ImageModel
        fields = ['image',]

class ImagePostSerializer(serializers.ModelSerializer):    
    images = ImageSerializer(many=True, read_only=True)
    def create(self, validated_data):
        links = []
        images_data = self.context['request'].FILES
        post = ImagePostModel.objects.create(**validated_data)

        print('post:', images_data)
        for image in images_data.getlist('image'):
            image_obj = ImageModel.objects.create(post=post, image=image)
            # print("obj: ", image_obj.image)
            links.append('https://bucket-for-ipl.s3.amazonaws.com/'+str(image_obj.image))
        post.link = ','.join(str(link) for link in links)
        post.save()
        print("link: ", post.link)        
        return post
    class Meta:
        model = ImagePostModel
        fields = ['useremail', 'username', 'date', 'desc', 'images', 'link', ]

# ============================================================

class VideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=True)
    class Meta:
        model = VideoModel
        fields = ['video',]
class VideoPostSerilizer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    def create(self, validated_data):
        links=[]
        videos_data = self.context['request'].FILES
        post = VideoPostModel.objects.create(**validated_data)
        for video in videos_data.getlist('video'):
            video_obj = VideoModel.objects.create(post=post, video=video)
            links.append('https://bucket-for-ipl.s3.amazonaws.com/'+str(video_obj.video))
        post.link = ','.join(str(link) for link in links)
        post.save()
        print("link: ", post.link)
        return post
    class Meta:
        model = VideoPostModel
        fields = ['useremail', 'username', 'date', 'desc', 'videos', 'link', ]

