import logging
import pickle

from helpers import *
import pandas as pd
import numpy as np
import scipy.sparse
from tqdm import tqdm

# import numpy as np
from multiprocessing import cpu_count, Pool
 
cores = cpu_count() #Number of CPU cores on your system
partitions = cores

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

with open(MATRIX_INDEX_PATH, "rb") as f:
    nodes_list = pickle.load(f)

MATRIX_SIZE = len(nodes_list)

def id_key(wiki_id : int) -> int:
    try:
        return nodes_list.index(wiki_id)
    except ValueError:
        return np.nan


def convert_df(df):
    df['source'] = df['source'].apply(id_key)
    df['target'] = df['target'].apply(id_key)
    df = df.dropna()
    df = df.astype(np.uint32)
    return df

def parallelize_dataframe(df, func, n_cores=12):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    # df = pool.map(func, df_split)
    pool.close()
    pool.join()
    return df

import time

if __name__ == "__main__":

    logging.info("Loading edge list dataframe")
    edge_df = pd.read_csv(EDGE_LIST_PATH, delimiter=',', header=None, dtype=np.uint32, nrows = 10 ** 7, names = ["source", "target"])


    logging.info("converting wiki ids to matrix indices")
    lil_df = parallelize_dataframe(edge_df, convert_df)
    print(lil_df.shape)
    # print(lil_df)
    print(f"{time.time() - t0} seconds")
    exit()

    # df = df.astype(np.uint32)
    logging.info("removed null edges")



    logging.info("creating sparse matrix")
    mat = scipy.sparse.lil_matrix((MATRIX_SIZE, MATRIX_SIZE))
    for row in tqdm(edge_df.itertuples()):
        mat[row.source, row.target] = 1


    with open(SPARSE_MATRIX_PATH, "wb") as f:
        pickle.dump(mat, f)
