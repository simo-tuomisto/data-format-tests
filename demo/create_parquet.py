import os
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tools.shuffling import get_rng, shuffle_list, shuffle_pandas

from tools.parquet import file_to_bytes

DATAFOLDER = 'data/deep'
LABELS = 'data/labels.csv'
PARQUET_FILE = 'data/deep.parquet'
PARQUET_FILE_SHUFFLED = 'data/deep-shuffled.parquet'

def create_parquet(outputfile, shuffling=False):

    if os.path.isfile(outputfile):
        os.remove(outputfile)

    pqwriter = None

    labels = pd.read_csv(LABELS)
    labels.reset_index(inplace=True)
    
    if shuffling:
        print('Shuffling labels.')
        rng = get_rng()
        labels = shuffle_pandas(labels, rng)

    batch_size = 50
    nsplits = int(len(labels)/batch_size)+1
    print('Splitting %d labels to %d batches of %d.' % (len(labels), nsplits, batch_size))
    labels_split = np.array_split(labels, nsplits)

    for index, label_chunk in enumerate(labels_split):
        label_chunk['Fullpath'] = label_chunk['Filename'].apply(lambda filename: os.path.join(DATAFOLDER, filename))
        label_chunk['Data'] = label_chunk['Fullpath'].apply(lambda filename: file_to_bytes(filename))

        pa_labels = pa.Table.from_pandas(label_chunk)
        if index == 0:
            pqwriter = pq.ParquetWriter(outputfile, pa_labels.schema)
        pqwriter.write_table(pa_labels, row_group_size=batch_size)

    pqwriter.close()
    
if __name__=="__main__":
    
    print('Creating sequential dataset: %s' % PARQUET_FILE)
    create_parquet(PARQUET_FILE, shuffling=False)
    print('Creating shuffled dataset: %s' % PARQUET_FILE_SHUFFLED)
    create_parquet(PARQUET_FILE_SHUFFLED, shuffling=True)