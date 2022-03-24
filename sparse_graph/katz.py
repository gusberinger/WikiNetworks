from helpers import *
from sparse_graph import SparseGraph
from scipy.sparse import load_npz
from sknetwork.ranking import Katz

log = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    log.info("start")
    node_list = load_node_list()
    print(node_list.find_title_from_article_id(US_ARTICLE_ID))
    log.info("loaded node list")

    with open(SPARSE_MATRIX_PATH, "rb") as f:
        adj = load_npz(f)
    graph = SparseGraph(adj, node_list)


    # graph[US_ARTICLE_ID]


    # node_list.remove_indices(range(10 ** 6))
    # adj = adj[10 ** 6 + 1: , 10 ** 6 + 1:]
    # print(adj.shape)
    # print(len(node_list.node_list))

    graph = SparseGraph(adj, node_list)
    graph.compute_degree()
    # sub_graph = graph.get_largest_component()
    # print(sub_graph.adjacency.shape)
    # sources = np.random.choice(np.arange(adj.shape[0]), 5, replace=False)

    close = Katz()
    log.info("calculating")
    scores = close.fit_transform(graph.adjacency)
    log.info("done")
    print(scores)

    log.info("matching articles")
    articles = [(node_list.find_article_id(i), score) for i, score in enumerate(scores)]
    articles_with_title = [(node_list.find_title_from_article_id(article_id), article_id, score) for article_id, score in articles]

    log.info("creating dataframe")
    df = pd.DataFrame(articles_with_title, columns = ["title", "article_id", "score"])
    df["in_degree"] = graph.in_degree
    df["out_degree"] = graph.out_degree
    
    log.info("saving dataframe")
    df.to_parquet(DUMP_PATH.joinpath("katz-centrality.parquet"))
    
    # df.to_parquet(DUMP_PATH.joinpath("katz-centrality.parquet"))