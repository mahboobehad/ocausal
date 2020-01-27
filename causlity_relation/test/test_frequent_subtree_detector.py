# In the name of Allah
import pytest

from causlity_relation.frequent_subtree_detector import FrequentSubTreeDetector
from causlity_relation.outlier_tree_constructor import OutlierTreeConstructor
from causlity_relation.test.sto_forest_generator import sto_forest_test_case_generator
from data_pre_processing.random_data.random_data_generator import generate_random_stream, generate_random_graph
from outlier_detection.spatial_temporal_outlier_detector import SpatialTemporalOutlierDetector


class TestFrequentSubtreeDetector:
    def test_find_frequent_subtrees_integrated(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=5, link_count=10, observation_count=4)
        edge_incident = generate_random_graph(list(stream.keys()), 30)

        # assume all data points are outliers, check whether it is possible to find causality
        link_threshold = 0
        feature_threshold = 0
        outlier_detector = SpatialTemporalOutlierDetector(stream, link_threshold, feature_threshold)
        outliers = outlier_detector.find_all_outliers()
        assert len(outliers) != 0

        constructor = OutlierTreeConstructor(outliers, edge_incident)
        outlier_forest = constructor.construct_spatial_temporal_outlier_forest()

        assert len(outlier_forest) != 0

        frequency_threshold = .1
        frequent_subtree_detector = FrequentSubTreeDetector(outlier_forest, edge_incident, frequency_threshold)
        frequent_subtrees = frequent_subtree_detector.find_frequent_subtrees()
        assert len(frequent_subtrees) != 0

    @pytest.mark.parametrize("test_input,expected_forest", sto_forest_test_case_generator())
    def test_find_frequent_subtrees(self, test_input, expected_forest):
        forest, frequency_threshold, edge_incident = test_input
        detector = FrequentSubTreeDetector(forest, edge_incident, frequency_threshold)
        frequent_trees = detector.find_frequent_subtrees()

        assert len(frequent_trees) == len(expected_forest)
        for et in expected_forest:
            is_expected = False
            for ft in frequent_trees:
                is_expected |= et.adj == ft.adj
            assert is_expected is True
