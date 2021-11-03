from django.db import models

# Create your models here.
class ImgProcModel(models.Model):
    image = models.FileField(upload_to='imgproc')
    
class ImgFaceModel(models.Model):
    image = models.FileField(upload_to='imgproc')