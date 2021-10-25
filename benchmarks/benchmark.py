import os
import argparse
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from tools.singlefile import read_image
from tools.parquet import read_image_bytes


DATAFOLDER = 'data/deep'
LABELS = 'data/labels.csv'

def get_rng():
    return np.random.default_rng(seed=10)


def shuffle_list(lst, rng):
    rng.shuffle(lst)

    
def shuffle_pandas(df, rng):
    index_shuffle = np.asarray(df.index)
    rng.shuffle(index_shuffle)
    return df.iloc[index_shuffle]


def read_parquet_sequential():

    pa_table = pq.read_table('data/deep.parquet')

    average_brightness = 0

    batches = pa_table.to_batches()

    i = 0

    for batch in batches:

        images = batch['Data'].to_pylist()

        for image_bytes in images:
            average_brightness += read_image_bytes(image_bytes).mean()

        i += 1

        if i%1000 == 0:
            print('Average brightness of %d images: %f' % (i, average_brightness / i))

    average_brightness /= len(pa_table)

    print(average_brightness)


def read_parquet_random():
    
    pa_table = pq.read_table('data/deep-random.parquet')

    average_brightness = 0

    batches = pa_table.to_batches()
    
    # Shuffle batches
    rng = get_rng()
    shuffle_list(batches, rng)

    i = 0

    order = []

    for batch in batches:

        order.extend(batch['index'].to_pylist())
        images = batch['Data'].to_pylist()    

        # Shuffle images
        shuffle_list(images, rng)

        for image_bytes in images:
            average_brightness += read_image_bytes(image_bytes).mean()

            i += 1

            if i%1000 == 0 and i>0:
                print('Average brightness of %d images: %f' % (i, average_brightness / i))

    average_brightness /= len(pa_table)

    print(average_brightness)

    print(order[:100])

    
def read_singlefile_sequential():

    labels = pd.read_csv(LABELS)

    labels['Fullpath'] = labels['Filename'].apply(lambda filename: os.path.join(DATAFOLDER, filename))

    average_brightness = 0

    for filename in labels['Fullpath']:
        average_brightness += read_image(filename).mean()

    average_brightness /= len(labels)
    print(average_brightness)

    
def read_singlefile_random():

    labels = pd.read_csv(LABELS)
    labels.reset_index(inplace=True)

    labels['Fullpath'] = labels['Filename'].apply(lambda filename: os.path.join(DATAFOLDER, filename))

    # Shuffle rows
    rng = get_rng()
    labels = shuffle_pandas(labels, rng)

    average_brightness = 0

    for i, filename in enumerate(labels['Fullpath']):
        average_brightness += read_image(filename).mean()
        if i%1000 == 0 and i>0:
            print('Average brightness of %d images: %f' % (i, average_brightness / i))

    average_brightness /= len(labels)
    print(average_brightness)

    print(list(labels.index)[:100])

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--order', choices=('sequential', 'random'), default='random', help='Iteration order')
    parser.add_argument('-t', '--type', choices=('singlefile', 'parquet'), default='singlefile', help='File type')
    parser.add_argument('-n', '--iterations', type=int, default=1, help='How many times the test should be run')
    
    args = parser.parse_args()
    
    order = args.order
    filetype = args.type
    iterations = args.iterations
    
    print('Running IO test for file type "%s" with %s access order.' % (filetype, order))
    
    for i in range(iterations):
        print('Running iteration %d' % i)
        exec("read_%s_%s()" % (filetype, order))