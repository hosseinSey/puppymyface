from web_engine import app

# for running on the local machine: 
if __name__ == '__main__': 
    from flask import Flask
    app = Flask('web_engine') #app = Flask('web_engine')

import io
import pickle            
import os
from time import localtime, strftime
from redis import Redis 
from .config import BaseConfig
from flask import render_template, request, redirect, url_for, send_from_directory, send_file
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config.from_object(BaseConfig)

redis = Redis(host = app.config['REDIS_HOST'], port = app.config['REDIS_PORT'])
image_cache = redis
# A temprary solution to sift through images only, should be the same as the one in puppifier_worker
IMAGE_CACHE_PREFIX = 'puppifier_'
IMAGE_CACHE_SUFFIX = '_breed'


def site_analytics():
    '''
    perform  the analytics of the website including: 
        - number of visits to the the home page
        - 
    '''
    if not redis.get('first_visit'): 
        redis.set('first_visit', strftime("%a, %d %b %Y %H:%M:%S", localtime()))    
    if not redis.get('first_visit_day'): 
        redis.set('first_visit_day', strftime("%d %b %Y", localtime()))    
    redis.incr('hits')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    filename = str(filename).lower()
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Route that will process the file upload
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('error.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error_message = "It seems no file was selected."
            return render_template('error.html', message = error_message)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = IMAGE_CACHE_PREFIX + filename
            # Store the image into the cache. To do so, we need to pickle the saved image. 
            # Otherwise, the image can not be retrieved from Redis
            output = io.BytesIO() 
            file.save(output)
            output.seek(0)
            image_cache.set(filename, pickle.dumps(output))
            output.close()
            # This is how to retrieve the image:  
            #file_object = pickle.loads(image_cache.get(filename))
            #return send_file(file_object, mimetype='image/' + filename.split('.')[-1]) 
            return redirect(url_for('upload_page', filename = filename))
        else:
            error_message = "Are you sure you are uploading an image file? " 
            return render_template('error.html', message = error_message)
    else: 
        site_analytics()
        return render_template('first_page.html', 
                           visit_number = redis.get('hits').decode(),
                           since = redis.get('first_visit_day').decode())
    

@app.route('/files/<filename>')
def send_file_from_cache(filename):
    '''
    Send a file from the cache such as redis.
    '''
    file_extension = filename.split('.')[-1].lower() 
    if image_cache.get(filename) and allowed_file(filename): 
        file_object = pickle.loads(image_cache.get(filename))
        mimetype = 'image/' + file_extension
        return send_file(file_object, mimetype = mimetype)

@app.route('/dogs/<breed_name>/<index>')
def send_dog_file(breed_name, index):
    from web_engine.src.image_utils import dog_files_for_breed
    paths, files = dog_files_for_breed(breed_name)
    return send_from_directory(paths[int(index) % len(paths)], files[int(index) % len(files)]) 


@app.route('/upload/<filename>', methods=['GET', 'POST'])
def upload_page(filename):
    from web_engine.src.image_utils import face_detector
    try:
        nr_human = face_detector(pickle.loads(image_cache.get(filename)))
    except: 
        nr_human = -1

    message = "We recognized <b>{}</b> human face{} in the picture you uploaded{}".format(nr_human, 's' if nr_human > 1 else '', ' !!!' if nr_human < 0 else '.')
    if request.method == 'POST': 
        return redirect(url_for('result_page', filename = filename))
    return render_template('upload_page.html', image = filename, msg = message)


@app.route('/result/<filename>')
def result_page(filename):
    '''
    from .src.recognizer import face_detector, dog_detector, Resnet50_predict_breed, dog_files_for_breed
    from glob import glob 
    full_image_path = os.path.join(UPLOAD_FOLDER, filename)

    is_human = face_detector(full_image_path)
    is_dog = dog_detector(full_image_path)

    breed = None 
    if is_human or is_dog:
        breed = Resnet50_predict_breed(full_image_path)
    else: 
        message = "We found neither dogs nor human in the picture you uploaded."
    

    if is_human: 
        message =  'The human face in the picture resembles the "{}"'.format(breed.replace('_', ' '))
    elif is_dog: 
        message = 'The breed of dog in the picture is "{}"'.format(breed.replace('_', ' '))
    '''
    # After determining the breed, let the image expire after 1 min
    breed = None 
    if image_cache.exists(filename + IMAGE_CACHE_SUFFIX): 
        image_cache.expire(filename, 60)
        breed = image_cache.get(filename + IMAGE_CACHE_SUFFIX).decode()
        message = "Hey! We think you resemble the <b> {} </b> breed!".format(breed.replace('_', ' '))
        return render_template('result_page.html', image = filename, msg = message, breed_name = breed)
    else: 
        message = "Sorry, our workers are very busy now. We are trying to find the best breed resemblance for you, but it seems we are too slow. Please go back and try again."
        return render_template('error.html', message = message)








if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)
