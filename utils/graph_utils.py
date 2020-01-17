# In the name of Allah
import matplotlib.pyplot as plt
import networkx as nx


def plot_sto_tree(tree: nx.DiGraph):
    pos = nx.spring_layout(tree)
    labels = {node: "link: " + str(node.link_index) + ", " + "tf: " + str(node.observation_index) for node in
              pos.keys()}
    nx.draw_networkx_nodes(tree, pos)
    nx.draw_networkx_edges(tree, pos)
    nx.draw_networkx_labels(tree, pos, labels, font_size=10)
    plt.draw()
    plt.show()

