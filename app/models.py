from django.db import models

# Create your models here.

class UploadModel(models.Model):
    img_file = models.ImageField(upload_to= '', blank = False)
