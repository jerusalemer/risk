__author__ = 'art'

import matplotlib.pyplot as plt
import networkx as nx


def draw_board(board):

    graph = nx.Graph()

    edges = []
    node_colors = {0: 'red', 1: 'blue'}
    for node in board.nodes.values():
        graph.add_node(node.id)
        for neighbour in node.neighbours:
            edges.append((node.id, neighbour.id))

    for edge in edges:
        graph.add_edge(*edge)

    val_map = {0: 0.3, 1: 0.4}

    #values = [val_map.get(node.owner) for node in graph.nodes()]

    values = [((node) % 10  * 0.1, (node) % 10 * 0.1, (node) % 10 * 0.1 ) for node in graph.nodes()]

    print values

    nx.draw_networkx(graph)
    nx.draw(graph,node_color = values)
    plt.show()


