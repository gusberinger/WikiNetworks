import numpy as np
import pandas as pd
from sortedcontainers import SortedList
from helpers import *
import pickle
import logging
from database import Database
import gzip

logging.getLogger().setLevel(logging.DEBUG)



db = Database(DATABASE_PATH)
pages_df = pd.read_sql("SELECT id FROM pages", db.sdow_conn)
logging.info("loaded pages sqlite databse")
nodes_list = SortedList(pages_df["id"])
logging.info("converted to SortedList")


with gzip.open(MATRIX_INDEX_PATH, "wb") as f:
    pickle.dump(nodes_list, f)

exit()




def id_key(wiki_id : int) -> int:
    try:
        return nodes_list.index(wiki_id)
    except ValueError:
        return np.nan



# Read data
# global memory usage after: one big array
df = pd.read_csv(EDGE_LIST_PATH, delimiter=',', header=None, dtype=np.uint32, nrows = 10 ** 4, names = ["source", "target"])
logging.info("Edge list loaded into database.")


df['source'] = df['source'].map(id_key)
logging.info("replaced all ids in source list")
df['target'] = df['target'].map(id_key)
logging.info("replaced all ids in target list")


# print(df.size)

# df = df.dropna()

# print(df.size)

# print(df.)
