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
        'path_TrData': 'C:/Users/nicol/Desktop/Uniandes/2020-1 Investigacion/Training Data/TrainingData',
        # Path for already saved extreme points decodification.
        'extremes' : ['list_extremes',1]
        }
# Changes current working directory
os.chdir(paths['working_directory'])

################################################################
###################### INPORT ESPECIAL MODULES #################
################################################################

    # PreProcessing
from PreProcessing import import_data_raw
from PreProcessing import extremes_sample
from PreProcessing import apply_to
from PreProcessing import get_search

    # Saving
from SaveLoadFunctions import save_extremes
from SaveLoadFunctions import load_extremes

    # Distance Functions
from DistanceFunctions import distances_matrix
from DistanceFunctions import D_PP
from DistanceFunctions import D_PPrk
from DistanceFunctions import D_PPpr

    # Plotting functions
from PlotFunctions import plot_projections
from PlotFunctions import plot_class_distances

################################################################
###################### PARAMETERS ##############################
################################################################

prm = {}
    # Minimum distance between peaks
prm['delta'] = 1     
    # First exponential parameter 
prm['q1'] = -5          
    # Second exponential parameter
prm['q2'] = -0.5
    # Minimum number of peaks allowed
prm['p_min'] = 3           
    # Maximum number of peaks allowed (0 if no maximum used)
prm['p_max'] = 0

# Distance function to be used
    # D_PP : basic distance
    # D_PPrk : ranked distance 
    # D_PPpr : proportional distance
dist_function = D_PP

# Ranked and Proportional distance use positive q2. Also
# Case ranked distance
prm['beta'] = 0.9
# Case proportional distance
prm['gamma'] = 2

do_plot = True

################################################################
###################### IMPORT DATA #############################
################################################################
# Imports data in order to create distances matrix.

# If file with extremes already exists uses it
if os.path.isfile(paths['extremes'][0] + str(paths['extremes'][1]) + '.csv'):
    list_extremes, classess = load_extremes(paths['extremes'][0] + str(paths['extremes'][1]))
# Else loads data from raw files
else:
    # Loads data from raw csv files
    data , classess = import_data_raw(trPath = paths['path_TrData'] + str(paths['extremes'][1]), format_type = paths['extremes'][1])
    
    # Get Information on extreme values
    list_extremes = apply_to(extremes_sample, data, other = None)
    
    # Saves extremes information for future use
    save_extremes(list_extremes, classess, paths['extremes'][0] + str(paths['extremes'][1]))
    

# Extracts Peak information
list_peaks = apply_to(get_search,list_extremes, prog = False) 

list_valleys = apply_to(get_search,list_extremes, prog = False, other ='min') 

# Normalizes so that maximum peak has intensity 1.

################################################################
###################### DISTANCES MATRIX ########################
################################################################

# Naming of file
optional = ''
if dist_function == D_PPrk:
    optional += ' beta ' + str(prm['beta'])
if dist_function == D_PPpr:
    optional += ' gamma ' + str(prm['gamma'])
if prm['p_max'] != 0:
    optional += ' - ' + 'p_max ' + str(prm['p_max'])

distM_name = 'DM' + str(paths['extremes'][1]) + ' - ' + dist_function.__name__ + optional + ' - p_min ' + str(prm['p_min']) + ' - delta ' + str(prm['delta']) + ' - q1 ' + str(prm['q1'] ) + ' - q2 ' + str(prm['q2']) + '.csv' 
                                
# If distances matrix exists then loads, otherwise creates it
if os.path.isfile(distM_name):
    distances = pd.read_csv(distM_name)
    classess = list(distances.columns)
else:
    # Filter samples with less than minimum number of peaks are omited
    tmp = range(len(classess))
    classess = [classess[i] for i in tmp if list_peaks[i].shape[0] >= prm['p_min']]
    list_peaks = [list_peaks[i]  for i in tmp if list_peaks[i].shape[0] >= prm['p_min']]
    
    # Filter irrelevant peaks (when p_max != 0)
    if prm['p_max'] != 0:
        for i in range(len(list_peaks)):
            if list_peaks[i].shape[0] > prm['p_max']:
                list_peaks[i] = list_peaks[i].sort_values(by = ['value'], ascending = False)
                list_peaks[i] = list_peaks[i].head(prm['p_max'])

    # Distances matrix
    distances = distances_matrix(classess, list_peaks, prm, dist_function)
    # Saves distances matrix
    distances.columns = classess
    
    # Normalizes distances
    max_distance = max(distances.max())
    distances = distances.apply(lambda x : x/max_distance)
    
    
    distances.to_csv(distM_name)    


################################################################
###################### DISTANCES MATRIX ########################
################################################################

if do_plot:
    plot_projections(distances, classess, distM_name.split('.csv')[0])
    plot_class_distances(distances, classess, distM_name.split('.csv')[0])













