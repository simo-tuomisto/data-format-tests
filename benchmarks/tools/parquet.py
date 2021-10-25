import numpy as np
import cv2
import pyarrow as pa
import pyarrow.parquet as pq

def file_to_bytes(filename):
    
    with pa.OSFile(filename, 'rb') as stream:
        file_contents = stream.readall()
    return file_contents

def read_image_bytes(data):

    buffer = np.fromstring(data, dtype='uint8')
    return cv2.imdecode(buffer, cv2.IMREAD_COLOR)

def read_images_table(dataset):
    
    images = dataset.to_pylist()
    
    image_data = []
    
    for image in images:
        image_data.append(read_image_bytes(image))
        
    return np.asarray(image_data)