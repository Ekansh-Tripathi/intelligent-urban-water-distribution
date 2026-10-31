import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph):
    G = nx.DiGraph()

    for u in graph:
        for v in graph[u]:
            capacity = graph[u][v]
            G.add_edge(u, v, capacity=capacity)

    positions = {
        "S": (0, 2),
        "C1": (2, 4),
        "C2": (2, 2),
        "C4": (2, 0),
        "C3": (4, 4),
        "C5": (4, 2),
        "C6": (4, 0),
        "T": (6, 2)
    }

    nx.draw_networkx_nodes(
        G,
        positions,
        node_size=2200
    )

    nx.draw_networkx_labels(
        G,
        positions,
        font_size=12,
        font_weight="bold"
    )

    nx.draw_networkx_edges(
        G,
        positions,
        arrows=True,
        arrowsize=20,
        width=2
    )

    edge_labels = nx.get_edge_attributes(G, "capacity")

    nx.draw_networkx_edge_labels(
        G,
        positions,
        edge_labels=edge_labels,
        font_size=10
    )

    plt.title("Urban Water Distribution Network")
    plt.axis("off")
    plt.tight_layout()
    plt.show()