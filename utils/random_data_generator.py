# In the name of Allah
import time

import numpy as np
from numba import njit


def generate_random_stream(data_point_dims, time_frame_bins, link_count, observation_count):
    stream = {link: [generate_random_time_frame(data_point_dims, time_frame_bins) for _ in range(observation_count)]
              for link in range(link_count)}
    return stream


@njit('(int32, int32)')
def generate_random_time_frame(data_point_dims, time_frame_bins):
    time_frame = np.empty((time_frame_bins, data_point_dims))
    for i in range(time_frame_bins):
        time_frame[i] = np.random.randn(data_point_dims)
        np.mean(time_frame[i])

    return time_frame


def generate_random_graph(links_labels, number_of_nodes):
    edge_incident = dict()
    for label in links_labels:
        u, v = np.random.randint(1, number_of_nodes + 1, 2)
        while u == v:
            u, v = np.random.randint(1, number_of_nodes + 1, 2)
        edge_incident[label] = [u, v]

    return edge_incident

