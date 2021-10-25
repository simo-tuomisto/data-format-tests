import os
import numpy as np
import pandas as pd
from tools.singlefile import read_image

datafolder = 'data/deep'
labelsfile = 'data/labels.csv'
outputfile = 'data/deep-random.parquet'

labels = pd.read_csv(labelsfile)
labels.reset_index(inplace=True)

labels['Fullpath'] = labels['Filename'].apply(lambda filename: os.path.join(datafolder, filename))

# Randomize rows
rng = np.random.default_rng(seed=10)
index_shuffle = np.asarray(labels.index.copy())
rng.shuffle(index_shuffle)
labels = labels.iloc[index_shuffle]

average_brightness = 0

for i, filename in enumerate(labels['Fullpath']):
    average_brightness += read_image(filename).mean()
    if i%1000 == 0 and i>0:
        print('Average brightness of %d images: %f' % (i, average_brightness / i))

average_brightness /= len(labels)
print(average_brightness)

print(list(labels.index)[:100])