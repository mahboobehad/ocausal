# In the name of Allah

from utils.random_data_generator import generate_random_stream

from outlier_detection.link_distortion_outlier_detector import LinkDistortionOutlierDetector


class TestLinkDistortion:
    stream = generate_random_stream(data_point_dims=3, time_frame_bins=5, link_count=4, observation_count=4)
    outlier_threshold = 0

    def test_find_outliers(self):
        distortion = LinkDistortionOutlierDetector(self.stream, self.outlier_threshold)
        outliers = distortion.find_outliers(0)
        assert len(outliers) != 0
