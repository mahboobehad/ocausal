# In the name of Allah
from utils.random_data_generator import generate_random_stream
from outlier_detection.spatial_temporal_outlier_detector import SpatialTemporalOutlierDetector


class TestSpatialTemporalOutlierDetector:
    def test_find_outliers(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=5, link_count=4, observation_count=4)
        # assume all data points are outlier, check whether it is possible to find causality
        link_threshold = 0
        feature_threshold = 0
        detector = SpatialTemporalOutlierDetector(stream, link_threshold, feature_threshold)
        outliers = detector.find_observation_outliers(observation_index=0)
        assert len(outliers) != 0
