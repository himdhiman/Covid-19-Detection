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
import matplotlib.pyplot as plt

# Create your views here.


def home(request):
    data = requests.get("https://corona-virus-stats.herokuapp.com/api/v1/cases/general-stats")
    json_data = data.json()
    total_cases = json_data['data']['total_cases']
    total_recovered = json_data['data']['recovery_cases']
    total_deaths = json_data['data']['death_cases']
    if request.method == 'POST':
        os.system('rm -rf ./media')
        form = forms.UploadFile(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        result = predict()
        data = {
            'result' : result
        }
        return JsonResponse(data)   
    else:
        os.system('rm -rf ./media')
        form = forms.UploadFile()
        return render(request, 'index.html', {'form' : form, 'total_cases' : total_cases, 'total_recovered' : total_recovered, 'total_deaths' : total_deaths}) 


def predict():
    model = load_model('./weights.hdf5')
    last_conv_layer = model.get_layer("conv2d_3")
    img_name = os.listdir("./media/")[0]    
    img = image.load_img(os.path.join("./media", img_name), target_size = (224, 224))
    img = image.img_to_array(img)
    img /= 255.0
    img = img.reshape((-1, 224, 224, 3))

    test_datagen = image.ImageDataGenerator(rescale = 1.0/255)
    test_generator = test_datagen.flow_from_directory('.', classes = ['media'], target_size = (224, 224), class_mode = 'binary')
    pred = model.predict_generator(test_generator)[0]

    grads = K.gradients(model.output, last_conv_layer.output)
    pooled_grads = K.mean(grads[0], axis=(0, 1, 2))
    iterate = K.function([model.input], [pooled_grads, last_conv_layer.output])
    pooled_grads_, last_conv_layer_ = iterate([img])
    last_conv_layer_ = last_conv_layer_.reshape(108, 108, 64)
    for i in range(64):
        last_conv_layer_[:,:,i] *= pooled_grads_[i]
    heatmap = np.mean(last_conv_layer_ , axis = -1)
    for x in range(heatmap.shape[0]):
        for y in range(heatmap.shape[1]):
            heatmap[x,y] = np.max(heatmap[x,y],0)
    heatmap = np.maximum(heatmap,0)
    heatmap /= np.max(heatmap)
    plt.imsave("media/heatmap.jpg", heatmap)

    if(pred < 0.5):
        return "Covid-19 Positive"
    return "Covid-19 Negative"


