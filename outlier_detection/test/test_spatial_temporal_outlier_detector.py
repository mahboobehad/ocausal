# In the name of God
from outlier_detection.spatial_temporal_outlier_detector import SpatialTemporalOutlierDetector
from outlier_detection.test.stream_generator import generate_random_stream


class TestSpatialTemporalOutlierDetector:
    def test_find_outliers(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=10, link_count=4, observation_count=4)
        detector = SpatialTemporalOutlierDetector(stream)
        outliers = detector.find_outliers(observation_index=0)
        assert len(outliers) != 0
