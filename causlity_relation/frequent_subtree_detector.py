# In the name of Allah
from collections import Counter
from typing import Dict, List, Optional, Set

import networkx as nx

from causlity_relation.exception import MalformedSTGraph


class FrequentSubTreeDetector:
    def __init__(self, sto_forest: List[nx.DiGraph], edge_incident: Dict[object, List],
                 frequency_threshold: float):
        self.edge_incident = edge_incident
        self.sto_forest = sto_forest
        number_of_trees = len(sto_forest)
        self.node_frequency_threshold = frequency_threshold * number_of_trees

    def find_frequent_subtrees(self, depth_limit=float("+inf")) -> Set[Optional[nx.DiGraph]]:
        frequent_nodes = self._find_frequent_sto()
        merge_targets = self._construct_frequent_forest(frequent_nodes)

        frequent_subtrees = set()
        depth = 0
        while len(merge_targets) > 0 and depth < depth_limit:
            depth += 1
            subtree_candidates = list()
            merged_trees = set()

            candidate_generated = False
            for to_be_merged in merge_targets:
                for node in to_be_merged.nodes:
                    for merge_target in merge_targets:
                        if self._insert_node(node, merge_target):
                            subtree_candidates.append(merge_target)
                            merged_trees.add(to_be_merged)
                            candidate_generated = True

            next_merge_trees = list()
            for candidate in subtree_candidates:
                count = 0
                for merge_target in merge_targets:
                    for node in merge_target:
                        if node in candidate.nodes:
                            count += 1
                if count >= self.node_frequency_threshold:
                    frequent_subtrees.add(candidate)
                    next_merge_trees.append(candidate)

            merge_targets.extend(next_merge_trees)

            for merged in merged_trees:
                merge_targets.remove(merged)

            if not candidate_generated:
                merge_targets = list()

        return frequent_subtrees

    def _find_frequent_sto(self) -> List[Optional[object]]:
        node_counter = Counter()

        for tree in self.sto_forest:
            for node in tree.nodes():
                node_counter[node.link_index] += 1

        frequent_nodes = list(
            filter(lambda node: node_counter[node] >= self.node_frequency_threshold, node_counter.keys()))
        return frequent_nodes

    def _insert_node(self, to_be_merged: object, tree, root=None) -> bool:
        if not root:
            root = self._find_root(tree)

        tree_root_destination = self.edge_incident[root][1]
        node_origin = self.edge_incident[to_be_merged][0]

        if tree_root_destination == node_origin and to_be_merged not in tree.nodes:
            tree.add_edge(root, to_be_merged)
            return True

        elif len(tree.nodes) == 1:
            return False

        else:
            for sub_node in self._find_sub_nodes(tree, root):
                if self._insert_node(to_be_merged, tree, sub_node):
                    return True

        return False

    @staticmethod
    def _find_root(tree: nx.DiGraph) -> object:
        if not nx.is_tree(tree):
            raise MalformedSTGraph("Graph is not a tree.")

        for node in tree.nodes():
            if tree.in_degree[node] == 0:
                return node

    @staticmethod
    def _find_sub_nodes(tree: nx.DiGraph, root):
        successors = list(dict(nx.bfs_successors(tree, root, depth_limit=1)).values())[0]
        return successors

    @staticmethod
    def _construct_frequent_forest(frequent_nodes) -> List[nx.DiGraph]:
        forest = list()
        for node in frequent_nodes:
            tree = nx.DiGraph()
            tree.add_node(node)
            forest.append(tree)

        return forest
