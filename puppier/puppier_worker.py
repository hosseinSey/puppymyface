'''
Created on Jul 7, 2017

@author: Hossein
'''

from redis import Redis 
import config#, recognizer  #https://stackoverflow.com/questions/1112618/import-python-package-from-local-directory-into-interpreter
import logging
import traceback
import pickle
# the file_utils library will get added later when building the Docker file
from src.file_utils import get_file_properties, set_file_properties
from src.image_utils import face_detector
import threading
import time
#from recognizer import dog_names

image_cache = Redis(host = config.BaseConfig.IMAGE_CACHE_HOST, port = config.BaseConfig.IMAGE_CACHE_PORT)
meta_cache = Redis(host = config.BaseConfig.META_CACHE_HOST, port = config.BaseConfig.META_CACHE_PORT)


def face_detector_worker():
    while True: 
        try: 
            # find all the keys in the cache
            keys = image_cache.scan()[1]
            #logging.warning("key scan = " + str(keys))
            for binary_key in keys:
                key = binary_key.decode()
                # check if the file 'key' has been processed before
                if get_file_properties(meta_cache, key, 'nrof_human_faces') == None:   
                    image = pickle.loads(image_cache.get(key))
                    logging.warning("Start counting the number of faces ...")
                    # TODO: 
                    nrof_faces = face_detector(image)
                    logging.warning(".... {} human faces recognized.".format(nrof_faces))
                    set_file_properties(meta_cache, key, nrof_human_faces = nrof_faces)
                    logging.warning("key = {}, nrof_faces = {}".format(key, nrof_faces))
        except Exception as e: 
            logging.error(traceback.print_exc())
        #time.sleep(1)

# Start the face detector thread: 
t = threading.Thread(target= face_detector_worker)
t.start()   
logging.warning("Face recognizer thread started.")



#
# Import the Keras stuff which is really time taking
#
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


def puppier_worker():
    '''
    This function constantly monitors the cache for images. 
    If there is a new image in the cache, it will find the 
    resembling dog breed for it
    input: 
        no inputs 
    return: 
        no return 
    '''
    while True: 
        try: 
            # find all the keys in the cache
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
    
'''
for some reason, TensorFlow doesn't like to be run as a thread. So, I am running 
it as the main process 
'''
puppier_worker()    
    
    
    
    
    
    
    
    
    
    
    