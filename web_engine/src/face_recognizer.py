'''
Created on Jul 5, 2017

@author: Hossein
'''
import os
import cv2    
from glob import glob            


# load train, test, and validation datasets
script_dirname, script_filename = os.path.split(os.path.abspath(__file__))
path_to_data = os.path.join(script_dirname, '../data')


# extract pre-trained face detector
face_cascade = cv2.CascadeClassifier(os.path.join(path_to_data, 'haarcascades/haarcascade_frontalface_alt.xml'))

# returns "True" if face is detected in image stored at img_path
def face_detector(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces)





# load train, test, and validation datasets
script_dirname, script_filename = os.path.split(os.path.abspath(__file__))
path_to_data = os.path.join(script_dirname, '../data')
DOG_IMAGES_PATH = os.path.join(script_dirname, '../static/')
#test_files, test_targets = load_dataset(os.path.join(path_to_data, 'dogImagesTest'))

def dog_files_for_breed(breed, num_dogs = 3):
    '''returns the path to files for this dog breed'''
    dog_files_for_this_breed = glob(os.path.join(DOG_IMAGES_PATH, 'dogImagesTest/*' + breed + '/*'))
    selected_dog_paths = dog_files_for_this_breed #np.random.choice(dog_files_for_this_breed, size=num_dogs, replace=False)
    paths = []
    dog_files = []
    for p in selected_dog_paths: 
        paths.append('/'.join(p.split('/')[:-1]))
        dog_files.append(p.split('/')[-1])
    return paths, dog_files

