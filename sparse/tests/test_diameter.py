import networkx as nx
from sparse.diameter import estimate_diameter, estimate_radius
from sparse.random_graph import from_networkx

if __name__ == "__main__":
    nxG = nx.watts_strogatz_graph(1000, 10, .01, seed=12)
    G = from_networkx(nxG)
    estimate = estimate_radius(G, 10)
    real_diameter = nx.radius(nxG)
    print(estimate, real_diameter)
