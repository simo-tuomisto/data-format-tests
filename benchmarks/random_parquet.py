from random import shuffle
import numpy as np
import pyarrow.parquet as pq
from tools.parquet import read_image_bytes

pa_table = pq.read_table('data/deep-random.parquet')

average_brightness = 0

batches = pa_table.to_batches()

# Randomize batches
rng = np.random.default_rng(seed=10)
rng.shuffle(batches)

i = 0

order = []

for batch in batches:

    order.extend(batch['index'].to_pylist())
    images = batch['Data'].to_pylist()    
    
    # Randomize images
    rng.shuffle(images)
    
    for image_bytes in images:
        average_brightness += read_image_bytes(image_bytes).mean()
        
        i += 1
        
        if i%1000 == 0 and i>0:
            print('Average brightness of %d images: %f' % (i, average_brightness / i))

average_brightness /= len(pa_table)

print(average_brightness)

print(order[:100])