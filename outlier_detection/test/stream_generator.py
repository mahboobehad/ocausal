# In the name of Allah
import numpy as np


def generate_random_stream(data_point_dims, time_frame_bins, link_count, observation_count):
    stream = {link: [np.array([np.random.randn(data_point_dims) + 1000
                               for _ in range(time_frame_bins)])
                     for _ in range(observation_count)]
              for link in range(link_count)}
    return stream
