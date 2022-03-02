import pandas as pd
from sortedcontainers import SortedList
from helpers import *
import pickle
import logging
from database import Database

logging.getLogger().setLevel(logging.DEBUG)

db = Database(DATABASE_PATH)
pages_df = pd.read_sql("SELECT id FROM pages", db.sdow_conn)
logging.info("loaded pages sqlite databse")
nodes_list = SortedList(pages_df["id"])
logging.info("converted to SortedList")


with open(MATRIX_INDEX_PATH, "wb") as f:
    pickle.dump(nodes_list, f)

logging.info("created node list file")

