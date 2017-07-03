from web_engine import app

# for running on the local machine: 
if __name__ == '__main__': 
    from flask import Flask
    app = Flask('web_engine') #app = Flask('web_engine')

import os
from time import localtime, strftime
from redis import Redis 
from .config import BaseConfig
from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#UPLOAD_FOLDER = 'web_engine/uploads/'
UPLOAD_FOLDER = '/tmp/uploads'

app.config.from_object(BaseConfig)

redis = Redis(host = app.config['REDIS_HOST'], port = app.config['REDIS_PORT'])

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

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    filename = str(filename).lower()
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/home2')
def home2():
    site_analytics()

    return render_template('first_page.html', 
                           visit_number = redis.get('hits').decode(),
                           since = redis.get('first_visit_day').decode())

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
            return render_template('error.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            #return redirect(url_for('send_file', filename = filename))
            return render_template('result_page.html', image = filename)
        else: 
            return render_template('error.html')
    else: 
        site_analytics()
        return render_template('first_page.html', 
                           visit_number = redis.get('hits').decode(),
                           since = redis.get('first_visit_day').decode())
    

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<path:filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename) 

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)
