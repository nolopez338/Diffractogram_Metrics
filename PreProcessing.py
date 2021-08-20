"""
Autor: Nicolas Orlando Lopez Cuellar
Objective: Functions for pre processing data
"""
import numpy as np
import pandas as pd
import os


###############################################################################
#################### SAMPLE MANIPULATION ######################################
###############################################################################

# Applies funtion constructed to work on sample on list of samples.
def apply_to(sample_fun, data, prog = True, other = None):
    # Progress
    if prog:
        print(sample_fun.__name__ + ' to data (' + str(len(data)) + ')')
        
    data_out = list()
    for i in range(len(data)):
        if other is None:
            sample = sample_fun(data[i].copy())
        else:
            sample = sample_fun(data[i].copy(), other)
            
        data_out.append(sample)
        
        # Progress
        if prog:
            progress = str(i + 1) + "/" + str(len(data))
            print(progress, end = ' - ')
            
    return(data_out)

# Finds index of an angle in a given sample
        # Bisection method
def find_angle(sample, angle, epsilon = 0.2):
    # Initialize
    a_n = sample.shape[0] - 1
    
    
    found = False
    step = int(a_n/2)
    idx = int(a_n/2)
    while not found:
        idx_angle = sample['Angle'][idx]

        step = step/2
    
        if np.abs(idx_angle- angle) < epsilon:
            found = True
        elif idx_angle - angle < 0:
            idx = int(idx + step)
        elif idx_angle - angle > 0:
            idx = int(idx - step)
        # elif step < 0.05:
        #    found = True
    
        idx_angle = sample['Angle'][idx]
        
    return idx
        
###############################################################################
#################### EXTREMES MANIPULATION ####################################
###############################################################################
# Creates diferential sample out of the sample
    # sample : two columns of angles and intensities
def differencial_sample(sample):
    out = sample.copy()
    for i in range(1,len(sample)):
        out.iloc[i,1] = sample.iloc[i,1] - sample.iloc[i-1,1]
    return(out)
    
# Get extreme values (max and min) out of sample
    # sample : two columns of angles and intensities
    # prop_self: Proportion from highest value
    # prop_dif: fixes proportion
def extremes_sample(sample, prop_self = 1/2, prop_dif = 1/80, min_delta = 0.4):
    
    prop_max = np.max(np.absolute(sample.iloc[:,1]))*prop_dif
    
    # Initialize
 #   extreme = sample.iloc[0,1].copy()
    extreme = sample.iloc[0,1]
    n_extreme = 0
    search = 'min'
    
    # Searches for extreme points
    sample_extremes = list()
    for i in range(1,len(sample)):
        actual = sample.iloc[i,1]
        
        # Replaces when finds more extreme value
        if search == 'min' and actual < extreme:
            extreme = actual
            n_extreme = i
        if search == 'max' and actual > extreme :
            extreme = actual
            n_extreme = i
        
        # Changes search and saves data when threshold passed
        if search == 'min' and extreme < (actual*prop_self - prop_max):
            sample_extremes.append({'search' : search,
                                  'pos' : n_extreme, 
                                  'Angle' : sample.iloc[n_extreme,0],
                                  'Intensity': extreme})
            search = 'max'
            
        if search == 'max' and actual < (extreme*prop_self - prop_max):
            sample_extremes.append({'search' : search,
                                  'pos' : n_extreme, 
                                  'Angle' : sample.iloc[n_extreme,0],
                                  'Intensity': extreme})
            search = 'min'
            
        # Saves last recorded value
        if i == (len(sample)-1):
            sample_extremes.append({'search' : search,
                                  'pos' : n_extreme, 
                                  'Angle' : sample.iloc[n_extreme,0],
                                  'Intensity': extreme})
            
    sample_extremes = pd.DataFrame(sample_extremes)
    
    # Eliminates minimum between two maximums too close to each other:
    drop_i = []
    for i in range(sample_extremes.shape[0]-2):
        # Checks only for maximum values separated by another extreme
        if (sample_extremes['search'][i] == 'max') and (sample_extremes['search'][i+2] == 'max'):
            # Checks if angle difference is less than minimum allowed
            if sample_extremes['Angle'][i+2] - sample_extremes['Angle'][i] < min_delta:
                # Checks which peak has higher intensity and keeps it
                drop_i.append(i+1)
                if sample_extremes['Intensity'][i] > sample_extremes['Intensity'][i+2]:
                    # Does not eliminate consecutive samples
                    if not (i in drop_i):
                        drop_i.append(i+2)
                else:
                    
                    drop_i.append(i)
    sample_extremes = sample_extremes.drop(drop_i)
    # Re index
    sample_extremes.reindex(index = range(sample_extremes.shape[0]))
    
    return sample_extremes


# Merges extremes list, classess and id in a single Dataframe
def merge_extreme_information(list_extremes, classess, list_id):
    df = pd.DataFrame()
    
    for i in range(len(list_extremes)):
        sample_extremes = list_extremes[i]
        # sample_extremes = pd.DataFrame(sample_extremes)
        
        sample_extremes['sample'] = i + 1
        sample_extremes['class'] = classess[i]
        sample_extremes['id'] = list_id[i] + 1

        
        df = pd.concat([df,sample_extremes], ignore_index = True, sort = True)
        
    return df
    
# From a result from the extremes_sample function we extract the search option
    # either max or min
def get_search(sample_extremes, search = 'max'):
    
    out = sample_extremes[sample_extremes['search'] == search]
    return(out)

# Merges list extremes in current w
def merge_extremes_dataframes(path = None, name = 'list_extremes'):
    
    if path is None:
        path = os.getcwd()
        
    # Gets all .csv files
    files = []

    # Selects list extremes (only the numbered ones)
    for file in os.listdir(path):
        if (".csv" in file) and (name in file):
            f = file.split(name)[1]
            f = f.split('.csv')[0]
            if f.isdigit():
                files.append(file)
    
    df = pd.DataFrame()
    # Merges dataframes
    for file in files:
            sample_extremes = pd.read_csv(file)
            df = pd.concat([df,sample_extremes], ignore_index = True, sort = True) 
            
    df.to_csv(name + '.csv')
    

###############################################################################
#################### DISTANCES MATRICES MANIPULATION ##########################
###############################################################################
    
# Plot projections for a specific distance matrix
def eliminate_unwanted(distance_matrix, classess, unwanted = ['Patata']):
    
    # Eliminates unwanetd information
    for eliminate in unwanted:
        # Eliminate from rows
        distance_matrix = distance_matrix.loc[[distance_matrix.index[i] for i in range(len(distance_matrix.index)) if not eliminate in classess[i] ]]
        
        # Eliminates from columns
        col_eliminate = [col for col in distance_matrix.columns if eliminate in col]
        for col in col_eliminate:
            distance_matrix = distance_matrix.drop(col, axis = 1)
        
        # Eliminates from classess
        classess = [cl for cl in classess if not eliminate in cl]
    
    return distance_matrix, classess


###############################################################################
#################### FILES MANIPULATION #######################################
###############################################################################
    
def create_folder(folder_name):
    path0 = folder_name
    path = path0
    idx = 0
    while os.path.isdir(path):
        idx += 1
        path = path0 + str(idx)
    os.mkdir(path)






















