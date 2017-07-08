'''
Created on Jun 23, 2017

@author: Hossein
'''

import os

class BaseConfig(object):
    #DEBUG = os.environ['DEBUG']
    REDIS_HOST = 'redis' #os.environ['REDIS_HOST'] #'redis'
    REDIS_PORT = 6379 #os.environ['REDIS_PORT'] #6379

