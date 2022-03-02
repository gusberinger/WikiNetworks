import logging
import pickle
from helpers import *
import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix
from tqdm import tqdm
from multiprocessing import Pool

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


def wiki_df_to_matrix_df(df):
    df['source'] = df['source'].apply(id_key)
    df['target'] = df['target'].apply(id_key)
    df = df.dropna()
    df = df.astype(np.uint32)
    return df


def dense_df_to_sparse(df):
    mat = lil_matrix((MATRIX_SIZE, MATRIX_SIZE))
    for row in df.itertuples():
        mat[row.source, row.target] = 1
    mat = mat.tocsr()
    return mat


def parallelize_dataframe(df, func, n_cores=12):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def parallelize_matrix_creation(df, n_cores=12):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    mat = sum(pool.map(dense_df_to_sparse, df_split))
    pool.close()
    pool.join()
    return mat




if __name__ == "__main__":
    # logging.info("Creating empty lil_matrix")
    # EMPTY_MAT = scipy.sparse.lil_matrix((MATRIX_SIZE, MATRIX_SIZE))

    logging.info("Loading edge list dataframe")

    # there are approximately 562,142,540 total rows. For testing purposes it is time consuming to load all of them.
    edge_df = pd.read_csv(EDGE_LIST_PATH, 
        delimiter=',', 
        header=None, 
        names = ["source", "target"],
        dtype=np.uint32, 
        nrows = 10 ** 7) 

    logging.info("converting wiki ids to matrix indices")
    lil_df = parallelize_dataframe(edge_df, wiki_df_to_matrix_df)
    edge_df = None
    logging.info("done.")


    mat = dense_df_to_sparse(lil_df)
    # mat = parallelize_matrix_creation(lil_df)
    # print(type)

    logging.info("created sparse matrix")
    logging.info("done.")
    with open(SPARSE_MATRIX_PATH, "wb") as f:
        pickle.dump(mat, f)
