from django.contrib import admin
from .models import ImagePostModel, ImageModel, VideoModel
# Register your models here.
admin.site.register(VideoModel)
admin.site.register(ImagePostModel)
admin.site.register(ImageModel)