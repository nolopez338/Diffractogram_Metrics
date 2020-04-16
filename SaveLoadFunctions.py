"""
Autor: Nicolas Orlando Lopez Cuellar
Objective: Functions for saving and loading data.
"""

import pandas as pd
import os

###################################################################
#################### DATA IMPORT ##################################
###################################################################

def import_data_raw(trPath, format_type = 1):
    # format_type
        # 1 : TrainingData1
        # 2 : TrainingData2
    # List which contains the diffractogram data of each file
    files_trData = []
    # List which contains the titles of each file
    files_classess = [] 
    files_titles = []

    # Gets all .csv files
    for file in os.listdir(trPath):
        if ".csv" in file:
            files_trData.append(trPath + '\\' + file)
            files_classess.append(file.split('_')[0])
            files_titles.append(file.split('.csv')[0])
        
    # Loads files as data frames.
    data = list()
    
    for f in files_trData:
        # First Format types (TrainingData1)
        if format_type == 1:
            sample = pd.read_csv(f)
            sample.columns = ['Angle','Intensity']
        # Second Format types (TrainingData2)
        elif format_type == 2:
            sample = pd.read_csv(f, names = ['Angle','Intensity'], error_bad_lines = False) 
            
            # Selects index for new data Frame
            start_index = list(sample.loc[sample['Angle'] == 'Angle'].index)[0] + 1
            
            sample = sample.iloc[start_index:,:]
            sample = sample.astype('float')
        data.append(sample)
    
    # Creates identifier for each sample
    files_id = list(range(len(files_titles)))
    files_id = [str(format_type) + '-' + str(f_id) for f_id in files_id]
    
    return data , files_classess, files_titles, files_id
    
################################################################
#################### EXTREMES ##################################
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
    list_classess = []
    
        # First column of data.
    angle_col = [i for i in range(len(df.columns)) if  df.columns[i] == 'Angle'][0]
    df = df.iloc[:,angle_col:]
    
    for sample in df['sample'].unique():
        # Submatrix of only sample extremes
        df_tmp = df[df['sample'] == sample]
        df_tmp = df_tmp.drop(columns = ['sample'])
        
        # Saves class
        list_classess.append(df_tmp['class'].iloc[0])
        df_tmp = df_tmp.drop(columns = ['class'])
        
        list_extremes.append(df_tmp)
        
    return list_extremes, list_classess, df


################################################################
#################### DISTANCE MATRIX ###########################
################################################################

def load_distances_matrices(path = None):
    
    # Gets working directorys
    if path is None:
        path_matrices = os.getcwd()
    else:
        path_matrices = path
    
    files = []
    files_titles = []

    # Gets all .csv distances matrix files
    for file in os.listdir(path_matrices):
        if (("Distances Matrix" in file) or ('DM' in file)) and ('.csv' in file):
            files.append(path_matrices + '\\' + file)
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    