# Data format tests

This repository contains some demo scripts and materials for a [Nordic-HPC](https://nordic-rse.org/) talk on [IO-profiling and optimization](https://nordic-rse.org/events/seminar-series/#october-i-o-profiling-and-optimization).

## Environment

The `environment.yml` can be used to create an Anaconda environment that can be used to run the demo. Environment might contain some extraneous packages.

## Demo

The `demo`-folder contains a demo that can be used to download [Deep Weeds dataset](https://github.com/AlexOlsen/DeepWeeds/), convert it into [Parquet](https://arrow.apache.org/docs/python/parquet.html)-format and test performance between using individual images and Parquet when going through the data in random or in sequential order.

### Downloading the datasets

Downloading the dataset is done with the `download_datasets.py`-script:

```sh
python download_datasets.py
```

The dataset size is 505MB.

### Converting the dataset to parquet

Converting the dataset to Parquet is done using the `create_parquet.py`-script:

```sh
python create_parquet.py
```

This will create two 471MB parquet-files:

1. `data/deep.parquet`: Parquet-file with data stored in the same order as labels.
2. `data/deep-shuffled.parquet`: Parquet-file with data stored in random shuffled order.

### Testing the data loading from parquet vs loading from individual files

The `data-formats-demo.py`-script can be used to test how the data loading works from a parquet-file vs individual files.

The script simply calculates the average brightness of the images.
This is done just to verify that the data is actually loaded and used.

There are few flags to the script:
- `-o ORDER` or `--order ORDER`: The iteration order for the files. Choices: sequential or random.
- `-t TYPE` or `--type TYPE`: The file type to use. Choices: singlefile or parquet.
- `-n ITERATIONS` or `--iterations ITERATIONS`: Number of times the files should be read.

For timing and monitoring the I/O calls, `time` and `strace` are good tools.

Following calls should suit you the best:

1. Sequential access with individual files:

```sh
time strace -c -e trace=%file,open,read python data-formats-demo.py -o sequential -t singlefile
```

2. Sequential access with parquet-files:

```sh
time strace -c -e trace=%file,open,read python data-formats-demo.py -o sequential -t parquet
```

3. Randomized access with individual files:

```sh
time strace -c -e trace=%file,open,read python data-formats-demo.py -o random -t singlefile
```

4. Batch-randomized access with parquet-files:

```sh
time strace -c -e trace=%file,open,read python data-formats-demo.py -o random -t parquet
```