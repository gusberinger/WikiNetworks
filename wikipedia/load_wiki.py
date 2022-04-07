from sparse import SparseGraph
from helpers import SPARSE_MATRIX_PATH, SPARSE_LABEL_PATH, DATABASE_PATH
import pickle
import sqlite3
import pandas as pd
import scipy.sparse


def load_wiki_labels(from_scratch=False) -> pd.DataFrame:
    # load pickled to avoid generating every time.
    if not from_scratch and SPARSE_LABEL_PATH.is_file():
        with open(SPARSE_LABEL_PATH, "rb") as f:
            return pickle.load(f)
    else:
        if not DATABASE_PATH.is_file():
            raise IOError('Specified SQLite file "{0}" does not exist.'.format(DATABASE_PATH))

        sdow_conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        labels_df = pd.read_sql("SELECT id, title FROM pages where is_redirect=0", sdow_conn)
        labels_df = labels_df.rename(columns={"id": "article_id"})
        labels_df = labels_df.sort_values(by=["article_id"])
        with open(SPARSE_LABEL_PATH, "wb") as f:
            pickle.dump(labels_df, f)
        return labels_df


def load_wikipedia(from_scratch=False) -> SparseGraph:
    labels = load_wiki_labels()
    print("loaded labels")
    with open(SPARSE_MATRIX_PATH, "rb") as f:
        matrix = scipy.sparse.load_npz(f)
    print("loaded adjacency")
    graph = SparseGraph(matrix, labels)
    print("created sparse graph")
    return graph
