from flask import render_template, jsonify, Flask, redirect, url_for, request
from app import app
import random
import os
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image
import numpy as np
from keras.models import load_model
from keras.initializers import glorot_uniform
import h5py


@app.route('/')

#disease_list = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax', 'Edema', 'Emphysema', \
                  # 'Fibrosis', 'Effusion', 'Pneumonia', 'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', \
                  # 'Hernia']

@app.route('/upload')
def upload_file2():
   return render_template('index.html')
	
@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      modeltype = request.values.get("selectmodel")
      path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
      print(path)
      x=[]
      img = image.load_img(path, target_size=(456,512), grayscale=True)
      img = image.img_to_array(img)
      img = img/255
      x.append(img)
      xx=np.array(x)
      if modeltype == "Elbow":
         model=load_model('elbow.h5',custom_objects={'GlorotUniform': glorot_uniform()}, compile=False)
      elif modeltype == "Hand":
         model=load_model('hand.h5',custom_objects={'GlorotUniform': glorot_uniform()}, compile=False)
      elif modeltype == "Finger":
         model=load_model('finger.h5',custom_objects={'GlorotUniform': glorot_uniform()}, compile=False)
      else:
         model = None

      if model is None:
         preds = [[0, 0]]
      else:
         preds = model.predict(xx)


      if preds[0][0] == 0:
      	d='model is not selected'
      elif preds[0][0] <= 0.40:
      	d='Bone is not break'
      elif preds[0][0] >= 0.60:
      	d='Bone is break'
      else:
      	d = 'I am not sure'

      f.save(path)
      return render_template('uploaded.html', title='Success', diagnose=d,  predictions=preds, user_image=f.filename, type_image=modeltype )


@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
   
    points = [(33.99986612400209, 71.47586110541991)]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
