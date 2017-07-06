'''
Created on Jul 5, 2017

@author: Hossein
'''
import os
from sklearn.datasets import load_files       
from keras.utils import np_utils
import numpy as np
from glob import glob
import cv2                

# define function to load train, test, and validation datasets
def load_dataset(path):
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    dog_targets = np_utils.to_categorical(np.array(data['target']), 133)
    return dog_files, dog_targets

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




# load list of dog names
dog_names = [item[50:-1] for item in sorted(glob(os.path.join(DOG_IMAGES_PATH, "dogImagesTest/*/")))]


# extract pre-trained face detector
face_cascade = cv2.CascadeClassifier(os.path.join(path_to_data, 'haarcascades/haarcascade_frontalface_alt.xml'))

# returns "True" if face is detected in image stored at img_path
def face_detector(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces) > 0


#Detect Dogs: 
#We use a pre-trained ResNet-50 model to detect dogs in images. 
#First download the ResNet-50 model, along with weights that have been trained on ImageNet, 
#a very large, very popular dataset used for image classification and other vision tasks. 
#ImageNet contains over 10 million URLs, each linking to an image containing an object from 
#one of 1000 categories. Given an image, this pre-trained ResNet-50 model returns a prediction 
#(derived from the available categories in ImageNet) for the object that is contained in the image.

from keras.applications.resnet50 import ResNet50
# define ResNet50 model
ResNet50_model = ResNet50(weights='imagenet')



# Pre-process the Data

#When using TensorFlow as backend, Keras CNNs require a 4D array (which we'll also refer to as a 4D tensor) as input, with shape
#(nb_samples,rows,columns,channels),
#(nb_samples,rows,columns,channels),
 #where nb_samples corresponds to the total number of images (or samples), and rows, columns, and channels correspond to the number of rows, columns, and channels for each image, respectively.
#The path_to_tensor function below takes a string-valued file path to a color image as input and returns a 4D tensor suitable for supplying to a Keras CNN. The function first loads the image and resizes it to a square image that is  224×224224×224  pixels. Next, the image is converted to an array, which is then resized to a 4D tensor. In this case, since we are working with color images, each image has three channels. Likewise, since we are processing a single image (or sample), the returned tensor will always have shape
#(1,224,224,3).
#(1,224,224,3).
#The paths_to_tensor function takes a numpy array of string-valued image paths as input and returns a 4D tensor with shape
#(nb_samples,224,224,3).
#(nb_samples,224,224,3).
#Here, nb_samples is the number of samples, or number of images, in the supplied array of image paths. It is best to think of nb_samples as the number of 3D tensors (where each 3D tensor corresponds to a different image) in your dataset!

from keras.preprocessing import image                  

def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)


# Making Predictions with ResNet-50
#Getting the 4D tensor ready for ResNet-50, and for any other pre-trained model in Keras, requires some additional processing. First, the RGB image is converted to BGR by reordering the channels. All pre-trained models have the additional normalization step that the mean pixel (expressed in RGB as  [103.939,116.779,123.68][103.939,116.779,123.68]  and calculated from all pixels in all images in ImageNet) must be subtracted from every pixel in each image. This is implemented in the imported function preprocess_input. If you're curious, you can check the code for preprocess_input here.
#Now that we have a way to format our image for supplying to ResNet-50, we are now ready to use the model to extract the predictions. This is accomplished with the predict method, which returns an array whose  ii -th entry is the model's predicted probability that the image belongs to the  ii -th ImageNet category. This is implemented in the ResNet50_predict_labels function below.
#By taking the argmax of the predicted probability vector, we obtain an integer corresponding to the model's predicted object class, which we can identify with an object category through the use of this dictionary.

from keras.applications.resnet50 import preprocess_input, decode_predictions

def ResNet50_predict_labels(img_path):
    # returns prediction vector for image located at img_path
    img = preprocess_input(path_to_tensor(img_path))
    return np.argmax(ResNet50_model.predict(img))


# Write a Dog Detector
#While looking at the dictionary, you will notice that the categories corresponding to dogs appear in an uninterrupted sequence and correspond to dictionary keys 151-268, inclusive, to include all categories from 'Chihuahua' to 'Mexican hairless'. Thus, in order to check to see if an image is predicted to contain a dog by the pre-trained ResNet-50 model, we need only check if the ResNet50_predict_labels function above returns a value between 151 and 268 (inclusive).
#We use these ideas to complete the dog_detector function below, which returns True if a dog is detected in an image (and False if not).

### returns "True" if a dog is detected in the image stored at img_path
def dog_detector(img_path):
    prediction = ResNet50_predict_labels(img_path)
    return ((prediction <= 268) & (prediction >= 151))


# Obtain Bottleneck Features
#In the code block below, extract the bottleneck features corresponding to the train, test, and validation sets by running the following:
#bottleneck_features = np.load('bottleneck_features/Dog{network}Data.npz')
#train_{network} = bottleneck_features['train']
#valid_{network} = bottleneck_features['valid']
#test_{network} = bottleneck_features['test']

### TODO: Obtain bottleneck features from another pre-trained CNN.
bottleneck_features = np.load(os.path.join(path_to_data, 'bottleneck_features/DogResnet50Data.npz'))
train_Resnet50 = bottleneck_features['train']
valid_Resnet50 = bottleneck_features['valid']
test_Resnet50 = bottleneck_features['test']

from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential

### Define your architecture.
Resnet50_model = Sequential()
Resnet50_model.add(GlobalAveragePooling2D(input_shape=train_Resnet50.shape[1:]))
Resnet50_model.add(Dense(133, activation='softmax'))
#ResNet50_model.summary()


### Load the model weights with the best validation loss.
Resnet50_model.load_weights(os.path.join(path_to_data, 'saved_models/weights.best.Resnet50.hdf5'))


### TODO: Write a function that takes a path to an image as input
### and returns the dog breed that is predicted by the model.

from .extract_bottleneck_features import *

def Resnet50_predict_breed(img_path):
    # extract bottleneck features
    bottleneck_feature = extract_Resnet50(path_to_tensor(img_path))
    # obtain predicted vector
    predicted_vector = Resnet50_model.predict(bottleneck_feature)
    # return dog breed that is predicted by the model
    return dog_names[np.argmax(predicted_vector)]


