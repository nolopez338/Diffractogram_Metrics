"""
Program: peak_extraction.py
Project: Exctracts position of peak features within a diffractogram sample.
Author: Nicolas Lopez
"""

import numpy as np
import pandas as pd
import os

class PeakFinder:

    def __init__(self, data_list=[]):
        self.data_list = data_list
        self.data_peaks = []
        self.b0 =


    def update_extreme_point(self, search, extreme_val, extreme_pos, current_val, current_pos):
        if search == 'min' and current_val < extreme_val:
            extreme_val = current_val
            extreme_pos = current_pos
        if search == 'max' and current_val > extreme_val:
            extreme_val = current_val
            extreme_pos = current_pos

        return extreme_val, extreme_pos

    def update_search(self, search, extreme_val, extreme_pos, extreme_angle, current_val, b0, b1):
        new_extreme = None

        if search == 'min' and extreme_val < (current_val * b0 - b1):
            new_extreme = self.__extreme(search, extreme_pos, extreme_angle, extreme_val)
            search = 'max'

        elif search == 'max' and current_val < (extreme_val * b0 - b1):
            new_extreme = self.__extreme(search, extreme_pos, extreme_angle, extreme_val)
            search = 'min'

        return new_extreme, search


    def find_peaks_in_sample(self, sample, b0, b1):
        data = sample['data']

        extreme_val = data.iloc[0, 1]
        extreme_pos = 0
        search = 'min'

        # Searches for extreme points
        sample_extremes = []

        for i in range(1, len(data)):
            current_val = data['Intensity'][i]

            extreme_val, extreme_pos = self.update_extreme_point(search, extreme_val, extreme_pos, current_val, i)

            new_extreme, search = self.update_search(search, extreme_val, extreme_pos,
                                                     data['Angle'][extreme_pos])
            # Saves last recorded value
            if i == (len(sample) - 1):
                sample_extremes.append({'search': search,
                                        'pos': n_extreme,
                                        'Angle': sample.iloc[n_extreme, 0],
                                        'Intensity': extreme})

        sample_extremes = pd.DataFrame(sample_extremes)

    def __extreme(self, search, pos, angle, intensity):
        out = {'search': search,
                'pos': pos,
                'Angle': angle,
                'Intensity': intensity}
        return out



