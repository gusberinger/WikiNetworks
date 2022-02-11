import re
from helpers import *
from tqdm import tqdm

row_format = re.compile(r"^\d+,\d+$")

with open(EDGE_LIST_PATH, "r") as f:
    for line in tqdm(f):
        if not re.match(row_format, line):
            print(line)
