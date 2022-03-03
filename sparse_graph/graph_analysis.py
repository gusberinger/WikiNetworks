from matplotlib.pyplot import connect
from helpers import *
import pickle
import scipy.sparse
import scipy.sparse.csgraph as cs 
import logging
from tqdm import tqdm
# import sknetwork as skn
from sknetwork.ranking import Closeness

with open(SPARSE_MATRIX_PATH, "rb") as f:
    mat = pickle.load(f)

closeness = Closeness(method="approximate")
seeds = {0:1}
scores = closeness.fit_transform(mat)
print(len(scores))
print(sorted(scores, reverse = True)[:100])

print(sum(scores))

# skn.sknetwork.ranking.PageRank(mat)

SIZE = mat.shape[0]

a = 5138150 # billboard top hits 1977
b = 24189148 # billboard top hits 1990
c = 1498512 # united states

# for i in range(SIZE):
#     # anarchism article row
#     print(mat[1, :].toarray())

# print(sum(mat[:, c].toarray()[0]))