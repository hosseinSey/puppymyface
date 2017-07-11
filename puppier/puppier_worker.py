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
from src.file_utils import get_file_properties, set_file_properties
#from recognizer import dog_names

image_cache = Redis(host = config.BaseConfig.IMAGE_CACHE_HOST, port = config.BaseConfig.IMAGE_CACHE_PORT)
meta_cache = Redis(host = config.BaseConfig.META_CACHE_HOST, port = config.BaseConfig.META_CACHE_PORT)

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


while True: 
    try: 
        keys = image_cache.scan()[1]
        #logging.warning("key scan = " + str(keys))
        for binary_key in keys:
            key = binary_key.decode()
            # check if the file 'key' has been processed before
            if not get_file_properties(meta_cache, key, 'breed'):  
                image = pickle.loads(image_cache.get(key))
                logging.warning("Start forward passing image through conv network...")
                breed = get_breed(image)
                logging.warning("CNN finished the job...")
                set_file_properties(meta_cache, key, breed = breed)
                logging.warning("key = {}, breed = {}".format(key, breed))
    except Exception as e: 
        logging.error(traceback.print_exc())
    #time.sleep(1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    