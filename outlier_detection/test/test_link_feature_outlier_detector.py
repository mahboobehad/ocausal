# In the name of Allah
import numpy as np

from outlier_detection.link_feature_outlier_detector import LinkFeatureOutlierDetector


class TestLinkFeatureOutlierDetector:
    def test_find_outlier(self):
        data_point_dim = 3
        time_frame_bins = 10
        time_frame_link_count = 3
        observation_count = 2
        stream = {link: [np.array([np.random.randn(data_point_dim) + 1000 for _ in range(time_frame_bins)]) for _ in
                  range(observation_count)]
                  for link in range(time_frame_link_count)}

        detector = LinkFeatureOutlierDetector(stream)
        outliers = detector.find_outliers(0)
        assert len(outliers) != 0
