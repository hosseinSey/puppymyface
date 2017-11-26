
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    page = '<h1> hi </h1>this is the first page'
    return page # + render_template('index.html')
