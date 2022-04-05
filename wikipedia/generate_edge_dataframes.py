"""
Convert the sqlite3 database into 200 edge lists dataframes where the edge corresponds to an index in the graph adjacency matrix.
"""

import logging
import pickle
from helpers import *
import pandas as pd
import numpy as np
from multiprocessing import Pool

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


with open(NODES_LIST_PATH, "rb") as f:
    nodes_list = pickle.load(f)


def id_key(wiki_id : int) -> int:
    try:
        return nodes_list.index(wiki_id)
    except ValueError:
        return np.nan



def links_df_to_matrix_df(df):
    df["outgoing_links"] = df["outgoing_links"].apply(lambda str: str.split("|"))
    df = df.explode("outgoing_links")
    df = df.astype(np.uint32)
    df['id'] = df['id'].apply(id_key)
    df['outgoing_links'] = df['outgoing_links'].apply(id_key)
    df = df.dropna()
    df = df.astype(np.uint32)
    return df

def parallelize_dataframe(df, func, n_cores=12):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

if __name__ == "__main__":

    db = Database()

    # Multiprocessing doesn't work correctly for chunks greater than 2GB due to python bug.
    # Split the process into six chunks to avoid memory errors.
    LINKS_TABLE_SIZE = db.sdow_conn.execute("SELECT COUNT() FROM links").fetchone()[0]
    chunksize = LINKS_TABLE_SIZE // 6

    # order by descending so we can find out memory issues right away. 
    query = "SELECT id, outgoing_links FROM links where outgoing_links_count > 0 ORDER BY outgoing_links_count DESC"

    for i, edge_df_chunk in enumerate(pd.read_sql(query,
        db.sdow_conn,
        chunksize = chunksize)):

        lil_df = parallelize_dataframe(edge_df_chunk, links_df_to_matrix_df, n_cores=6)
        edge_df_chunk = None
        lil_df.to_parquet(DUMP_PATH.joinpath(f"lil_df_temp-{i:03}.parquet"))
        logging.info(f"Processed chunk {i}.")

    
    # The file size will be unevenly distributed, so we combine them into one dataframe and then split them evenly.
    glob = list(DUMP_PATH.glob("lil_df_temp-*.parquet"))
    logging.info(f"Combining {len(glob)} parquet files.")
    df = pd.concat((pd.read_parquet(path) for path in glob))

    
    logging.info("Removing old parquet files.")
    for path in glob:
        path.unlink

    
    df_split = np.array_split(df, 100)
    df = None # not needed anymore

    for i, split in enumerate(df_split, 1):
        split.to_parquet(DUMP_PATH.joinpath("lil_df").joinpath(f"lil_df-{i:03}.parquet"))


