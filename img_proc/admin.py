from django.contrib import admin

from .models import ImgFaceModel, ImgProcModel, VdoFaceModel, VdoProcModel

# Register your models here.
admin.site.register(ImgProcModel)
admin.site.register(ImgFaceModel)
admin.site.register(VdoProcModel)
admin.site.register(VdoFaceModel)