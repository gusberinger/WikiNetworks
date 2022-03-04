"""
Helper classes and methods.
"""

import logging
import requests
from pathlib import Path
import sqlite3

WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'
ROOT_PATH = Path(__file__).parent.parent
DUMP_PATH = ROOT_PATH.joinpath("download_scripts", "dump")
DATABASE_PATH = DUMP_PATH.joinpath("sdow.sqlite")
SPARSE_MATRIX_PATH = DUMP_PATH.joinpath("sparse_mat.npz")
NODES_LIST_PATH = DUMP_PATH.joinpath("nodes_list.pickle")

class Database(object):
	def __init__(self):
		if not Path(DATABASE_PATH).is_file():
			raise IOError('Specified SQLite file "{0}" does not exist.'.format(DATABASE_PATH))
		self.sdow_conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
		self.sdow_cursor = self.sdow_conn.cursor()
