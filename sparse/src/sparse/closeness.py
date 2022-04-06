from __future__ import annotations
import pandas as pd
import numpy as np
from typing import Dict
from tqdm import tqdm


def distance_from(graph, start_node : int) -> Dict[int, int]:
    """Breadth first search."""
    N = graph.adjacency.shape[0]
    predecessors = np.empty(N, dtype=int)
    node_list =  np.empty(N, dtype=int)
    levels = np.empty(N, dtype=int)
    indptr = graph.adjacency.indptr
    indices = graph.adjacency.indices

    predecessors.fill(-1)
    node_list.fill(-1)
    levels.fill(-1)

    node_list[0] = start_node
    levels[start_node] = 0
    i_nl = 0
    i_nl_end = 1

    pbar = tqdm(total=N)
    while i_nl < i_nl_end:
        pnode = node_list[i_nl]
        pbar.update(1)
        for i in range(indptr[pnode], indptr[pnode + 1]):
            cnode = indices[i]
            if (cnode == start_node):
                continue
            elif (predecessors[cnode] == -1):
                node_list[i_nl_end] = cnode
                predecessors[cnode] = pnode
                levels[cnode] = levels[pnode] + 1
                i_nl_end += 1
        i_nl += 1
    pbar.close()
    return levels