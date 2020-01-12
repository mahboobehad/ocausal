# In the name of Allah
from typing import Dict, List

import numpy as np
from attr import dataclass
from numpy.linalg import LinAlgError


@dataclass(eq=True, frozen=True)
class FeatureOutlier:
    link_index: int
    time_bin_index: int
    observation_index: int


class LinkFeatureOutlierDetector:
    def __init__(self, link_observations_stream: Dict, outlier_threshold):
        self.link_observations_stream = link_observations_stream
        self.outlier_threshold = outlier_threshold

    def find_outliers(self, observation_index) -> List[FeatureOutlier]:
        outliers = list()
        for link in self.link_observations_stream:
            for time_bin_index, link_feature in enumerate(self.link_observations_stream[link][observation_index]):
                distance = self._compute_mahalanobis_distance(link_feature,
                                                              self.link_observations_stream[link][observation_index])
                if distance >= self.outlier_threshold:
                    outliers.append(FeatureOutlier(link, time_bin_index, observation_index))

        return outliers

    @staticmethod
    def _compute_mahalanobis_distance(link_feature, all_link_features) -> float:
        mu = np.array(all_link_features).mean(axis=0)
        cov = np.cov(all_link_features, rowvar=0)
        try:
            cov_inv = np.linalg.inv(cov)
        except LinAlgError:
            cov_inv = np.ones(cov.shape)

        mahalanobis_distance = np.sqrt((link_feature - mu).T @ cov_inv @ (link_feature - mu))
        return mahalanobis_distance
