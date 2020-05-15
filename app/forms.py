from django import forms
from app import models

class UploadFile(forms.ModelForm):
    class Meta:
        model = models.UploadModel
        fields = ['img_file']