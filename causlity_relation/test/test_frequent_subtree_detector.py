# In the name of God
from causlity_relation.frequent_subtree_detector import FrequentSubTreeDetector
from outlier_detection.spatial_temporal_outlier_detector import SpatialTemporalOutlierDetector
from random_data_generator import generate_random_stream, generate_random_graph


class TestFrequentSubtreeDetector:
    def test_find_frequent_subtrees(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=10, link_count=4, observation_count=4)
        edge_incident = generate_random_graph(list(stream.keys()), 5)
        outlier_detector = SpatialTemporalOutlierDetector(stream, edge_incident)
        sto_forest = outlier_detector.construct_spatial_temporal_outlier_forest()
        frequent_subtree_detector = FrequentSubTreeDetector()
        frequent_subtrees = frequent_subtree_detector.find_frequent_subtrees(sto_forest)
        assert frequent_subtrees is not None
