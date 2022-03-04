# from sortedcontainers import SortedList
from os import link
from helpers import *
import mwxml
import re
from tqdm import tqdm
from collections import deque
import pandas as pd
from database import Database

XML_PATH = ROOT_PATH.joinpath("downloads", "enwiki-20220201-pages-articles-multistream1.xml-p1p41242", "enwiki-20220201-pages-articles-multistream1.xml-p1p41242")


pages_df = pd.read_csv(DUMP_PATH.joinpath("pages_data.csv"), 
    compression="gzip",
    dtype={"id":str})
print(pages_df.head())

# print("CONVERTING TO NUMPY...")
# numpy_list = df["title"].to_numpy()
print("CONVERTING TO DICTIONARY")
# pages = SortedList(numpy_list)
pages_dict = pd.Series(pages_df.id.values, index = pages_df.title).to_dict()

print(pages_dict["anarchist_organisations"])
del pages_df
# del numpy_list


WIKI_LINKS_REGEX = re.compile(r"\[\[([^#\|]+?)(?:\|[^\]]+)?\]\]")


# def write_buffer():
    # with open(DUMP_PATH.joinpath(""))

buffer = deque()
with open(XML_PATH, "r", encoding="latin-1") as f:
    dump = mwxml.Dump.from_file(f)
    for i, page in tqdm(enumerate(dump)):
        for revision in page:
            if revision.text.startswith("#REDIRECT"):
                continue

            links_all = re.findall(WIKI_LINKS_REGEX, revision.text)
            links_all = [link.lower() for link in links_all]
            links = [pages_dict[link] for link in links_all if link in pages_dict.keys()]
            links_str = f"{page.id}\t" + "|".join(links)
            # print(links_str)

            # if i % 10 ** 4 == 0:
                