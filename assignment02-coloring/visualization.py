#!/usr/bin/python
# -*- coding: utf-8 -*-


def draw_graph(node_count, edges, color):
    import networkx as nx
    import matplotlib.pyplot as plt
    G=nx.Graph()
    G.add_nodes_from(range(node_count))
    G.add_edges_from(edges)

    pos=nx.spring_layout(G)

    nx.draw(G,pos, node_color = color)
    nx.draw_networkx_labels(G,pos,{k:k for k in range(node_count)})

    plt.show()
