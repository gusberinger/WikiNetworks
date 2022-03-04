import pandas as pd
from sortedcontainers import SortedList
from helpers import *
import pickle


if __name__ == "__main__":

    db = Database()

    pages_df = pd.read_sql("SELECT id FROM pages where is_redirect=0", db.sdow_conn)
    nodes_list = SortedList(pages_df["id"])

    with open(NODES_LIST_PATH, "wb") as f:
        pickle.dump(nodes_list, f)

