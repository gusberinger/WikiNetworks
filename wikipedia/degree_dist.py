import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import load_npz
from sparse_graph import SparseGraph
from helpers import *


def safe_log(n):
    if n == 0:
        return 0
    else:
        return math.log(n)


if __name__ == "__main__":
    adj = load_npz(SPARSE_MATRIX_PATH)
    node_list = load_node_list()
    graph = SparseGraph(adj, node_list)
    graph.compute_degree()
    x = graph.in_degree
    y = graph.out_degree
    
    x = np.vectorize(safe_log)(x)
    y = np.vectorize(safe_log)(y)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    # x, y = np.random.rand(2, 100) * 4
    hist, xedges, yedges = np.histogram2d(x, y, bins = 50)
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    print(np.matrix(hist))
    print(hist.shape)
    print(type(hist))

    zpos = 0

    # Construct arrays with the dimensions for the bars.
    dx = dy = 0.5 * np.ones_like(zpos)
    dz = hist.ravel()
    # print(dz)

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

    plt.show()