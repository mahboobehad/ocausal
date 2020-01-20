# In the name of Allah

import networkx as nx

from outlier_detection.link_feature_outlier_detector import FeatureOutlier


def sto_forest_test_case_generator():
    test_case = list()

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
    expected_forest = [et1, et2]

    # if node is in the half of trees then it is frequent
    frequency_threshold = .5

    test_case.append(([sto_forest, frequency_threshold, edge_incident], expected_forest))

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

    test_case.append(([sto_forest, frequency_threshold, edge_incident], expected_forest))

    # TODO add test case for cyclic frequent structure -> exception

    return test_case
