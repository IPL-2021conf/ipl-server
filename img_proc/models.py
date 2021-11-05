from django.db import models

# Create your models here.
class ImgProcModel(models.Model):
    image = models.FileField(upload_to='imgproc')
    
class ImgFaceModel(models.Model):
    image = models.FileField(upload_to='imgproc')

class VdoProcModel(models.Model):
    video = models.FileField(upload_to='videoproc')
class VdoFaceModel(models.Model):
    video_face = models.FileField(upload_to='videoproc')