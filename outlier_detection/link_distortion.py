# In the name of Allah
from typing import List, Dict
import numpy as np

from outlier_detection.exception import IllegalLinkIndexException, MalformedTimeFrameException


class LinkDistortion:
    def __init__(self, stream_time_frames: Dict):
        self.time_frames = stream_time_frames

    def min_distort(self, link_index):
        if link_index not in self.time_frames.keys():
            raise IllegalLinkIndexException()

        link_time_frames = self.time_frames[link_index]
        self._check_link_time_frame_len(link_time_frames)

        min_distortion = float("+inf")
        for i, tf_1 in enumerate(link_time_frames):
            for j, tf_2 in enumerate(link_time_frames):
                if i != j:
                    current_distortion = self._compute_time_frame_distance(tf_1, tf_2)
                    min_distortion = min(current_distortion, min_distortion)

        return min_distortion

    @staticmethod
    def _check_link_time_frame_len(link_time_frames):
        if len(link_time_frames) == 1:
            raise MalformedTimeFrameException("More time frames is needed to compute distortion.")

        if any(len(link_time_frames[i]) != len(link_time_frames[i - 1]) for i in range(1, len(link_time_frames))):
            raise MalformedTimeFrameException("Time frames have not same bins.")

    @staticmethod
    def _compute_time_frame_distance(tf_1, tf_2):
        diff = np.sqrt(np.sum(np.array([np.power(tf_1[time_bin] - tf_2[time_bin], 2) for time_bin in range(len(tf_1))])))
        return diff
