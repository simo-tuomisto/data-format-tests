import pyarrow.parquet as pq
from tools.parquet import read_image_bytes 

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