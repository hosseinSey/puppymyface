from web_engine import app

# for running on the local machine: 
if __name__ == '__main__': 
    from flask import Flask
    app = Flask('web_engine') #app = Flask('web_engine')

import io
import pickle            
import json            
from time import localtime, strftime, time
from redis import Redis 
from .config import BaseConfig
from flask import render_template, request, redirect, url_for, send_from_directory, send_file, session
from flask import jsonify
from werkzeug import secure_filename
from .src.file_utils import get_file_properties, set_file_properties

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

KEY_SESSION_ID_COUNT = 'last_session_id'
MAX_SESSION_COUNT = 2**16
SESSION_ID_KEY = 'id'
EXPIRE_AFTER_MINS = 60  # expire the uploaded image after this many minutes

app.config.from_object(BaseConfig)

# Cache for the meta data and working variables 
meta_cache = Redis(host = app.config['META_CACHE_HOST'], port = app.config['META_CACHE_PORT'])
# Cache for blobs such as images
image_cache = Redis(host = app.config['IMAGE_CACHE_HOST'], port = app.config['IMAGE_CACHE_PORT'])

if not meta_cache.exists(KEY_SESSION_ID_COUNT): 
    meta_cache.set(KEY_SESSION_ID_COUNT, 0)

def get_time_ms():
    return str(time()).replace('.', '')

def get_or_creat_session():
    '''
    Create a session. The session ID would be the current epoch + a counter to keep the sessions
    
    return 
        :str a session id 
    '''
    if SESSION_ID_KEY in session:
        return session[SESSION_ID_KEY]
    else: 
        meta_cache.incr(KEY_SESSION_ID_COUNT)
        if int(meta_cache.get(KEY_SESSION_ID_COUNT).decode()) > MAX_SESSION_COUNT:
            meta_cache.set(KEY_SESSION_ID_COUNT, 0) 
        session_id = get_time_ms() +  meta_cache.get(KEY_SESSION_ID_COUNT).decode()
        session[SESSION_ID_KEY] = session_id
        return session[SESSION_ID_KEY]
    

def get_breed_from_cache(filename):
    if meta_cache.exists(filename): 
        #exprie the file 
        if image_cache.exists(filename):
            image_cache.expire(filename, 2 * 60)
        return get_file_properties(meta_cache, filename, 'breed')

def is_image_expired(filename):
    '''
    Check the cache to see if the image has been expired.
    Expiration happens when file exists in the meta_cache but not in image_cache
    '''
    # TODO: implement this in proper way!
    if filename not in image_cache: 
        return True
    return False

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
    session_id = get_or_creat_session()
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
            filename = get_time_ms() + '_' + secure_filename(file.filename)
            # Save image into a BytesIO object which acts as a file
            file_object = io.BytesIO() 
            file.save(file_object)
            file_object.seek(0)
            # Pickle the object to save in the cache:
            file_pickled = pickle.dumps(file_object)
            image_cache.set(filename, file_pickled)
            file_object.close()
            # set an expiration time for the image:
            image_cache.expire(filename, EXPIRE_AFTER_MINS * 60) 
            # set the file properties:
            set_file_properties(meta_cache, filename, session_id = session_id) 
            set_file_properties(meta_cache, filename, private_to_device = 'True')
            
            # This is how to retrieve the image:  
            #file_object = pickle.loads(image_cache.get(filename))
            return redirect(url_for('upload_page', filename = filename))
        else:
            error_message = "Are you sure you are uploading an image file? " 
            return render_template('error.html', message = error_message)
    else: 
        site_analytics()
        return render_template('first_page.html')
    

@app.route('/files/<filename>')
def send_file_from_cache(filename):
    '''
    Send a file from the cache such as redis.
    '''
    if is_image_expired(filename): 
        return send_from_directory('static/images', 'icons-Expired.png')
    privacy = get_file_properties(meta_cache, filename, 'private_to_device')
    if privacy: 
        if privacy == 'True' and session[SESSION_ID_KEY] != get_file_properties(meta_cache, filename, 'session_id'):
            return send_from_directory('static/images', 'access_denied.gif')
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

@app.route('/static/<filename>')
def get_static_file(filename):
    file_path = {'ladda-themeless.min.css': 'static/dist/', 
                    'spin.min.js': 'static/dist/', 
                    'ladda.min.js': 'static/dist/'}
    if filename in file_path: 
        return send_from_directory(file_path[filename], filename)
    else: 
        raise Exception("File not in list.")


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
    breed = get_breed_from_cache(filename) 
    # if the results are back: 
    if breed :
        message = "Hey! We think you resemble the <b> {} </b> breed!".format(breed.replace('_', ' '))
    else: 
        message = "We are trying to find the best breed resemblance for you, but it seems our workers are too slow. <br> <br> Please refresh this page again in a few seconds."
    return render_template('result_page.html', image = filename, msg = message, breed_name = breed)


@app.route('/qz-1e-0e-9d-ae-81J-c1-bb-8d-e8-88q-81')
def clear():
    meta_cache.flushall()
    image_cache.flushall()
    return "All data in the cache flushed out!"

@app.route('/job_stat', methods=['POST'])
def is_recognized():
    '''
    Checks if the dog breed for the image for filename is recognized
    input: 
        :filename str name of the file
    output: 
        :json {status: done/processing/error}
    '''
    if request.method == 'POST':
        filename = request.form['filename']
        if meta_cache.exists(filename): 
            breed = get_file_properties(meta_cache, filename, 'breed')
            if breed: 
                return jsonify({'status' : 'done'})
            else: 
                return jsonify({'status' : 'processing'})
        return jsonify({'status' : 'error'})

@app.route('/about')
def about_page():
    #count the number of times an image is puppied
    return render_template('about.html', 
                       visit_number = meta_cache.get('hits').decode(),
                       since = meta_cache.get('first_visit_day').decode())

@app.route('/privacy_policy')
def privacy_policy_page():
    return ''


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)
