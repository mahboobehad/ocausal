# In the name of Allah
import networkx as nx
import pytest

from causlity_relation.frequent_subtree_detector import FrequentSubTreeDetector
from causlity_relation.outlier_tree_constructor import OutlierTreeConstructor
from data_pre_processing.random_data.random_data_generator import generate_random_stream, generate_random_graph
from outlier_detection.link_feature_outlier_detector import FeatureOutlier
from outlier_detection.spatial_temporal_outlier_detector import SpatialTemporalOutlierDetector


class TestFrequentSubtreeDetector:
    @pytest.mark.skip("Test is time consuming, optimization is required.")
    def test_find_frequent_subtrees_integrated(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=5, link_count=4, observation_count=4)
        edge_incident = generate_random_graph(list(stream.keys()), 5)
        # assume all data points are outlier, check whether it is possible to find causality
        link_threshold = 0
        feature_threshold = 0
        outlier_detector = SpatialTemporalOutlierDetector(stream, link_threshold, feature_threshold)
        outliers = outlier_detector.find_all_outliers()
        constructor = OutlierTreeConstructor(outliers, edge_incident)
        outlier_forest = constructor.construct_spatial_temporal_outlier_forest()

        frequency_threshold = 1
        frequent_subtree_detector = FrequentSubTreeDetector(outlier_forest, edge_incident, frequency_threshold)
        frequent_subtrees = frequent_subtree_detector.find_frequent_subtrees()
        assert len(frequent_subtrees) != 0

    def test_find_frequent_subtrees(self):
        # TODO: parametrize the test

        sto_list = [FeatureOutlier(1, 0, 0), FeatureOutlier(5, 1, 1), FeatureOutlier(6, 0, 2),
                    FeatureOutlier(4, 0, 1), FeatureOutlier(2, 0, 0), FeatureOutlier(3, 0, 1),
                    FeatureOutlier(3, 0, 0), FeatureOutlier(4, 0, 2), FeatureOutlier(3, 0, 3),
                    FeatureOutlier(4, 1, 4)]

        # construction of first tree
        t1 = nx.DiGraph()
        t1.add_edge(sto_list[0], sto_list[1])
        t1.add_edge(sto_list[1], sto_list[2])

        # construction of second tree
        t2 = nx.DiGraph()
        t2.add_edge(sto_list[0], sto_list[3])

        # construction of third tree
        t3 = nx.DiGraph()
        t3.add_edge(sto_list[4], sto_list[5])
        t3.add_edge(sto_list[5], sto_list[7])

        # construction of fourth tree
        t4 = nx.DiGraph()
        t4.add_edge(sto_list[8], sto_list[9])

        sto_forest = [t1, t2, t3, t4]

        print(sto_forest)
        edge_incident = {1: ['a', 'b'],
                         2: ['a', 'c'],
                         3: ['c', 'b'],
                         4: ['b', 'g'],
                         5: ['b', 'i'],
                         6: ['i', 'g']}

        # After finding causality, temporal data is ignored
        et1 = nx.DiGraph()
        et1.add_edge(1, 4)
        et2 = nx.DiGraph()
        et2.add_edge(3, 4)
        expected_frequent_trees = [et1, et2]

        # if node is in the half of trees then it is frequent
        frequency_threshold = .5
        detector = FrequentSubTreeDetector(sto_forest, edge_incident, frequency_threshold)
        frequent_trees = detector.find_frequent_subtrees()

        assert len(frequent_trees) == len(expected_frequent_trees)

        for et in expected_frequent_trees:
            is_expected = False

            for ft in frequent_trees:
                is_expected |= et.adj == ft.adj

            assert is_expected is True

        sto_list = [FeatureOutlier(3, 0, 0), FeatureOutlier(5, 0, 1), FeatureOutlier(4, 2, 1),
                    FeatureOutlier(2, 0, 0), FeatureOutlier(3, 0, 1), FeatureOutlier(5, 1, 2),
                    FeatureOutlier(4, 0, 2)]

        t5 = nx.DiGraph()
        t5.add_edge(sto_list[0], sto_list[1])
        t5.add_edge(sto_list[0], sto_list[2])

        t6 = nx.DiGraph()
        t6.add_edge(sto_list[3], sto_list[4])
        t6.add_edge(sto_list[4], sto_list[5])
        t6.add_edge(sto_list[4], sto_list[6])

        et = nx.DiGraph()
        et.add_edge(3, 4)
        et.add_edge(3, 5)
        expected_forest = [et]

        sto_forest = [t5, t6]

        frequency_threshold = .55
        detector = FrequentSubTreeDetector(sto_forest, edge_incident, frequency_threshold)
        frequent_forest = detector.find_frequent_subtrees()

        assert len(expected_forest) == len(frequent_forest)
        for et in expected_forest:
            for ft in frequent_forest:
                assert et.adj == ft.adj
