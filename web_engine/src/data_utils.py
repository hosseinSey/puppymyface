'''
Created on Jul 5, 2017

@author: Hossein
'''
import os
from glob import glob

# load train, test, and validation datasets
script_dirname, script_filename = os.path.split(os.path.abspath(__file__))
path_to_data = os.path.join(script_dirname, '../data')

DOG_IMAGES_PATH = os.path.join(script_dirname, '../static/dog_images')
#test_files, test_targets = load_dataset(os.path.join(path_to_data, 'dogImagesTrain'))

def dog_files_for_breed(breed):
    '''returns the path to files for this dog breed'''
    path = os.path.join(DOG_IMAGES_PATH, breed + '*')
    dog_files_for_this_breed = glob(str(path))
    selected_dog_paths = dog_files_for_this_breed #np.random.choice(dog_files_for_this_breed, size=num_dogs, replace=False)
    if not selected_dog_paths:
        return None
    paths = []
    dog_files = []
    for p in selected_dog_paths:
        paths.append('/'.join(p.split('/')[:-1]))
        dog_files.append(p.split('/')[-1])
    return dog_files, paths


if __name__ == '__main__':
    print('==== FUNC CALL ======')
    print(dog_files_for_breed(breed))





#
