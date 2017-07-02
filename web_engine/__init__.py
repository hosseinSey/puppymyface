from flask import Flask

app = Flask(__name__)  # i.e., app = Flask('web_engine')
from web_engine import route
