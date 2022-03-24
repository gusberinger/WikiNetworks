import logging
import pickle
from re import sub
import sqlite3
from typing import Any, List, Optional, Union
import pandas as pd
from scipy import sparse
from scipy.sparse import load_npz
import numpy as np
from helpers import *

log = logging.getLogger(__name__)




class SparseLabels:
	
	def __init__(self, new_df) -> None:

		self._internal_df = new_df
		article_id_from_index_dict = dict(zip(new_df.index, new_df["article_id"]))
		title_from_index_dict = dict(zip(new_df.index, new_df["title"]))
		index_from_article_id_dict = {v:k for k, v in article_id_from_index_dict.items()}

		self.find_index_from_article_id = index_from_article_id_dict.get
		self.find_article_id_from_index = article_id_from_index_dict.get
		self.find_title_from_index = title_from_index_dict.get
		self.find_title_from_article_id = dict(zip(new_df["article_id"], new_df["title"])).get
		
	def remove_indices(self, indices) -> 'SparseLabels':
		new_df = self._internal_df.drop(indices, axis = 0)
		return SparseLabels(new_df)


def load_wiki_labels(from_scratch = False) -> 'SparseLabels':

	# load pickled to avoid generating every time. 
	if not from_scratch and Path(SPARSE_LABEL_PATH).is_file():
		with open(SPARSE_LABEL_PATH, "rb") as f:
			return pickle.load(f)
	else:
		log.warning("Node list file not found. Generating...")
		
		if not Path(DATABASE_PATH).is_file():
			raise IOError('Specified SQLite file "{0}" does not exist.'.format(DATABASE_PATH))
			
		sdow_conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
		labels_df = pd.read_sql("SELECT id, title FROM pages where is_redirect=0", sdow_conn)
		labels_df = labels_df.rename(columns={"id": "article_id"})
		print(labels_df.head())
		labels_df = labels_df.sort_values(by = ["article_id"])

		labels = SparseLabels(labels_df)

		with open(SPARSE_LABEL_PATH, "wb") as f:
			pickle.dump(labels, f)
		
		return labels

def load_wiki_graph():
	


def _delete_from_csr(mat, indices : List[int]):
	"""
	Parameters
	---
	mat:
		The csr sparse adjacency matrix of the graph.
	indices:
		The indices of the nodes in the graph that will be removed.

	Returns
	---
	mat:
		The sparse adjacency matrix of the graph with the nodes removed.
	"""
	if mat.shape[0] != mat.shape[1]:
		raise ValueError("Matrix must be square.")

	mask = np.ones(mat.shape[0], dtype=bool)
	mask[indices] = False
	return mat[mask][:,mask]

class SparseGraph:

	def __init__(self, adjacency, labels) -> None:
		self.adjacency = adjacency
		self.labels = labels
		self.in_degrees = None
		self.out_degrees = None

	def get_largest_component(self, directed : bool = True, connection : str = "strong") -> 'SparseGraph':
		"""
		Parameters
		---
		matrix:
			The sparse adjacency matrix of the graph.
		labels:
			The labels of each node in the graph. The index of the list corresponds to the index in the adjacency matrix.
		direct:
			If ``True`` the graph is treated as directed. 
		connection:
			If ``"strong"``, the connected components will all be strongly connected together, if ``"weak"`` the connected components will be weakly connected. If ``directed == False`` the parameter is ignored.

		Returns
		---
		sub_matrix:
			The sparse adjacency matrix of the largest strongly connected subgraph.
		sub_labels:
			The labels of each node in the subgraph.
		"""
		_, component_labels = sparse.csgraph.connected_components(self.adjacency, directed=directed, connection=connection)
		unique_component_labels, count = np.unique(component_labels, return_counts=True)
		largest = unique_component_labels[np.argmax(count)]
		indices = np.where(component_labels == largest)[0]
		unconnected_indices = list(set(range(self.adjacency.shape[0])) - set(indices))
		new_labels = self.remove_indices(unconnected_indices)
		sub_matrix = _delete_from_csr(self.adjacency, unconnected_indices)
		subgraph = self.remove_indices(sub_matrix, new_labels)
		return subgraph

	def compute_degree(self) -> None:
		"""
		Fills in the degrees for self.in_degree and self.out_degree
		"""
		self.in_degree = np.array(np.sum(self.adjacency, axis = 0))[0]
		self.out_degree = np.array(np.sum(self.adjacency, axis = 1).transpose())[0]
		

	def outgoing_neighbors(self, index : int) -> list[int]:
		nodes = self.adjacency[index,:].toarray()[0]
		return np.nonzero(nodes)[0]

	def incoming_neighbors(self, index : int) -> list[int]:
		nodes = self.adjacency[:, index].toarray()[0]
		return np.nonzero(nodes)[0]

	def remove_indices(self, indices : List[int]) -> 'SparseGraph':
		new_adjacency = _delete_from_csr(self.adjacency, indices)
		new_labels = self.labels.remove_indices(indices)
		return SparseGraph(new_adjacency, new_labels)




if __name__ == "__main__":
	# US_ARTICLE_ID = 12
	adj = load_npz(SPARSE_MATRIX_PATH)
	labels = load_wiki_labels()
	graph = SparseGraph(adj, labels)
	log.info("Imported graph")
	graph.compute_degree()
	log.info("Computed degree")
	us_index = graph.labels.find_index_from_article_id(US_ARTICLE_ID)
	print(graph.in_degree[us_index])
	
