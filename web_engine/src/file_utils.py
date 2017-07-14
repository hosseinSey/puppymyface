import json            
from redis import Redis 

ALLOWED_FILE_PROPERTIES = set(['session_id', 'breed', 'private_to_device'])

def set_file_properties(cache: Redis, key: str, **kwarg):
    '''
    Set the properties for a file in the cache
    The structure of cache is {..., key : {a json object with properties as fields}, ...}
    
    input
        :cache_name the cache to be manipulated 
        :key the key to the record 
        :kwargs 
    '''
    # create the entry if it doesn't exists
    if not cache.exists(key): 
        cache.set(key, '{}')
    file_properties_json = cache.get(key).decode()  

    try: 
        file_properties = json.loads(file_properties_json)             
    except: 
        # TODO: handle the exception
        raise
    # update the file properties with the arguments provided to the fundtion:    
    for arg_key, arg_val in kwarg.items(): 
        if arg_key not in ALLOWED_FILE_PROPERTIES:
            raise Exception('Invalid file property.')            
        file_properties[arg_key] = arg_val
    cache.set(key, json.dumps(file_properties)) 
             
def get_file_properties(cache: Redis, key: str, property_name):
    '''
    Get the properties for a file in the cache
    The structure of cache is {..., key : {a json object with properties as fields}, ...}
    
    input
        :cache_name the cache to be manipulated 
        :key the key to the record 
        :property_name the name of file property to get 
        
    return
        : property value or None
    '''
    if property_name not in ALLOWED_FILE_PROPERTIES:
        raise Exception('Invalid file property.')
    
    if not cache.exists(key):
        return            
    file_properties_json = cache.get(key).decode()  
    try: 
        file_properties = json.loads(file_properties_json)          
    except: 
        # TODO: handle the exception
        return
    if property_name in file_properties: 
        return file_properties[property_name]
        