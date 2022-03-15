from helpers import *

if __name__ == "__main__":
    with open(TESTING_MATRIX_PATH, "rb") as f:
        adj, labels = pickle.load(f)

    print(adj.shape[0])


    def bread_first_search(source, target, adj):

        in_degree = sum

        if source == target:
            return [source]

        paths = []
        unvisited_forward = {source: [None]}
        unvisited_backward = {target: [None]}

        visited_forward = {}
        visited_backward = {}

        forward_depth = 0
        backward_depth = 0

        while len(paths) == 0 and len(unvisited_forward) != 0 and len(unvisited_backward) != 0:
            forward_count = 