# Created by Egonu Narcisse. May 21, 2019
#importing the module that has the function
#from result_function import Analyze
# importing packages from Flask
from flask import Flask, render_template, json, request, url_for, jsonify
# importing the model from soil analysis folder
from flask_cors import CORS
#from flask_restful import api
# import TS packages
#from PIL import Image
# importing the necessary libraries
from keras import backend as K
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array, load_img
from keras.models import load_model
import numpy as np
import pickle
import os


app = Flask(__name__)

# Initializing Cors
CORS(app)

# default route
@app.route("/")
def home():
    return "Hello World"

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return f" Wrong Url {e}"


@app.route("/api", methods=["POST"])
def api():
   print(request.files["file"])
   input_data = request.files['file']
   print(input_data)
   data = "Nariccse"
   response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
   return response

@app.route("/analyse", methods=["POST"])
def check():
   def Analyze(imgPath):
    # loading the necssary models
    truth = ["Clay Soil", "loamy Soil", "Sandy Soil"]
    model_1 = load_model("real_vgg16.h5")
    model_2 = pickle.loads(open("first_model.pickle", "rb").read())

    # preprocessing the image and predicting
    image = load_img(imgPath, target_size=(224, 224))
    image = img_to_array(image)
    image = imagenet_utils.preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    features = model_1.predict(image)
    features = features.reshape((1, 512*7*7))
    final_result = model_2.predict(features)
    return truth[final_result[0]]


   input_d = request.files["file"]
   print(input_d)
   #name = Analyze(r"loamy.jpg")
   name = Analyze(input_d)
   K.clear_session()
   # print(name, "It worked")

   return jsonify({"data" : name})


if __name__ == "__main__":
    app.run(port="5001", debug=True)
