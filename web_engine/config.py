'''
Created on Jun 23, 2017

@author: Hossein
'''

import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    IMAGE_CACHE_HOST = os.environ['IMAGE_CACHE_HOST'] #'redis'
    IMAGE_CACHE_PORT = os.environ['IMAGE_CACHE_PORT'] #6379
    META_CACHE_HOST = os.environ['META_CACHE_HOST']
    META_CACHE_PORT = os.environ['META_CACHE_PORT']
    EXPIRE_AFTER_MINS = 20  # expire the uploaded image after this many minutes
