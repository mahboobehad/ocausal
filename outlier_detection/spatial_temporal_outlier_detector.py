# In the name of Allah
from typing import List

from outlier_detection.link_distortion_outlier_detector import LinkDistortionOutlierDetector
from outlier_detection.link_feature_outlier_detector import LinkFeatureOutlierDetector


class SpatialTemporalOutlierDetector:
    def __init__(self, stream_time_frame):
        self.distortion_outlier_detector = LinkDistortionOutlierDetector(stream_time_frame)
        self.feature_outlier_detector = LinkFeatureOutlierDetector(stream_time_frame)

    def find_outliers(self, observation_index) -> List:
        temporal_outliers = self.distortion_outlier_detector.find_outliers(observation_index)
        spatial_outliers = self.feature_outlier_detector.find_outliers(observation_index)
        spatial_temporal_outliers = list(filter(lambda x: x.link_index in temporal_outliers, spatial_outliers))
        return spatial_temporal_outliers
