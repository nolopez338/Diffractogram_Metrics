"""
Autor: Nicolas Orlando Lopez Cuellar
Objective: Functions for saving and loading data.
"""

import pandas as pd
import os


    
################################################################
#################### PRE PROCESSING ############################
################################################################

# Saves list_extremes in a csv file
def save_extremes(list_extremes, classess, name):
    df = pd.DataFrame()
    
    for i in range(len(list_extremes)):
        sample_extremes = list_extremes[i]
        # sample_extremes = pd.DataFrame(sample_extremes)
        
        sample_extremes['sample'] = i + 1
        sample_extremes['class'] = classess[i]
        
        df = pd.concat([df,sample_extremes], ignore_index = True, sort = True)
        
    df.to_csv( name + '.csv')

# Loads list_extremes froma a csv file
def load_extremes(name):
    df = pd.read_csv(name + '.csv')
    list_extremes = []
    list_ids = []
    
    angle_col = [i for i in range(len(df.columns)) if  df.columns[i] == 'Angle'][0]
    df = df.iloc[:,angle_col:]
    
    for sample in df['sample'].unique():
        df_tmp = df[df['sample'] == sample]
        df_tmp = df_tmp.drop(columns = ['sample'])
        
        list_ids.append(df_tmp['class'].iloc[0])
        df_tmp = df_tmp.drop(columns = ['class'])
        
        list_extremes.append(df_tmp)
        
    return list_extremes, list_ids

def load_distances_matrices(path = None):
    
    # Gets working directorys
    if path is None:
        path_matrices = os.getcwd()
    else:
        path_matrices = path
    
    files = []
    files_titles = []

    # Gets all .csv distances matrix files
    for r, d, f in os.walk(path_matrices):
        for file in f:
            if (("Distances Matrix" in file) or ('DM' in file)) and ('.csv' in file):
                files.append(os.path.join(r, file))
                files_titles.append(file)
    
    data = []
    data_classess = []
    for f in files:
        # Get distance Matrix
        distance_matrix = pd.read_csv(f, index_col = 0)
        # Get Classess
        classess = [col_name.split('.')[0] for col_name in distance_matrix.columns]
        
            
        # Normalizes distances
        max_distance = max(distance_matrix.max())
        distances = distance_matrix.apply(lambda x : x/max_distance)
        
        distances.to_csv(f.split('\\')[-1])    

        
        # Save information
        data.append(distance_matrix)
        data_classess.append(classess)
    
    # Gets Tag on file name to classify it
    titles = []
    for f in files_titles:
        titles.append(f)
    
    return data, titles, data_classess
    
    
    
    
    
    
    
    
    
    
    
    
    
    