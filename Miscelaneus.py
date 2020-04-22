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
from DistanceFunctions import distances_centroids_matrix

data, titles, data_classess = load_distances_matrices()

distance_matrix = data[0]
classess = data_classess[0]

# Get centroid distance matrix
distances_centroids = distances_centroids_matrix(distance_matrix,classess)


################################################################
###################### ISpecific Modules #######################
################################################################
from PreProcessing import import_data_raw

data , classess = import_data_raw(trPath = paths['path_TrData'] + str(paths['extremes'][1]), format_type = paths['extremes'][1])


################################################################
###################### ISpecific Modules #######################
################################################################
from PlotFunctions import plot_sample
from PreProcessing import apply_to
from PreProcessing import extremes_sample
from PreProcessing import get_search

# Get Information on extreme values
list_extremes = apply_to(extremes_sample, data, other = None)

 

# Extracts Peak information
list_peaks = apply_to(get_search,list_extremes, prog = False) 

list_valleys = apply_to(get_search,list_extremes, prog = False, other ='min') 


k = 19

sample = data[k]
valleys = list_valleys[k]
peaks = list_peaks[k]
extremes = list_extremes[k]

sample_extremes = extremes

plot_sample(sample, 'test' ,os.getcwd() , peaks = peaks, valleys = valleys, colors = ['blue','red','green'], angle_zoom = None, angle_window = 5)


angle_zoom = 32
angle_window = 8
plot_sample(sample, 'test' ,os.getcwd() , peaks = peaks, valleys = valleys, colors = ['blue','red','green'], angle_zoom = angle_zoom, angle_window = angle_window)

find_angle(36,sample)
find_angle(36.1,sample)

###########################################################

P1 = list_peaks[0]
P2 = list_peaks[1]

out = D_PP(list_peaks[0],list_peaks[1], prm)

out0 = D_PP(list_peaks[0],list_peaks[0], prm)
out1 = D_PP(list_peaks[1],list_peaks[1], prm)

#########################################3
p = P1.iloc[0]
P = P1

d_pP(p,P,prm)



d_pP_info(p, P, prm)




import pylab
fig = pylab.figure()
figlegend = pylab.figure(figsize=(3,2))
ax = fig.add_subplot(111)
lines = ax.plot(range(10), pylab.randn(10), range(10), pylab.randn(10))
figlegend.legend(lines, ('one', 'two'), 'center')
fig.show()
figlegend.show()
figlegend.savefig('legend.png')









