# In the name of Allah
from typing import Dict, List, Tuple

import numpy as np

from outlier_detection.exception import IllegalIndexException, MalformedTimeFrameException


class LinkDistortionOutlierDetector:
    def __init__(self, link_observation_stream: Dict, outlier_threshold):
        self.stream = link_observation_stream
        self.outlier_threshold = outlier_threshold

    def find_outliers(self, observation_index) -> List:
        outliers = list()
        global_min, global_max = self._find_distort_extrema(observation_index)

        for link in self.stream.keys():
            link_min_distort = self._find_normalized_min_distort(link, observation_index, global_min, global_max)

            if link_min_distort >= self.outlier_threshold:
                outliers.append(link)

        return outliers

    def _find_normalized_min_distort(self, link_index, observation_index, global_min, global_max) -> float:

        if link_index not in self.stream.keys():
            raise IllegalIndexException()

        link_time_frames = self.stream[link_index]
        self._check_link_time_frame_len(link_time_frames)

        min_distortion = float("+inf")
        for i, tf in enumerate(link_time_frames):
            if i != observation_index:
                current_distortion = self._compute_time_frame_distance(tf, link_time_frames[observation_index])
                min_distortion = min(current_distortion, min_distortion)

        normalized_link_min_distort = abs((min_distortion - global_min) / global_max if global_max != 0 else (
                min_distortion - global_min))
        return normalized_link_min_distort

    def _find_distort_extrema(self, observation_index) -> Tuple:
        global_max = float('-inf')
        global_min = float('+inf')
        for link in self.stream.keys():
            current_observation = self.stream[observation_index]
            for i, tf in enumerate(self.stream[link]):
                if i != observation_index:
                    current_distort = self._compute_time_frame_distance(current_observation, tf)
                    global_max = max(current_distort, global_max)
                    global_min = min(current_distort, global_min)

        return global_min, global_max

    @staticmethod
    def _compute_time_frame_distance(tf_1, tf_2) -> float:
        diff = np.sqrt(
            np.sum(np.array([np.power(tf_1[time_bin] - tf_2[time_bin], 2) for time_bin in range(len(tf_1))])))
        return diff

    @staticmethod
    def _check_link_time_frame_len(link_time_frames):
        if len(link_time_frames) == 1:
            raise MalformedTimeFrameException("More time frames are needed to compute distortion.")

        if any(len(link_time_frames[i]) != len(link_time_frames[i - 1]) for i in range(1, len(link_time_frames))):
            raise MalformedTimeFrameException("Time frames have not same bins.")

