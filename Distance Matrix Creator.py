"""
Autor: Nicolas Orlando Lopez Cuellar
Objective: Create distances matrix for a set of given parameters
"""

################################################################
###################### IMPORT MODULES ##########################
################################################################

# Basic modules
import os
import pandas as pd
import sys

################################################################
###################### INPUT VARIABLES #########################
################################################################


#### Adress for inputs (MODIFY FOR EACH COMPUTER)
paths = {
        # Where the functions will be loaded from
        'working_directory' : "C:/Users/nicol/Desktop/Uniandes/2020-1 Investigacion/Codes",
        # Path for folder with the training data
        'path_TrData': 'C:/Users/nicol/Desktop/Uniandes/2020-1 Investigacion/Training Data/TrainingData',
        # Exterme information to be used
            # 0 : All data sets
            # n != 0 : data set n
        'extremes' : ['list_extremes', '' ]
        }

manual_path = False
# Changes current working directory
if manual_path:
    os.chdir(paths['working_directory'])
else:
        # colab
    tmp = 1
        # Current computer
# =============================================================================
#     os.chdir(os.path.dirname(sys.argv[0]))
# =============================================================================


################################################################
###################### INPORT ESPECIAL MODULES #################
################################################################

    # PreProcessing
from PreProcessing import extremes_sample
from PreProcessing import merge_extreme_information
from PreProcessing import apply_to
from PreProcessing import get_search
from PreProcessing import create_folder

    # Saving
from SaveLoadFunctions import import_data_raw
from SaveLoadFunctions import load_extremes

    # Distance Functions
from DistanceFunctions import distances_matrix
from DistanceFunctions import distances_centroids_matrix
from DistanceFunctions import D_PP
from DistanceFunctions import D_PPrk
from DistanceFunctions import D_PPpr

    # Plotting functions
from PlotFunctions import plot_projections
from PlotFunctions import plot_class_distances

################################################################
###################### BASIC PARAMETERS ########################
################################################################

prm = {}
    # Minimum distance between peaks
prm['delta'] = 0.5
    # First exponential parameter 
prm['q1'] =   -5
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
3
# Ranked and Proportional distance use positive q2
# Case ranked distance
prm['beta'] = 0.8
# Case proportional distance
prm['gamma'] = 2

# Optional do plotting after creating the matrix
do_plot = True

################################################################
###################### IMPORT DATA #############################
################################################################
# Imports data in order to create distances matrix.

# If file with extremes already exists uses it
if os.path.isfile(paths['extremes'][0] + str(paths['extremes'][1]) + '.csv'):
    list_extremes, classess, extremes_df = load_extremes(paths['extremes'][0] + str(paths['extremes'][1]))
# Else loads data from raw files
else:
    # Loads data from raw csv files
    data , classess, file_names, files_id = import_data_raw(trPath = paths['path_TrData'] + str(paths['extremes'][1]), format_type = paths['extremes'][1])
    
    # Get Information on extreme values
    list_extremes = apply_to(extremes_sample, data, other = None)
    
    # Merges the above information in one table
    extremes_df = merge_extreme_information(list_extremes, classess, files_id)
    
    # Sves file for future use
    extremes_df.to_csv(paths['extremes'][0] + str(paths['extremes'][1]) + '.csv')

# Extracts Peak informations
list_peaks = apply_to(get_search,list_extremes, prog = False) 

list_valleys = apply_to(get_search,list_extremes, prog = False, other ='min') 

# Normalizes so that maximum peak has intensity 1.

################################################################
###################### DISTANCES MATRIX ########################
################################################################

# Naming of output file
    # Optional string for aditional parameters
optional = ''
if dist_function == D_PPrk:
    optional += ' beta ' + str(prm['beta'])
if dist_function == D_PPpr:
    optional += ' gamma ' + str(prm['gamma'])
if prm['p_max'] != 0:
    optional += ' - ' + 'p_max ' + str(prm['p_max'])

    # Name
tmp = str(paths['extremes'][1]) + ' - ' + dist_function.__name__ + optional + ' - p_min ' + str(prm['p_min']) + ' - delta ' + str(prm['delta']) + ' - q1 ' + str(prm['q1'] ) + ' - q2 ' + str(prm['q2']) + '.csv' 
distM_name = 'DM ' + tmp
distCM_name = 'DCM '   + tmp       
                      
# If distances matrix exists then loads, otherwise creates it
if os.path.isfile(distM_name):
    distances = pd.read_csv(distM_name)
    distances = distances.drop(columns = [col for col in distances.columns if 'Unnamed' in col] )
    
    classess = list(distances.columns)
    classess = [cl.split('.')[0] for cl in classess]
            
    
else:
    # Filter samples with less peaks than the minimum allowed
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
    distances = distances_matrix(list_peaks, classess, prm, dist_function)

    # Normalizes distances: Maximum Distance becomes 1
    max_distance = max(distances.max())
    distances = distances.apply(lambda x : x/max_distance)

distances_centroids = distances_centroids_matrix(distances, classess)

distances_centroids.to_csv(distCM_name)
distances.to_csv(distM_name)    


################################################################
###################### PLOT ####################################
################################################################

if do_plot:
    plot_projections(distances, classess, distM_name.split('.csv')[0])
    plot_class_distances(distances, classess, distM_name.split('.csv')[0])













