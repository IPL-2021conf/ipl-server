from django.contrib import admin

from .models import ImgFaceModel, ImgProcModel

# Register your models here.
admin.site.register(ImgProcModel)
admin.site.register(ImgFaceModel)