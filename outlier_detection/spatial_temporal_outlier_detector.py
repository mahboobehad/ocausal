# In the name of Allah
from typing import List, Dict

from outlier_detection.link_distortion_outlier_detector import LinkDistortionOutlierDetector
from outlier_detection.link_feature_outlier_detector import LinkFeatureOutlierDetector, FeatureOutlier


class SpatialTemporalOutlierDetector:
    def __init__(self, stream_time_frame: Dict, link_outlier_threshold: float, feature_outlier_threshold: float):
        self.stream_time_frame = stream_time_frame
        self.distortion_outlier_detector = LinkDistortionOutlierDetector(stream_time_frame, link_outlier_threshold)
        self.feature_outlier_detector = LinkFeatureOutlierDetector(stream_time_frame, feature_outlier_threshold)

    def find_all_outliers(self) -> List[List[FeatureOutlier]]:
        observations_count = self._find_observation_count()
        st_outliers = [self.find_observation_outliers(observation_index) for observation_index in
                       range(observations_count)]
        return st_outliers

    def find_observation_outliers(self, observation_index) -> List[FeatureOutlier]:
        temporal_outliers = self.distortion_outlier_detector.find_outliers(observation_index)
        spatial_outliers = self.feature_outlier_detector.find_outliers(observation_index)
        spatial_temporal_outliers = list(filter(lambda x: x.link_index in temporal_outliers, spatial_outliers))
        return spatial_temporal_outliers

    def _find_observation_count(self) -> int:
        for key in self.stream_time_frame.keys():
            return len(self.stream_time_frame[key])
