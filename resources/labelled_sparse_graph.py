from typing import Any, List
import numpy as np

class LabelledSparseGraph(object):

    def __init__(self, adjacency, labels : List[Any]) -> None:
        self.adjacency = adjacency
        self.labels = labels


    def find_index(self, article_id : int, safe = True):
        if safe:
            try:
                return self.labels.index(article_id)
            except ValueError:
                return np.nan
        else:
            return self.labels.index(article_id) 


    def find_article_id(self, index):
        return self.labels[index]