# In the name of Allah
from typing import List, Dict
from collections import defaultdict

import networkx as nx

from outlier_detection.link_distortion_outlier_detector import LinkDistortionOutlierDetector
from outlier_detection.link_feature_outlier_detector import LinkFeatureOutlierDetector, FeatureOutlier
from random_data_generator import generate_random_stream, generate_random_graph


class SpatialTemporalOutlierDetector:
    def __init__(self, stream_time_frame: Dict, edge_incident: Dict):
        self.stream_time_frame = stream_time_frame
        self.observation_count = self._find_observation_count(stream_time_frame)
        self.edge_incident = edge_incident
        self.distortion_outlier_detector = LinkDistortionOutlierDetector(stream_time_frame)
        self.feature_outlier_detector = LinkFeatureOutlierDetector(stream_time_frame)

    def find_outliers(self, observation_index) -> List:
        temporal_outliers = self.distortion_outlier_detector.find_outliers(observation_index)
        spatial_outliers = self.feature_outlier_detector.find_outliers(observation_index)
        spatial_temporal_outliers = list(filter(lambda x: x.link_index in temporal_outliers, spatial_outliers))
        return spatial_temporal_outliers

    def construct_spatial_temporal_outlier_forest(self) -> Dict:
        st_outliers = [self.find_outliers(observation_index) for observation_index in range(self.observation_count)]
        trees = defaultdict(list)

        for time_frame in range(self.observation_count):
            for sto in st_outliers[time_frame]:
                sto_tree = self.construct_spatial_temporal_outlier_tree(sto, st_outliers, time_frame)
                if sto_tree:
                    trees[time_frame].append(sto_tree)

        return trees

    def construct_spatial_temporal_outlier_tree(self, sto: FeatureOutlier, st_outliers: List[FeatureOutlier],
                                                time_frame_index, tree=None):
        if not tree:
            tree = nx.DiGraph()

        if time_frame_index == self.observation_count - 1:
            return tree

        for next_sto in st_outliers[time_frame_index + 1]:
            sto_destination = self.edge_incident[sto.link_index][1]
            next_sto_origin = self.edge_incident[next_sto.link_index][0]
            if sto_destination == next_sto_origin:
                tree.add_node(sto)
                tree.add_node(next_sto)
                tree.add_edge(sto, next_sto)
                self.construct_spatial_temporal_outlier_tree(next_sto, st_outliers, time_frame_index + 1, tree)

    @staticmethod
    def _find_observation_count(stream_time_frame):
        for key in stream_time_frame.keys():
            return len(stream_time_frame[key])

