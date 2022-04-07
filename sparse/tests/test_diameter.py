import networkx as nx
from sparse.diameter import estimate_diameter

from sparse.random_graph import from_networkx

if __name__ == "__main__":
    nxG = nx.watts_strogatz_graph(1000, 10, .01, seed=10)
    G = from_networkx(nxG)
    # nx.draw_circular(nxG)
    # plt.show()
    d = estimate_diameter(G, 50)
    real_d = nx.diameter(nxG)
    print(real_d)
