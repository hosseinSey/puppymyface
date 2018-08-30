'''
Created on Jul 5, 2017

@author: Hossein
'''
import os
import cv2   
import numpy as np 
from PIL import Image           

# load train, test, and validation datasets
script_dirname, script_filename = os.path.split(os.path.abspath(__file__))
path_to_data = os.path.join(script_dirname, '../data')


# extract pre-trained face detector
face_cascade = cv2.CascadeClassifier(os.path.join(path_to_data, 'haarcascades/haarcascade_frontalface_alt.xml'))

def face_detector(raw_image):#(img_path):
    '''
    detect the human faces in an image. 
    '''
    image_array_rgb = np.array(Image.open(raw_image))    
    img = cv2.cvtColor(image_array_rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces)

