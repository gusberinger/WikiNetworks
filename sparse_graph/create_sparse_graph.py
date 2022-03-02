import logging
from helpers import *
import pandas as pd
import gzip

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
