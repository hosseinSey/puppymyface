'''
Created on Jun 23, 2017

@author: Hossein
'''

import os

class BaseConfig(object):
    IMAGE_CACHE_HOST = os.environ['IMAGE_CACHE_HOST'] #'redis'
    IMAGE_CACHE_PORT = os.environ['IMAGE_CACHE_PORT'] #6379
    META_CACHE_HOST = os.environ['META_CACHE_HOST'] 
    META_CACHE_PORT = os.environ['META_CACHE_PORT'] 

