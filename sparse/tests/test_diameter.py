import networkx as nx
from sparse.diameter import estimate_diameter
from sparse.random_graph import from_networkx

if __name__ == "__main__":
    nxG = nx.watts_strogatz_graph(1000, 10, .01, seed=10)
    G = from_networkx(nxG)
    estimate = estimate_diameter(G, 100)
    real_diameter = nx.diameter(nxG)
    print(estimate, real_diameter)
