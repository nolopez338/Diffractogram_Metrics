"""
Autor: Nicolas Orlando Lopez Cuellar
Objective: Loss functions and classification
"""

from SaveLoadFunctions import load_distances_matrices

from DistanceFunctions import distancesC_matrix

from PreProcessing import eliminate_unwanted

path = 'C:\\Users\\nicol\\Desktop\\Uniandes\\2020-1 Investigacion\\Results D_PPrk'


data0, titles0, data_classess0 = load_distances_matrices()
data, titles, data_classess = load_distances_matrices(path = path)


name_df = titles[0]
df = data[0]
classess = data_classess[0]

df, classess = eliminate_unwanted(df,classess)

dfC = distancesC_matrix(df,classess)




