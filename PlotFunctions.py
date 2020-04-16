"""
Autor: Nicolas Orlando Lopez Cuellar
Objective: Functions for Plotting
"""
################################################################
#################### MODULES ###################################
################################################################

import numpy as np
import os

import matplotlib.pyplot as plt

# import matplotlib
# matplotlib.use('tkAgg')


from PreProcessing import eliminate_unwanted
from PreProcessing import find_angle

from DistanceFunctions import distancesC_matrix

from SaveLoadFunctions import load_distances_matrices



################################################################
#################### PARAMETERS ################################
################################################################

figure_size = (20,10)

colors = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']
colors = ['tab:' + color for color in colors]

################################################################
#################### PLOT ALL ###########3######################
################################################################
        
# Plot projections of all current folder distance matrices.
def plot_all_DM(projections = True, centroid_distances = True):
    # Load all distances Matrix
    distances, titles, data_classess  = load_distances_matrices()
    
    for i in range(len(distances)):
                        
        new = titles[i].split('.csv')[0]
        if projections:
            plot_projections(distances[i], data_classess[i] , new)
        if centroid_distances:
            plot_class_distances(distances[i], data_classess[i] , new)
            
################################################################
#################### PROJECTIONS ###############################
################################################################

# Plot projections for a specific distance matrix
# Plots 1 image for each class, each with 1 subplot for every other class.
def plot_projections(distance_matrix, classess, folder_images = 'Images', unwanted = ['Patata']):
    
    # Eliminates unwanted classess
    distance_matrix, classess = eliminate_unwanted(distance_matrix, classess, unwanted)
        
    # Get centroid distance matrix
    distances_centroids = distancesC_matrix(distance_matrix,classess)

    # Unique classess
    classess_unique = np.unique(np.array(classess))
    
    # Creates directory if it doesnt exists
    if not os.path.exists(folder_images):
        os.mkdir(folder_images)
        
    n_img = len(classess_unique)
    
    # Loops over every class
    for i in range(n_img):
        # Creates Figure
        fig = plt.figure(figsize= figure_size)
        
        # Create subplots for every other class
        for j in range(n_img):
            # Applies for different classess.
            if i != j:
                indexi = [idx for idx in distances_centroids.index if classess_unique[i] in idx]
                indexj = [idx for idx in distances_centroids.index if classess_unique[j] in idx]
    
                dfi = distances_centroids.loc[indexi]
                dfj = distances_centroids.loc[indexj]
    
                ax = fig.add_subplot(2,4,j+1)
                ax.scatter(dfi[dfi.columns[i]] , dfi[dfi.columns[j]], color= colors[i] , marker='o', s = 25)
                ax.scatter(dfj[dfj.columns[i]] , dfj[dfj.columns[j]], color= colors[j] , marker='x', s = 20)
            
                # Title
                ax.set_title(classess_unique[j])
                
                # x_label
                x_label = 'D ' + classess_unique[i]
                ax.set_xlabel(x_label)
                
                # y_label
                y_label = 'D ' + classess_unique[j]
                ax.set_ylabel(y_label)
        
        fig.suptitle(folder_images)
        
        # Save figure
        fig_title = folder_images + '/' +  classess_unique[i]  + ' - ' + folder_images + '.png'
        plt.savefig(fig_title)
        
        plt.close()
        
################################################################
#################### CLASS DISTANCES ###########################
################################################################
 
