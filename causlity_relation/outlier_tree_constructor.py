# In the name of Allah
from typing import Optional, Dict, List, Union

import networkx as nx

from causlity_relation.exception import MalformedSpatialTemporalOutlierList
from outlier_detection.link_feature_outlier_detector import FeatureOutlier


class OutlierTreeConstructor:
    def __init__(self, spatial_temporal_outliers: List[List[FeatureOutlier]], edge_incident: Dict):
        self.edge_incident = edge_incident
        self.spatial_temporal_outliers = spatial_temporal_outliers

    def construct_spatial_temporal_outlier_forest(self) -> List[Optional[nx.DiGraph]]:

        if len(self.spatial_temporal_outliers) < 2:
            raise MalformedSpatialTemporalOutlierList("More observation is required.")

        forest = list()

        for time_frame_index in range(len(self.spatial_temporal_outliers)):
            for sto in self.spatial_temporal_outliers[time_frame_index]:
                sto_tree = self._construct_spatial_temporal_outlier_tree(sto, time_frame_index)
                if sto_tree:
                    forest.append(sto_tree)

        return forest

    def _construct_spatial_temporal_outlier_tree(self, sto: FeatureOutlier, time_frame_index, tree=None) -> \
            Optional[nx.DiGraph]:

        if time_frame_index == len(self.spatial_temporal_outliers) - 1:
            return tree

        pruning_allowed = False
        for next_sto in self.spatial_temporal_outliers[time_frame_index + 1]:
            sto_destination = self.edge_incident[sto.link_index][1]
            next_sto_origin = self.edge_incident[next_sto.link_index][0]
            can_grow = sto_destination == next_sto_origin
            pruning_allowed |= not can_grow
            if can_grow:
                if not tree:
                    tree = nx.DiGraph()
                tree.add_edge(sto, next_sto)
                return self._construct_spatial_temporal_outlier_tree(next_sto, time_frame_index + 1, tree)
        else:
            if pruning_allowed:
                return tree
