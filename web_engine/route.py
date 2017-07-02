#from web_engine import app

# for running on the local machine: 
#if __name__ == '__main__': 
from flask import Flask
app = Flask('web_engine') #app = Flask('web_engine')

import os
from time import localtime, strftime
from redis import Redis 
#from .config import BaseConfig
class BaseConfig(object):
    SECRET_KEY = 'none'
    DEBUG = False
    REDIS_HOST = 'redis'
    REDIS_PORT = 6379


from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#UPLOAD_FOLDER = 'web_engine/uploads/'
UPLOAD_FOLDER = 'uploads/'

app.config.from_object(BaseConfig)

#redis = Redis(host = app.config['REDIS_HOST'], port = app.config['REDIS_PORT'])
redis = None


def site_analytics():
    '''
    perform  the analytics of the website including: 
        - number of visits to the the home page
        - 
    '''
    if not redis.get('first_visit'): 
        redis.set('first_visit', strftime("%a, %d %b %Y %H:%M:%S", localtime()))    
    if not redis.get('first_visit_dat'): 
        redis.set('first_visit_day', strftime("%d %b %Y", localtime()))    
    redis.incr('hits')

@app.route('/home')
def home_page():
    site_analytics()
    
    return render_template('first_page.html', 
                           visit_number = redis.get('hits').decode(),
                           since = redis.get('first_visit_day').decode())

# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        
        #return "success"
        import subprocess
        subprocess.call(['chmod', '0744', file_path])
        
        from os import listdir
        from os.path import isfile, join
        onlyfiles = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]
        #return str(onlyfiles)
    
        return redirect(url_for('uploaded_file', filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)


@app.route('/test')
def test():
    output = ''
    output += 'Hey There!'
    output += '<hr>'
    output += '<br>'
    output += 'The time is now: '
    output += strftime("%a, %d %b %Y %H:%M:%S", localtime())
    output += '<br>'
    output += strftime("%d %b %Y", localtime())
    output += '<br>'

    return output 

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)
