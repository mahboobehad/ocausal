# In the name of Allah
import networkx as nx

from causlity_relation.frequent_subtree_detector import FrequentSubTreeDetector
from outlier_detection.link_feature_outlier_detector import FeatureOutlier
from outlier_detection.spatial_temporal_outlier_detector import SpatialTemporalOutlierDetector
from random_data_generator import generate_random_stream, generate_random_graph


class TestFrequentSubtreeDetector:
    def test_find_frequent_subtrees(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=10, link_count=4, observation_count=4)
        edge_incident = generate_random_graph(list(stream.keys()), 5)

        outlier_detector = SpatialTemporalOutlierDetector(stream, edge_incident)
        sto_forest = outlier_detector.construct_spatial_temporal_outlier_forest()

        frequency_threshold = 3
        frequent_subtree_detector = FrequentSubTreeDetector(frequency_threshold)
        frequent_subtrees = frequent_subtree_detector.find_frequent_subtrees(sto_forest)
        assert len(frequent_subtrees) != 0

    def test_find_frequent_nodes(self):
        sto_list = [FeatureOutlier(0, 0, 0), FeatureOutlier(1, 0, 1)]
        t_1 = nx.DiGraph()
        t_1.add_edge(sto_list[0], sto_list[1])
        sto_forest = {0: [t_1, t_1]}
        frequency_threshold = 1
        frequent_subtree_detector = FrequentSubTreeDetector(frequency_threshold)
        frequent_subtrees = frequent_subtree_detector.find_frequent_nodes(sto_forest, 1)
        assert len(frequent_subtrees) != 0
