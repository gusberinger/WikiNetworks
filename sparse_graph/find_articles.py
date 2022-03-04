import numpy as np
from helpers import *
import sys
import pickle

with open(NODES_LIST_PATH, "rb") as f:
    node_list = pickle.load(f)


def find_matrix_index(article_id : int, safe = True):
    if safe:
        try:
            return node_list.index(article_id)
        except ValueError:
            return np.nan
    else:
        return node_list.index(article_id) 


def find_article_id(matrix_index):
    return node_list[matrix_index]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Not correct input")
    print(node_list.index(int(sys.argv[1])))