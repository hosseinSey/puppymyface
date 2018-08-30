
import io
import logging
import json
import random
import pickle
from time import time
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory, send_file
from redis import Redis
from werkzeug import secure_filename
from config import BaseConfig

from src.file_utils import get_file_properties, set_file_properties
from src.data_utils import dog_files_for_breed

app = Flask(__name__)  # i.e., app = Flask('web_engine')
app.config.from_object(BaseConfig)

# Cache for the meta data and working variables
meta_cache = Redis(host = app.config['META_CACHE_HOST'], port = app.config['META_CACHE_PORT'])
# Cache for blobs such as images
image_cache = Redis(host = app.config['IMAGE_CACHE_HOST'], port = app.config['IMAGE_CACHE_PORT'])

def gen_random_name():
    '''
    Generate a name based on time and a random generator
    '''
    return (
        str(time()).replace('.', '')
        + str(random.random()).replace('.', '')[:5]
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def receive_files():
    '''
    Endpoint for receiving files from client. Store the files in cache
    and return the name of the files
    '''
    ret_val = []
    if request.method == 'POST':
        for key in request.files:
            file = request.files[key]
            filename = secure_filename(gen_random_name())
            #
            # Save image into a BytesIO object which acts as a file
            file_object = io.BytesIO()
            file.save(file_object)
            file_object.seek(0)
            # Pickle the object to save in the cache:
            file_pickled = pickle.dumps(file_object)
            image_cache.set(filename, file_pickled)
            file_object.close()
            # set an expiration time for the image:
            image_cache.expire(filename, app.config['EXPIRE_AFTER_MINS'] * 60)
            #
            ret_val.append(filename)
    return json.dumps(ret_val), 200, {'Content-Type': 'application/json'}

@app.route('/static/<file_type>/<filename>')
def get_static_file(file_type, filename):
    #logging.warning('static files being sent')
    return send_from_directory("static/" + file_type, filename)

@app.route('/bank/<filename>')
def send_image_from_cache(filename):
    '''
    Retreive and send image files from the Redis cache
    '''
    if image_cache.get(filename):
        file_object = pickle.loads(image_cache.get(filename))
        mimetype = 'image/*'
        return send_file(file_object, mimetype = mimetype)


@app.route('/dog_images/<filename>')
def send_dog_file(filename):
    return send_from_directory("static/dog_images", filename)

@app.route('/puppier', methods=['POST'])
def send_puppy_info():
    def is_valid_image_id(image_id: str):
        ''' check if the file exists '''
        if meta_cache.exists(filename):
            return True
        return False

    BREED = 'breed'
    NROF_FACES = 'nrof_faces'
    DOG_IMAGES = 'dog_images'
    ret_val = {}
    breed = None
    nrof_faces = None

    for key in request.form:
        filename = request.form[key]
        if is_valid_image_id(filename):
            breed = get_file_properties(meta_cache, filename, 'breed')
            nrof_faces = get_file_properties(meta_cache, filename, 'nrof_human_faces')
            #logging.warning('breed of {} is {} '.format(filename, breed))
            #logging.warning('nr of human faces in {} is {} '.format(filename, nrof_faces))
    if breed:
        ret_val[BREED] = breed.replace('_', ' ')
        dog_files, _ = dog_files_for_breed(breed)
        ret_val[DOG_IMAGES] = dog_files
    if nrof_faces != None:
        ret_val[NROF_FACES] = nrof_faces

    response = json.dumps(ret_val)
    return response







#
