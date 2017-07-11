'''
Created on Jul 7, 2017

@author: Hossein
'''

from redis import Redis 
import logging
import time
import traceback
import pickle
#from recognizer import dog_names

image_cache = Redis(host = config.BaseConfig.IMAGE_CACHE_HOST, port = config.BaseConfig.IMAGE_CACHE_PORT)
meta_cache = Redis(host = config.BaseConfig.META_CACHE_HOST, port = config.BaseConfig.META_CACHE_PORT)


while True: 
    try: 
        keys = image_cache.scan()[1]
        #logging.warning("key scan = " + str(keys))
        for binary_key in keys:
            key = binary_key.decode()
            if not meta_cache.exists(key):  
                image = pickle.loads(image_cache.get(key))
                logging.warning("Start forward passing image through conv network...")
                breed = get_breed(image)
                logging.warning("CNN finished the job...")
                meta_cache.set(key, breed)
                logging.warning("key = {}, breed = {}".format(key, breed))
    except Exception as e: 
        logging.error(traceback.print_exc())
    #time.sleep(1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    