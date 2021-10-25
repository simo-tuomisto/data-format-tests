import os
import numpy as np
import pandas as pd
from tools.singlefile import read_image

datafolder = 'data/deep'

labels = pd.read_csv('data/labels.csv')

labels['Fullpath'] = labels['Filename'].apply(lambda filename: os.path.join(datafolder, filename))

average_brightness = 0

for filename in labels['Fullpath']:
    average_brightness += read_image(filename).mean()

average_brightness /= len(labels)
print(average_brightness)
