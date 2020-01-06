# In the name of Allah
from typing import Dict, List
import numpy as np


from outlier_detection.exception import IllegalIndexException, MalformedTimeFrameException


class LinkDistortionOutlierDetector:
    def __init__(self, stream_time_frames: Dict):
        self.time_frames = stream_time_frames

    def min_distort(self, link_index, time_frame_index):
        if link_index not in self.time_frames.keys():
            raise IllegalIndexException()

        if not 0 <= time_frame_index <= link_index:
            raise IllegalIndexException()

        link_time_frames = self.time_frames[link_index]
        self._check_link_time_frame_len(link_time_frames)

        min_distortion = float("+inf")
        for i, tf in enumerate(link_time_frames):
            if i != time_frame_index:
                current_distortion = self._compute_time_frame_distance(tf, link_time_frames[time_frame_index])
                min_distortion = min(current_distortion, min_distortion)

        return min_distortion

    @staticmethod
    def _check_link_time_frame_len(link_time_frames):
        if len(link_time_frames) == 1:
            raise MalformedTimeFrameException("More time frames are needed to compute distortion.")

        if any(len(link_time_frames[i]) != len(link_time_frames[i - 1]) for i in range(1, len(link_time_frames))):
            raise MalformedTimeFrameException("Time frames have not same bins.")

    @staticmethod
    def _compute_time_frame_distance(tf_1, tf_2):
        diff = np.sqrt(
            np.sum(np.array([np.power(tf_1[time_bin] - tf_2[time_bin], 2) for time_bin in range(len(tf_1))])))
        return diff

    def find_outliers(self) -> List:
        return list()
