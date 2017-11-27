'''
Created on Nov 9, 2017

@author: hossein
'''

from time import time
from flask import Flask
from flask import request
from flask import send_from_directory
from flask import render_template
from werkzeug import secure_filename
import json
import random

app = Flask(__name__)

def gen_random_name():
    return (
        str(time()).replace('.', '')
        + str(random.random()).replace('.', '')[:5]
    )

@app.route('/')
def home():
    page = '<h1> hi </h1>this is the home page'
    return page


@app.route('/upload', methods=['POST'])
def upload():
    ret_val = []
    if request.method == 'POST':
        for key in request.files:
            file = request.files[key]
            file_name = secure_filename(gen_random_name())
            file.save('uploads/' + file_name)
            ret_val.append(file_name)
    return json.dumps(ret_val), 200, {'Content-Type': 'application/json'}

@app.route('/bank/<file_name>')
def send_file(file_name):
    return send_from_directory('uploads', file_name)

@app.route('/static/<file_type>/<filename>')
def get_static_file(file_type, filename):
    return send_from_directory("static/" + file_type, filename)

@app.route('/dog_images/<filename>')
def get_dog_file(filename):
    return send_from_directory("static/dog_images", filename)

@app.route('/puppier', methods=['POST'])
def send_puppy_info():
    def is_valid_image_id(image_id: str):
        ''' check if the file exists '''
        return True

    BREED = 'breed'
    NROF_FACES = 'nrof_faces'
    DOG_IMAGES = 'dog_images'
    ret_val = {}
    breed = None
    nrof_faces = None

    r = random.random()
    p_success = 0.1
    if r < p_success:
        breed = 'German shepherd'
    if r < 8 * p_success:
        nrof_faces = 1

    if breed:
        ret_val[BREED] = breed.replace('_', ' ')
        ret_val[DOG_IMAGES] = [
            'German_shepherd_dog_04885.jpg',
            'German_shepherd_dog_04887.jpg',
            'German_shepherd_dog_04888.jpg',
            'German_shepherd_dog_04889.jpg',
            'German_shepherd_dog_04890.jpg']
    if nrof_faces:
        ret_val[NROF_FACES] = nrof_faces

    response = json.dumps(ret_val)
    return response


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5001, debug = True)
