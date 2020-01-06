# In the name of Allah

import numpy as np

from outlier_detection.link_distortion_outlier_detector import LinkDistortionOutlierDetector


class TestLinkDistortion:
    time_frame = {0: [[np.array([4, 5]), np.array([0, 0])],
                      [np.array([1, 1]), np.array([0, 0])]]}

    def test_min_distort(self):
        distortion = LinkDistortionOutlierDetector(self.time_frame)
        link_index = 0
        time_frame_index = 0
        min_distort = distortion.min_distort(link_index, time_frame_index)
        expected_min_distort = 5.
        assert min_distort == expected_min_distort

    def test_find_outliers(self):
        distortion = LinkDistortionOutlierDetector(self.time_frame)
        outliers = distortion.find_outliers(0)
        assert len(outliers) != 0
