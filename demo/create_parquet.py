import os
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from tools.parquet import file_to_bytes

imagefolder = 'data/deep'
labelsfile = 'data/labels.csv'
outputfile = 'data/deep.parquet'

if os.path.isfile(outputfile):
    os.remove(outputfile)

pqwriter = None

labels = pd.read_csv(labelsfile)
labels.reset_index(inplace=True)

batch_size = 50
nsplits = int(len(labels)/batch_size)+1
print('Splitting %d labels to %d batches of %d.' % (len(labels), nsplits, batch_size))
labels_split = np.array_split(labels, nsplits)

for index, label_chunk in enumerate(labels_split):
    label_chunk['Fullpath'] = label_chunk['Filename'].apply(lambda filename: os.path.join(imagefolder, filename))
    label_chunk['Data'] = label_chunk['Fullpath'].apply(lambda filename: file_to_bytes(filename))
    
    pa_labels = pa.Table.from_pandas(label_chunk)
    if index == 0:
        pqwriter = pq.ParquetWriter(outputfile, pa_labels.schema)
    pqwriter.write_table(pa_labels)

pqwriter.close()