from database import Database
from pathlib import Path
from scipy.sparse import csr_matrix
import numpy as np
import time
import itertools
from tqdm import tqdm

root = Path(__file__).parent.parent
database_path = root.joinpath("scripts", "dump", "sdow.sqlite")

db = Database(database_path)

db.depth_first_search(2731583)

