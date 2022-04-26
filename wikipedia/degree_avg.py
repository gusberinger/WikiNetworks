from load_wiki import load_wikipedia
import numpy as np
from helpers import ISBN_ID


def report(lst):
    print(f"Mean: {np.mean(lst)}")
    print(f"Median: {np.median(lst)}")
    print(f"Length: {len(lst)}")
    print(f"Standard Deviation: {np.std(lst)}")



if __name__ == "__main__":
    G = load_wikipedia()
    G.compute_degree()
    print("out_degree:\n" + "-" * 10)
    report(G._out_degree)
    print("\nin_degree:\n" + "-" * 10)
    report(G._in_degree)

    print("\n" * 2)
    isbn_index = G.labels.find_index_from_article_id(ISBN_ID)
    print(G.labels.find_title_from_index(isbn_index))
    print(f"ISBN indegree: {G.in_degree(isbn_index)} ")
    print(f"ISBN outdegree: {G.out_degree(isbn_index)} ")


