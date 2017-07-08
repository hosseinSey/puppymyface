'''
Created on Jul 7, 2017

@author: Hossein
'''

from redis import Redis 
import config#, recognizer  #https://stackoverflow.com/questions/1112618/import-python-package-from-local-directory-into-interpreter
import logging
import time
import traceback
import pickle
#from recognizer import dog_names

image_cache = Redis(host = config.BaseConfig.REDIS_HOST, port = config.BaseConfig.REDIS_PORT)

# Import the Keras stuff which is really time taking
logging.warning("Loading Keras modules...")
import recognizer
logging.warning("Modules are loaded. The puppier_worker is starting...")

def get_breed(image_file):
    #is_human = face_detector(full_image_path)
    #is_dog = recognizer.dog_detector(full_image_path)
    
    #breed = None 
    #if is_human or is_dog:
    breed = recognizer.Resnet50_predict_breed(image_file)
    #else: 
    #    message = "We found neither dogs nor human in the picture you uploaded."
    
    
    #if is_human: 
    #    message =  'The human face in the picture resembles the "{}"'.format(breed.replace('_', ' '))
    #elif is_dog: 
    #    message = 'The breed of dog in the picture is "{}"'.format(breed.replace('_', ' '))
    return breed


# A temprary solution to sift through images only, should be the same as the one in puppifier_worker
IMAGE_CACHE_PREFIX = 'puppifier_'
IMAGE_CACHE_SUFFIX = '_breed'

def is_valid_key(key):
    '''checks if the key is for an image and meet the criteria''' 
    prefix_len = len(IMAGE_CACHE_PREFIX)
    return (type(key) is str
            and len(key) >= prefix_len 
            and key[:prefix_len] == IMAGE_CACHE_PREFIX 
            and (len(key) < len(IMAGE_CACHE_SUFFIX) 
                 or len(key) >= len(IMAGE_CACHE_SUFFIX) 
                 and  key[-len(IMAGE_CACHE_SUFFIX):] != IMAGE_CACHE_SUFFIX))

while True: 
    try: 
        keys = image_cache.scan()[1]
        #logging.warning("key scan = " + str(keys))
        for binary_key in keys:
            str_key = binary_key.decode()
            if is_valid_key(str_key):
                key_for_result = str_key + IMAGE_CACHE_SUFFIX
                if not image_cache.get(key_for_result):  
                    image = pickle.loads(image_cache.get(str_key))
                    breed = get_breed(image)
                    image_cache.set(key_for_result,  breed)
                    logging.warning("key = {}, breed = {}".format(key_for_result, breed))
    except Exception as e: 
        logging.error(traceback.print_exc())
    time.sleep(0.4)
    
    
    
    
    
    
    
    
    
    
    
    
    
    