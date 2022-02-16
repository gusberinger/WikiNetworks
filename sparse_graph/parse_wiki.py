from helpers import *
import mwxml
import re
import mwparserfromhell
from tqdm import tqdm
from collections import deque

XML_PATH = ROOT_PATH.joinpath("downloads", "enwiki-20220201-pages-articles-multistream1.xml-p1p41242", "enwiki-20220201-pages-articles-multistream1.xml-p1p41242")


external_links = re.compile(r"== {0,3}External links {0,3}==")

# wiki_links = re.compile(r"\[\[(?!.+?:)([^\]\[]+)(\|[^\]\[]+)?\]\]")
# wiki_links = re.compile(r"\[\[(.*?)\]\]")
wiki_links = re.compile(r"\[\[([^#\|]+?)(\|[^\]]+)?\]\]")

# mwparserfromhell.parse()
buffer = deque()

with open(XML_PATH, "r", encoding="latin-1") as f:
    dump = mwxml.Dump.from_file(f)
    for i, page in tqdm(enumerate(dump)):
        for revision in page:
            if revision.text.startswith("#REDIRECT"):
                continue
            links = re.findall(wiki_links, revision.text)
            outdegree = len(links)
            for link in links:
                buffer.append((page.id, link))
        