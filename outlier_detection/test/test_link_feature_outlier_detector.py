# In the name of Allah
import numpy as np

from outlier_detection.link_feature_outlier_detector import LinkFeatureOutlierDetector
from random_data_generator import generate_random_stream


class TestLinkFeatureOutlierDetector:
    def test_find_outlier(self):
        stream = generate_random_stream(data_point_dims=3, time_frame_bins=10, link_count=4, observation_count=4)
        detector = LinkFeatureOutlierDetector(stream)
        outliers = detector.find_outliers(0)
        assert len(outliers) != 0
