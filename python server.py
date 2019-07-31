from flask import Flask,request
from flask_cors import CORS
import cv2
import tensorflow as tf
import numpy as np
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)
@app.route("/predict/",methods=['GET'])
def predict():
    url=request.args.get('url')
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    pix = np.array(img)
    print(pix.shape)
    X= cv2.resize(pix,dsize=(224,224))
    model = tf.keras.models.load_model('model.h5')
    images=[X]
    X=np.asarray(images)
    predictions=model.predict(X)
    p=(np.argmax(predictions, axis=1)[0])
    s=str(p)+""
        
    return s

@app.route("/",methods=['GET'])
def default():
    return "<h1> Welcome to Samba's test server <h1>"

if __name__ == '__main__':
    app.run()
