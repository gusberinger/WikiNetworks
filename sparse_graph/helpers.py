"""
Helper classes and methods.
"""
import pickle
from pathlib import Path
import sqlite3
from typing import List
import pandas as pd
import numpy as np
import logging

logging.basicConfig(
	format='%(asctime)s %(levelname)-8s %(message)s',
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S')


WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'
ROOT_PATH = Path(__file__).parent.parent
DUMP_PATH = ROOT_PATH.joinpath("dump")
DATABASE_PATH = DUMP_PATH.joinpath("sdow.sqlite")
SPARSE_MATRIX_PATH = DUMP_PATH.joinpath("sparse_mat.npz")
NODES_LIST_PATH = DUMP_PATH.joinpath("nodes_list.pickle")

US_ARTICLE_ID = 3434750

class Database(object):
	def __init__(self):
		if not Path(DATABASE_PATH).is_file():
			raise IOError('Specified SQLite file "{0}" does not exist.'.format(DATABASE_PATH))
		self.sdow_conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
		self.sdow_cursor = self.sdow_conn.cursor()

class NodeList(object):
	def __init__(self, testing : bool = False) -> None:
		db = Database()
		if testing:
			node_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
		else:
			pages_df = pd.read_sql("SELECT id FROM pages where is_redirect=0", db.sdow_conn)
			node_list = sorted(pages_df["id"])
		node_dict = {article_id:index for index, article_id in enumerate(node_list)}
		self.node_dict = node_dict
		self.node_list = node_list

	def find_index(self, article_id : int, safe = True):
		if safe:
			try:
				return self.node_dict[article_id]
			except KeyError:
				return np.nan
		else:
			return self.node_dict[article_id]


	def find_article_id(self, index : int):
		return self.node_list[index]


	def remove_indices(self, indices : List[int]) -> None:
		"""Remove values from NodeList by index in place. The indexes are shifted down so the structure is maintained.
		That is, if index 2 is removed from [(0, A), (1, B), (2, C), (3, D)), (4, E), (5, F)] the new list becomes:
			[(0, A), (1, B), (2, D), (3, E), (4, F)]
		"""
		# ensure order of dataframe
		df = pd.DataFrame(self.node_dict.items(), columns = ["label", "index"])
		df = df.sort_values(by = ["index"])
		df = df.drop(indices, axis=0)
		node_list = list(df["label"])
		self.node_dict = {article_id:index for index, article_id in enumerate(node_list)}
		self.node_list = node_list

	def __len__(self):
		return len(self.node_dict.items())

def load_node_list():
	if Path(NODES_LIST_PATH).is_file():
		with open(NODES_LIST_PATH, "rb") as f:
			return pickle.load(f)
	else:
		logging.warning("Node list file not found. Generating...")
		node_list = NodeList()
		with open(NODES_LIST_PATH, "wb") as f:
			pickle.dump(node_list, f)
		return node_list


if __name__ == "__main__":
	node_list = NodeList(testing = True)
	node_list.remove_indices([2,3])
	print(node_list.node_dict)