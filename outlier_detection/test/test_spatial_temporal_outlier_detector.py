# In the name of Allah
from outlier_detection.spatial_temporal_outlier_detector import SpatialTemporalOutlierDetector
from random_data_generator import generate_random_stream, generate_random_graph


class TestSpatialTemporalOutlierDetector:
    def test_find_outliers(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=10, link_count=4, observation_count=4)
        edge_incident = generate_random_graph(list(stream.keys()), 5)
        detector = SpatialTemporalOutlierDetector(stream, edge_incident)
        outliers = detector.find_outliers(observation_index=0)
        assert len(outliers) != 0

    def test_construct_spatial_temporal_outlier_forest(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=10, link_count=4, observation_count=4)
        edge_incident = generate_random_graph(list(stream.keys()), 5)
        detector = SpatialTemporalOutlierDetector(stream, edge_incident)
        outlier_forest = detector.construct_spatial_temporal_outlier_forest()
        assert len(outlier_forest) != 0
