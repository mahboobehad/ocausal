# In the name of Allah
import pytest

from causlity_relation.exception import MalformedSpatialTemporalOutlierList
from outlier_detection.link_feature_outlier_detector import FeatureOutlier
from causlity_relation.outlier_tree_constructor import OutlierTreeConstructor


def test_construct_spatial_temporal_outlier_forest():
    outliers = [[FeatureOutlier(0, 0, 0)], [FeatureOutlier(1, 0, 1)], [FeatureOutlier(2, 0, 2)]]
    edge_incident = {0: [1, 2],
                     1: [2, 3],
                     2: [3, 4]}
    constructor = OutlierTreeConstructor(outliers, edge_incident)
    outlier_forest = constructor.construct_spatial_temporal_outlier_forest()
    assert len(outlier_forest) != 0
    assert len(outlier_forest[0].nodes) == 3

    outliers = [[FeatureOutlier(0, 0, 0)], [FeatureOutlier(2, 1, 1)]]
    constructor = OutlierTreeConstructor(outliers, edge_incident)
    outlier_forest = constructor.construct_spatial_temporal_outlier_forest()
    assert len(outlier_forest) == 0

    outliers = [[FeatureOutlier(0, 0, 0)]]
    constructor = OutlierTreeConstructor(outliers, edge_incident)
    with pytest.raises(MalformedSpatialTemporalOutlierList):
        outlier_forest = constructor.construct_spatial_temporal_outlier_forest()
