# In the name of Allah

import numpy as np

from outlier_detection.link_distortion import LinkDistortion


class TestLinkDistortion:
    def test_min_distort(self):
        time_frame = {1: [np.array([40, 50]), np.array([10, 10])]}
        distortion = LinkDistortion(time_frame)
        min_distort = distortion.min_distort(1)
        expected_min_distort = 50.
        assert min_distort == expected_min_distort
