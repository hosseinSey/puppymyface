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
from flask import render_template, request, redirect, url_for, send_from_directory, send_file, session
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config.from_object(BaseConfig)

# Cache for the meta data and working variables 
meta_cache = Redis(host = app.config['META_CACHE_HOST'], port = app.config['META_CACHE_PORT'])
# Cache for blobs such as images
image_cache = Redis(host = app.config['IMAGE_CACHE_HOST'], port = app.config['IMAGE_CACHE_PORT'])

def site_analytics():
    '''
    perform  the analytics of the website including: 
        - number of visits to the the home page
        - 
    '''
    if not meta_cache.get('first_visit'): 
        meta_cache.set('first_visit', strftime("%a, %d %b %Y %H:%M:%S", localtime()))    
    if not meta_cache.get('first_visit_day'): 
        meta_cache.set('first_visit_day', strftime("%d %b %Y", localtime()))    
    meta_cache.incr('hits')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    filename = str(filename).lower()
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Route that will process the file upload
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check for input errors: 
        if 'file' not in request.files:
            return render_template('error.html')
        file = request.files['file']
        if file.filename == '':
            error_message = "It seems no file was selected."
            return render_template('error.html', message = error_message)
        # Save file in the Cache
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Save image into a BytesIO object which acts as a file
            file_object = io.BytesIO() 
            file.save(file_object)
            file_object.seek(0)
            # Pickle the object to save in the cache:
            image_cache.set(filename, pickle.dumps(file_object))
            file_object.close()
            # This is how to retrieve the image:  
            #file_object = pickle.loads(image_cache.get(filename))
            return redirect(url_for('upload_page', filename = filename))
        else:
            error_message = "Are you sure you are uploading an image file? " 
            return render_template('error.html', message = error_message)
    else: 
        site_analytics()
        return render_template('first_page.html', 
                           visit_number = meta_cache.get('hits').decode(),
                           since = meta_cache.get('first_visit_day').decode())
    

@app.route('/files/<filename>')
def send_file_from_cache(filename):
    '''
    Send a file from the cache such as redis.
    '''
    if image_cache.get(filename) and allowed_file(filename): 
        file_object = pickle.loads(image_cache.get(filename))
        file_extension = filename.split('.')[-1].lower() 
        mimetype = 'image/' + file_extension
        return send_file(file_object, mimetype = mimetype)

@app.route('/dogs/<breed_name>/<index>')
def send_dog_file(breed_name, index):
    from web_engine.src.image_utils import dog_files_for_breed
    paths, files = dog_files_for_breed(breed_name)
    if files: 
        return send_from_directory(paths[int(index) % len(paths)], files[int(index) % len(files)])
    return '' 


@app.route('/upload/<filename>', methods=['GET', 'POST'])
def upload_page(filename):
    
    '''
    import signal 
    def signal_handler(signum, frame):
        raise Exception("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(0.1)   # seconds
    '''
    try:
        '''
        You really shouldn't be doing computationally expensive operations in the web server
        '''
        #from web_engine.src.image_utils import face_detector
        #nr_human = face_detector(pickle.loads(image_cache.get(filename)))
        nr_human = -2
    except: 
        nr_human = -1

    if nr_human >= 0 : 
        message = "We recognized <b>{}</b> human face{} in the picture you uploaded{}".format(nr_human, 's' if nr_human > 1 else '', ' !!!' if nr_human < 0 else '.')
    else: 
        message = "We are blind, and we don't know if there is any human faces in your picture! <br>Our workers could not process your picture in a reasonable time."
    if request.method == 'POST': 
        return redirect(url_for('result_page', filename = filename))
    return render_template('upload_page.html', image = filename, msg = message)


@app.route('/result/<filename>')
def result_page(filename):
    # After determining the breed, let the image expire after 1 min
    breed = None 
    # if the results are back: 
    if meta_cache.exists(filename): 
        if image_cache.exists(filename):
            image_cache.expire(filename, 5 * 60)
        breed = meta_cache.get(filename).decode()
        message = "Hey! We think you resemble the <b> {} </b> breed!".format(breed.replace('_', ' '))
        return render_template('result_page.html', image = filename, msg = message, breed_name = breed)
    else: 
        message = "Sorry, our workers are very busy now. We are trying to find the best breed resemblance for you, but it seems we are too slow. Please go back and try again."
        return render_template('error.html', message = message)








if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)
