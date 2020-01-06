# In the name of Allah
from typing import Dict, List

import numpy as np
from attr import dataclass
from numpy.linalg import LinAlgError


@dataclass
class FeatureOutlier:
    link_index: int
    time_bin_index: int


class LinkFeatureOutlierDetector:
    def __init__(self, stream_time_frames: Dict, outlier_threshold=1):
        self.stream_time_frames = stream_time_frames
        self.outlier_threshold = outlier_threshold

    def find_outliers(self, time_frame_index) -> List[FeatureOutlier]:
        outliers = list()
        for link in self.stream_time_frames:
            for time_bin_index, link_feature in enumerate(self.stream_time_frames[link][time_frame_index]):
                distance = self._compute_mahalanobis_distance(link_feature,
                                                              self.stream_time_frames[link][time_frame_index])
                if distance >= self.outlier_threshold:
                    outliers.append(FeatureOutlier(link, time_bin_index))

        return outliers

    @staticmethod
    def _compute_mahalanobis_distance(link_feature, all_link_features):
        mu = np.array(all_link_features).mean(axis=0)
        cov = np.cov(all_link_features, rowvar=0)
        try:
            cov_inv = np.linalg.inv(cov)
        except LinAlgError:
            cov_inv = np.ones(cov.shape)

        mahalanobis_distance = np.sqrt((link_feature - mu).T @ cov_inv @ (link_feature - mu))
        return mahalanobis_distance

