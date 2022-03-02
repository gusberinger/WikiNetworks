import numpy as np
from scipy.sparse import coo_matrix, save_npz
import pandas as pd
from sortedcontainers import SortedList
import time
from helpers import *
import pickle
from tqdm import tqdm

# file source: https://stackoverflow.com/questions/38688062/converting-a-1-2gb-list-of-edges-into-a-sparse-matrix



# Read data
# global memory usage after: one big array
df = pd.read_csv(EDGE_LIST_PATH, delimiter=',', header=None, dtype=np.uint32, nrows = 10 ** 7)
data = df.to_numpy()
df = None
n_edges = data.shape[0]

# Learn mapping to range(0, N_VERTICES)  # N_VERTICES unknown
# global memory usage after: one big array + one big searchtree
print('fit mapping')
start = time.time()
observed_vertices = SortedList()
mappings = np.arange(n_edges*2, dtype=np.uint32)  # upper bound on vertices
for column in range(data.shape[1]):
    for row in tqdm(range(data.shape[0])):
        # double-loop: slow, but easy to understand space-complexity
        val = data[row, column]
        if val not in observed_vertices:
            observed_vertices.add(val)
mappings = mappings[:len(observed_vertices)]
n_vertices = len(observed_vertices)
end = time.time()
print(' secs: ', end-start)

with open(OBSERVED_LIST_PATH, "wb") as f:
    pickle.dump(observed_vertices, f)

with open(MAPPINGS_PATH, "wb") as f:
    pickle.dump(mappings, f)

print('transform mapping')
# Map original data (in-place !)
# global memory usage after: one big array + one big searchtree(can be deleted!)
start = time.time()
for column in range(data.shape[1]):
    for row in tqdm(range(data.shape[0])):
        # double-loop: slow, but easy to understand space-complexity
        val = data[row, column]
        mapper_pos = observed_vertices.index(val)
        data[row, column] = mappings[mapper_pos]
end = time.time()
print(' secs: ', end-start)
observed_vertices = None  # if not needed anymore
mappings = None  # if not needed anymore

# Create sparse matrix (only caring about a single triangular part for now)
# if needed: delete dictionary before as it's not needed anymore!
sp_mat = coo_matrix((np.ones(n_edges, dtype=bool), (data[:, 0], data[:, 1])), shape=(n_vertices, n_vertices))
save_npz(SPARSE_MATRIX_PATH.parent.joinpath("spmat.npz"), sp_mat, compressed=True)

with open(SPARSE_MATRIX_PATH, "wb") as f:
    pickle.dump(sp_mat, f)