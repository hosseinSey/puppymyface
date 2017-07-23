'''
Created on Jul 5, 2017

@author: Hossein
'''
import os
from glob import glob 

# load train, test, and validation datasets
script_dirname, script_filename = os.path.split(os.path.abspath(__file__))
path_to_data = os.path.join(script_dirname, '../data')

DOG_IMAGES_PATH = os.path.join(script_dirname, '../static/')
#test_files, test_targets = load_dataset(os.path.join(path_to_data, 'dogImagesTrain'))

def dog_files_for_breed(breed, num_dogs = 3):
    '''returns the path to files for this dog breed'''
    dog_files_for_this_breed = glob(os.path.join(DOG_IMAGES_PATH, 'dogImagesTrain/*' + breed + '/*'))
    selected_dog_paths = dog_files_for_this_breed #np.random.choice(dog_files_for_this_breed, size=num_dogs, replace=False)
    if not selected_dog_paths: 
        return None, None 
    paths = []
    dog_files = []
    for p in selected_dog_paths: 
        paths.append('/'.join(p.split('/')[:-1]))
        dog_files.append(p.split('/')[-1])
    return paths, dog_files

