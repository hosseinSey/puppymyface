'''
Created on Jun 23, 2017

@author: Hossein
'''

import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    REDIS_HOST = os.environ['REDIS_HOST'] #'redis'
    REDIS_PORT = os.environ['REDIS_PORT'] #6379

