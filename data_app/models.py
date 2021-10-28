from django.db import models
from django.utils import timezone
# Create your models here.
# ============================================================
class ImagePostModel(models.Model):
    desc = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    username = models.CharField(max_length=30, null=False)
    useremail = models.EmailField(max_length=50, null=False)
    link = models.TextField(null=True, blank=True)
class ImageModel(models.Model):
    post = models.ForeignKey(ImagePostModel, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images')


class VideoPostModel(models.Model):
    desc = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    username = models.CharField(max_length=30, null=False)
    useremail = models.EmailField(max_length=50, null=False)
    link = models.TextField(null=True, blank=True)
class VideoModel(models.Model):
    post = models.ForeignKey(VideoPostModel, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos')

