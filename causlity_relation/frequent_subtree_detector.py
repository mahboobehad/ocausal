# In the name of Allah
from collections import Counter
from typing import Dict


class FrequentSubTreeDetector:
    def __init__(self, frequency_threshold=2):
        self.frequency_threshold = frequency_threshold

    def find_frequent_subtrees(self, sto_forest: Dict):
        number_of_trees = len(sto_forest)
        node_frequency_threshold = number_of_trees * self.frequency_threshold
        frequent_nodes = self.find_frequent_nodes(sto_forest, node_frequency_threshold)
        merge_target = frequent_nodes
        frequent_subtrees = list()

    @staticmethod
    def find_frequent_nodes(sto_forest: Dict, frequency_threshold):
        node_counter = Counter()
        for time_frame_trees in sto_forest:
            for tree in sto_forest[time_frame_trees]:
                for node in tree.nodes():
                    node_counter[node] += 1

        frequent_nodes = list(filter(lambda node: node_counter[node] > frequency_threshold, node_counter.keys()))
        return frequent_nodes
