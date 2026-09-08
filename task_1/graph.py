import networkx as nx
import matplotlib.pyplot as plt


def build_graph(
    edges: list[tuple],
    positions: dict[int, tuple],
    labels: dict[int, str]
) -> nx.DiGraph:
    G = nx.DiGraph()

    G.add_weighted_edges_from(edges)

    plt.figure(figsize=(10, 6))
    nx.draw(
        G,
        positions,
        with_labels=False,
        node_size=2000,
        node_color="skyblue",
        font_size=12,
        font_weight="bold",
        arrows=True
    )
    #labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, positions, edge_labels)
    nx.draw_networkx_labels(G, positions, labels=labels)

    # Відображаємо граф
    plt.show()

    return G