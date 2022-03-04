import logging
import pickle
import time
from helpers import *
import pandas as pd
import numpy as np
import scipy.sparse
from tqdm import tqdm

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def update_matrix(df, mat):
    for row in df.itertuples():
        mat[row.id, row.outgoing_links] = 1
    return mat

if __name__ == "__main__":
    with open(NODES_LIST_PATH, "rb") as f:
        size = len(pickle.load(f))

    logging.info(f"Creating empty graph of size {size:,}.")
    graph_matrix = scipy.sparse.csr_matrix((size, size))

    glob = list(DUMP_PATH.joinpath("lil_df").glob("lil_df-*.parquet"))
    for path in tqdm(glob):
        df = pd.read_parquet(path)
        # print(df.head())
        data = np.ones(df.shape[0])
        row = df["id"]
        col = df["outgoing_links"]
        mat = scipy.sparse.coo_matrix((data, (row, col)), shape=(size, size))
        mat = mat.tocsr()
        graph_matrix += mat
        mat = None

    logging.info("Casting graph type")
    

    scipy.sparse.save_npz(SPARSE_MATRIX_PATH, graph_matrix, compressed = False)