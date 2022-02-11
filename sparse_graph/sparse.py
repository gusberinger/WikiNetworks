import scipy.sparse as sp
import numpy as np
import pandas as pd
from pathlib import Path
from helpers import EDGE_LIST_PATH


# ROOT = Path(__file__).parent.parent
# EDGE_LIST_PATH = ROOT.joinpath("scripts", "dump", "edgelist.csv")


# Read data file and return sparse matrix in coordinate format
data = pd.read_csv(EDGE_LIST_PATH, sep=',', header=None, dtype=np.int32)
rows = data[0]  # Not a copy, just a reference.
cols = data[1]
ones = np.ones(len(rows), np.uint32)
print("start")
matrix = sp.coo_matrix((ones, (rows, cols)))
print("End")