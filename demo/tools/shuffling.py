import numpy as np
import pandas as pd

def get_rng():
    return np.random.default_rng(seed=10)


def shuffle_list(lst, rng):
    rng.shuffle(lst)

    
def shuffle_pandas(df, rng):
    index_shuffle = np.asarray(df.index)
    rng.shuffle(index_shuffle)
    return df.iloc[index_shuffle]