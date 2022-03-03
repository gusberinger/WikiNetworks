from helpers import *
import sys
import pickle

with open(MATRIX_INDEX_PATH, "rb") as f:
    node_list = pickle.load(f)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Not correct input")
    print(node_list.index(int(sys.argv[1])))
    print(node_list[0])