# Classess distances
def plot_class_distances(distance_matrix, classess, folder_images = 'Images', unwanted = ['Patata'], colors = colors):
        
    # Eliminates unwanted classess
    distance_matrix, classess = eliminate_unwanted(distance_matrix, classess, unwanted)
        
    # Get centroid distance matrix
    distances_centroids = distancesC_matrix(distance_matrix,classess)

    # Unique classess
    classess_unique = np.unique(np.array(classess))
        
    # Creates Imgage
    n_img = len(classess_unique)
    fig = fig = plt.figure(figsize= figure_size) 

    # Cretes subplot for every class
    for i in range(n_img):
        
        # Gets submatrix using only elements of the corresponding class
        df_sub = distances_centroids.iloc[[j for j in range(len(classess)) if classess[j] == classess_unique[i]]]
        df_sub = df_sub.copy()
        
        df_sub['sum'] = df_sub.sum(axis = 1)
        df_sub = df_sub.sort_values(by = ['sum'])
        
        df_sub = df_sub.drop(columns = ['sum'])
        
        # Creates x (Sample #)
        x = range(1,df_sub.shape[0]+1)
        
        ax = fig.add_subplot(2,4,i+1)

        # Creates scatter line for each centroid distance
        for j in range(n_img):
            # Creates y (Distance to corresponding class)
            y =  df_sub.iloc[:,[j]]
            
            ax.scatter(x,y, color = colors[j], marker = 'o', s = 40)
            ax.plot(x,y, color = colors[j])
            
        # Title
        ax.set_title(classess_unique[i])
        
        # x_label
        x_label = 'Sample #'
        ax.set_xlabel(x_label)
        
        # y_label
        y_label = 'Class Distance'
        ax.set_ylabel(y_label)
        
    fig.suptitle(folder_images)
        
    # Save figure
    fig_title = 'Centroid Distances - ' + folder_images + '.png'
    plt.savefig(fig_title)
        
################################################################
#################### PLOT SAMPLES ##############################
################################################################
    
def plot_all_samples(data,classess, folder_images = 'Samples'):
    return 1
    

# Plots diffractogram sample with peaks and valleys
    # colors: color for
def plot_sample(sample, name, path, peaks = None, valleys = None, colors = ['blue','red','green'], angle_zoom = None, angle_window = 4, save = True):
    
    # Full Window
    a_1 = 0
    a_n = sample.shape[0] - 1
    # Window with zoom
    if not(angle_zoom is None):
        min_angle = angle_zoom - angle_window
        max_angle = angle_zoom + angle_window
        
        if sample['Angle'][a_n] < max_angle:
            max_angle = sample['Angle'][a_n]
        if min_angle > max_angle or min_angle < sample['Angle'][a_1]:
            min_angle = sample['Angle'][a_1]
            
        # Bisection method for finding zoom

        pos = []        
        for ang in [min_angle,max_angle]:
            pos.append(find_angle(ang, sample))
            
        
        a_1 = pos[0]
        a_n = pos[1]
# =============================================================================
#         # Super slow method 
#         for i in range(sample.shape[0]-1):
#             if  (list(sample['Angle'])[i] < min_angle) and (list(sample['Angle'])[i + 1] > min_angle):
#                 a_1 = i
#             if  (list(sample['Angle'])[i] < max_angle) and (list(sample['Angle'])[i + 1] > max_angle):
#                 a_n = i
#                 break 
# =============================================================================
    fig = plt.figure() 
    
    ax = fig.add_subplot(111)
    
    ax.plot(list(sample['Angle'])[a_1:a_n], list(sample['Intensity'])[a_1:a_n], color = colors[0])
    if not (peaks is None):
        peaks = peaks[(peaks['Angle'] >= list(sample['Angle'])[a_1]) & (peaks['Angle'] <= list(sample['Angle'])[a_n])]
        ax.scatter(list(peaks['Angle']),list(peaks['Intensity']), color = colors[1])
    if not (valleys is None):
        valleys = valleys[(valleys['Angle'] >= list(sample['Angle'])[a_1]) & (valleys['Angle'] <= list(sample['Angle'])[a_n])]
        ax.scatter(list(valleys['Angle']),list(valleys['Intensity']), color = colors[2])
    
    fig.suptitle(name)
    
    if save:
        plt.show()
    else:
        plt.savefig(path + '\\' + name + '.png')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    