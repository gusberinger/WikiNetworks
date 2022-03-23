import enum
from typing import Dict
from numpy import indices

from tqdm import tqdm
from helpers import *
from sparse_graph import SparseGraph
import scipy.sparse as sp
import queue

log = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


# WAY TO SLOW
# def breadth_first_search_level(graph : 'SparseGraph', node : int) -> Dict[int, int]:
#     visited = {node}
#     level = {node : 0}
#     n = graph.adjacency.shape[0]

#     q = queue.Queue()
#     q.put(node)
#     i = 0

#     with tqdm(total = n) as pbar: 
#         while not q.empty():
#             v = q.get()
#             pbar.update(1)
#             neighbors = graph.incoming_neighbors(v)
#             for w in neighbors:
#                 if w not in visited:
#                     q.put(w)
#                     level[w] = level[v] + 1
#                     visited.add(w)
#     return level


def breadth_first_search_level(graph : 'SparseGraph', start_node : int) -> Dict[int, int]:
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




if __name__ == "__main__":
    log.info("start")
    node_list = load_node_list()
    log.info("loaded node list")

    with open(SPARSE_MATRIX_PATH, "rb") as f:
        adj = sp.load_npz(f)
    graph = SparseGraph(adj, node_list)
    node_list = None
    
    log.info("finding subgraph")
    # subgraph = graph.get_largest_component()
    subgraph = graph
    us_index = subgraph.labels.find_index(US_ARTICLE_ID)
    log.info("got subgraph")

    log.info("Finding levels")
    levels = breadth_first_search_level(subgraph, us_index)
    log.info("Done")
    print(levels)

    df = pd.DataFrame(enumerate(levels), columns=["node", "level"])
    print(df.head())
    df.to_parquet(DUMP_PATH.joinpath("us_levels.parquet"))




    # df = pd.DataFrame(levels.items(), columns = ["node", "level"], dtype=np.uint32)
    # print(df.head())
    # df.to_parquet(DUMP_PATH.joinpath("us_levels.parquet"))