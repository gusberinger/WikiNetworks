"""
Helper classes and methods.
"""
from pathlib import Path
import logging

logging.basicConfig(
	format='%(asctime)s %(levelname)-8s %(message)s',
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S')


WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'
ROOT_PATH = Path(__file__).parent
REPORT_PATH = ROOT_PATH.joinpath("report")
DUMP_PATH = ROOT_PATH.joinpath("dump")
DATABASE_PATH = DUMP_PATH.joinpath("sdow.sqlite")
SPARSE_MATRIX_PATH = DUMP_PATH.joinpath("sparse_mat.npz")
SPARSE_LABEL_PATH = DUMP_PATH.joinpath("labels.pickle")
TESTING_MATRIX_PATH = DUMP_PATH.joinpath("testing_matrix.pickle")
US_ARTICLE_ID = 3434750
WAYBACK_ID = 23538754
ISBN_ID = 14919

