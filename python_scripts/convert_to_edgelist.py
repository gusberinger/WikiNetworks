from pathlib import Path
from database import Database
from tqdm import tqdm
from collections import deque
from helpers import *
import random

ROW_COUNT = 6464930

# start with empty edge list
if EDGE_LIST_PATH.is_file():
    EDGE_LIST_PATH.unlink()

db = Database(DATABASE_PATH)
db.sdow_cursor.execute("SELECT id, outgoing_links, outgoing_links_count FROM links")

buffer = deque()

# def write_buffer(buffer):
#     with open(ROOT.joinpath("scripts", "dump", f"edgelist-{random.randint(1000, 9999)}.csv"), "a") as f:
#         f.write("\n".join(buffer))


def write_buffer(buffer):
    with open(ROOT.joinpath(EDGE_LIST_PATH), "a") as f:
        f.write("\n".join(buffer))
        f.write("\n")

for i, row in tqdm(enumerate(db.sdow_cursor, 1), total = ROW_COUNT):
    page_id, links_str, outgoing_links_count = row
    
    # no edges exist
    if outgoing_links_count == 0:
        continue

    links_lst = links_str.split("|")
    for link in links_lst:
        buffer.append(f"{page_id},{link}")

    if i % (10 ** 6) == 0:
        write_buffer(buffer)
        buffer = deque()

write_buffer(buffer)
