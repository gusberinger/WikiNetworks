import igraph
import scipy.sparse
from load_wiki import load_wikipedia
from helpers import SPARSE_MATRIX_PATH
import logging

logging.basicConfig(
	format='%(asctime)s %(levelname)-8s %(message)s',
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

logging.info("start")
graph = load_wikipedia()
logging.info("done")