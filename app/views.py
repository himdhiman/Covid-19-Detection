from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from django.views.generic import TemplateView
import os
from keras.models import load_model, Sequential, Model
from keras.layers import *
import numpy as np
from keras.preprocessing import image
import keras.backend as K
import keras
from app import forms

# Create your views here.


def home(request):
    data = requests.get("https://corona-virus-stats.herokuapp.com/api/v1/cases/general-stats")
    json_data = data.json()
    total_cases = json_data['data']['total_cases']
    total_recovered = json_data['data']['recovery_cases']
    total_deaths = json_data['data']['death_cases']
    if request.method == 'POST':
        form = forms.UploadFile(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        result = predict()
        data = {
            'result' : result
        }
        os.system('rm -rf ./media')
        return JsonResponse(data)
    else:
        os.system('rm -rf ./media')
        form = forms.UploadFile()
        return render(request, 'index.html', {'form' : form, 'total_cases' : total_cases, 'total_recovered' : total_recovered, 'total_deaths' : total_deaths}) 


def predict():
    model = load_model('./weights.hdf5')
    test_datagen = image.ImageDataGenerator(rescale = 1.0/255)
    test_generator = test_datagen.flow_from_directory('.', classes = ['media'], target_size = (224, 224), class_mode = 'binary')
    pred = model.predict_generator(test_generator)[0]
    if(pred < 0.5):
        return "Covid-19 Positive"
    return "Covid-19 Negative"


