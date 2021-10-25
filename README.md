# Data format tests

This repository contains some demo scripts and materials for a [Nordic-HPC](https://nordic-rse.org/) talk on [IO-profiling and optimization](https://nordic-rse.org/events/seminar-series/#october-i-o-profiling-and-optimization).

## Environment

The `environment.yml` can be used to create an Anaconda environment that can be used to run the demo. Environment might contain some extraneous packages.

## Demo

The `demo`-folder contains a demo that can be used to download [Deep Weeds dataset](https://github.com/AlexOlsen/DeepWeeds/), convert it into [Parquet](https://arrow.apache.org/docs/python/parquet.html)-format and test performance between using individual images and Parquet when going through the data in random or in sequential order.