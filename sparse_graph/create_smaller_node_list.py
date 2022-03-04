"""
The goal of this module is to identify the highly connected components separate them into a smaller subgraph. This is because several algorithms we want to use involve the 
"""

from cProfile import label
import numpy as np
from helpers import *
import pickle
import scipy.sparse
import scipy.sparse.csgraph as cs 
import logging
from tqdm import tqdm
import find_from_big
from sortedcontainers import SortedList
import sknetwork as skn
import sknetwork.topology
US_PAGE_ID = 3434750



# print(US_PAGE_ID)

# with open(NODES_LIST_PATH, "rb") as f:
#     nodes_list = pickle.load(f)

US_INDEX = find_from_big.find_matrix_index(US_PAGE_ID)


# by hypothesis, every highly connected node can be reached from the united states. 
mat = scipy.sparse.load_npz(SPARSE_MATRIX_PATH)


if __name__ == "__main__":
    n_components, labels = cs.connected_components(mat, directed = True, connection="strong")
    unique_labels, counts = np.unique(labels, return_counts=True)
    
    # lets find an article that is in the 2nd largest strongly connected component
    index_largest = np.argsort(counts, axis=0)[-1]
    largest_component = unique_labels[index_largest]
    # size = np.count_nonzero(labels == largest_component)
    # print(size, size / mat.shape[0])
    # label_index = unique_labels.find(largest_component)
    label_index = np.where(unique_labels == largest_component)
    
    
    # article_id = find_from_big.find_article_id(label_index)
    print(label_index)
    print(type(label_index))
    