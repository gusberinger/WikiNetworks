import logging
from database import Database
import pickle
from helpers import *
import pandas as pd
import numpy as np
from multiprocessing import Pool

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


with open(MATRIX_INDEX_PATH, "rb") as f:
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
    # logging.info("Creating empty lil_matrix")


    # logging.info("Loading edge list dataframe")
    # there are approximately 562,142,540 total rows. For testing purposes it is time consuming to load all of them.


    db = Database(DATABASE_PATH)


    # Multiprocessing doesn't work correctly for chunks greater than 2GB
    LINKS_TABLE_SIZE = db.sdow_conn.execute("SELECT COUNT() FROM links").fetchone()[0]
    chunksize = LINKS_TABLE_SIZE // 6

    # order by descending so we can find out memory issues right away. 
    query = "SELECT id, outgoing_links FROM links where outgoing_links_count > 0 ORDER BY outgoing_links_count DESC"

    for i, edge_df_chunk in enumerate(pd.read_sql(query,
        db.sdow_conn,
        chunksize = chunksize)):

        lil_df = parallelize_dataframe(edge_df_chunk, links_df_to_matrix_df, n_cores=6)
        edge_df_chunk = None
        lil_df.to_parquet(DUMP_PATH.joinpath(f"lil_df-{i}.parquet"))
        logging.info("Processed chunck {i}.")

    
    glob = list(DUMP_PATH.glob("lil_df-*.parquet"))
    logging.info(f"Combining {len(glob)} parquet files.")
    df = pd.concat((pd.read_parquet(path) for path in glob))
    logging.info(f"Saving combined files.")
    df.to_parquet(DUMP_PATH.joinpath("lil_df.parquet"))
    logging.info("Removing sepearte parquet files.")
    for path in glob:
        path.unlink()
