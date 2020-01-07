# In the name of Allah
from collections import Counter
from typing import Dict

import networkx as nx


class FrequentSubTreeDetector:
    def __init__(self, edge_incident, frequency_threshold=2):
        self.frequency_threshold = frequency_threshold
        self.edge_incident = edge_incident

    def find_frequent_subtrees(self, sto_forest: Dict):
        number_of_trees = len(sto_forest)
        node_frequency_threshold = number_of_trees * self.frequency_threshold
        frequent_nodes = self.find_frequent_nodes(sto_forest, node_frequency_threshold)
        merge_target = frequent_nodes
        frequent_subtrees = list()

        while len(merge_target) > 0:
            pass

    @staticmethod
    def find_frequent_nodes(sto_forest: Dict, frequency_threshold):
        node_counter = Counter()
        for time_frame_trees in sto_forest:
            for tree in sto_forest[time_frame_trees]:
                for node in tree.nodes():
                    node_counter[node] += 1

        frequent_nodes = list(filter(lambda node: node_counter[node] > frequency_threshold, node_counter.keys()))
        return frequent_nodes

    def insert_node(self, node, tree, root=None):
        if not root:
            root = self.find_root(tree)
        root_destination = self.edge_incident[root.link_index][1]
        node_origin = self.edge_incident[node.link_index][0]

        if root_destination == node_origin and node not in tree.nodes:
            tree.add_edge(root, node)
            return True

        elif len(tree.nodes) == 1:
            return False
        else:
            for sub_node in self.find_sub_nodes(tree, root):
                if self.insert_node(node, tree, sub_node):
                    return True

        return False

    @staticmethod
    def find_root(tree: nx.DiGraph):
        for node in tree.nodes:
            if node.in_degree == 0:
                return node

    @staticmethod
    def find_sub_nodes(tree: nx.DiGraph, root):
        successors = nx.dfs_successors(tree, root)
        return successors