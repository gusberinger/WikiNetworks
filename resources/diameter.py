from helpers import *
from sparse_graph import SparseGraph
import scipy.sparse as sp
from sknetwork.ranking import Katz
import matplotlib.pyplot as plt
import sknetwork.path

log = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    log.info("start")
    node_list = load_node_list()
    log.info("loaded node list")

    with open(SPARSE_MATRIX_PATH, "rb") as f:
        adj = sp.load_npz(f)
    graph = SparseGraph(adj, node_list)
    node_list = None
    subgraph = graph.get_largest_component()
    graph = None



    log.info("starting")
    results = sknetwork.path.diameter(subgraph.adjacency, 1000, n_jobs=1)
    log.info("done")
    print(results)

    