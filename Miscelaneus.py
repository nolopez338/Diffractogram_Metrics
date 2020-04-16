"""
Autor: Nicolas Orlando Lopez Cuellar
Objective: Create distances matrix for a set of given parameters
"""

################################################################
###################### IMPORT MODULES ##########################
################################################################

import os
import pandas as pd

################################################################
###################### INPUT VARIABLES #########################
################################################################

#### Adress for inputs (MODIFY FOR EACH COMPUTER)
paths = {
        # Where the functions will be loaded from
        'working_directory' : "C:/Users/nicol/Desktop/Uniandes/2020-1 Investigacion/Codes",
        # Path for folder with the training data
        'path_TrData': 'C:/Users/nicol/Desktop/Uniandes/2020-1 Investigacion/Training Data/TrainingData2',
        # Path for already saved extreme points decodification.
        'extremes' : ['list_extremes',1]
        }
# Changes current working directory
os.chdir(paths['working_directory'])


################################################################
###################### ISpecific Modules #######################
################################################################

from SaveLoadFunctions import load_distances_matrices

from PlotFunctions import plot_sample

data, titles, data_classess = load_distances_matrices()





################################################################
###################### ISpecific Modules #######################
################################################################


k = 19

sample = data[k]
valleys = list_valleys[k]
peaks = list_peaks[k]
extremes = list_extremes[k]

sample_extremes = extremes

plot_sample(sample, 'test' ,os.getcwd() , peaks = peaks, valleys = valleys, colors = ['blue','red','green'], angle_zoom = None, angle_window = 5)


angle_zoom = 80
angle_window = 10
plot_sample(sample, 'test' ,os.getcwd() , peaks = peaks, valleys = valleys, colors = ['blue','red','green'], angle_zoom = angle_zoom, angle_window = angle_window)

find_angle(36,sample)
find_angle(36.1,sample)


