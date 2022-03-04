"""
Helper classes and methods.
"""

from pathlib import Path
import sqlite3
from typing import List
import pandas as pd
import numpy as np


WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'
ROOT_PATH = Path(__file__).parent.parent
DUMP_PATH = ROOT_PATH.joinpath("dump")
DATABASE_PATH = DUMP_PATH.joinpath("sdow.sqlite")
SPARSE_MATRIX_PATH = DUMP_PATH.joinpath("sparse_mat.npz")
NODES_LIST_PATH = DUMP_PATH.joinpath("nodes_list.pickle")

class Database(object):
	def __init__(self):
		if not Path(DATABASE_PATH).is_file():
			raise IOError('Specified SQLite file "{0}" does not exist.'.format(DATABASE_PATH))
		self.sdow_conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
		self.sdow_cursor = self.sdow_conn.cursor()


class NodeList(object):
	def __init__(self) -> None:
		db = Database()

		pages_df = pd.read_sql("SELECT id FROM pages where is_redirect=0", db.sdow_conn)
		node_list = sorted(pages_df["id"])
		node_dict = {k:v for k, v in enumerate(node_list)}

		self.node_dict = node_dict

	def find_index(self, article_id : int, safe = True):
		if safe:
			try:
				return self.labels.index(article_id)
			except ValueError:
				return np.nan
		else:
			return self.labels.index(article_id) 


	def find_article_id(self, index : int):
		return self.labels[index]


	def remove_indices(self, indices : List[int]) -> None:
		"""Remove values from NodeList by index in place. The indexes are shifted down so the structure is maintained.
		That is, if index 2 is removed from [(0, A), (1, B), (2, C), (3, D)), (4, E), (5, F)] the new list becomes:
			[(0, A), (1, B), (2, D), (3, E), (4, F)]
		"""
		node_list = self.node_dict.values()
		node_list = np.delete(node_list, indices)
		self.node_dict = {k:v for k, v in enumerate(node_list)}


if __name__ == "__main__":
	node_list = NodeList()