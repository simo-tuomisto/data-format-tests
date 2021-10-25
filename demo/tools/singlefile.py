import numpy as np
import cv2

def read_image(filename):

    return cv2.imread(filename)

def read_images(images):
    
    image_data = []
    
    for image in images:
        image_data.append(read_image(image))
        
    return np.asarray(image_data)