"""
Autor: Nicolas Orlando Lopez Cuellar
Objetivo: Peak Metrics
"""

################################################################
###################### IMOPRT MODULES ##########################
################################################################

import numpy as np
import pandas as pd

from scipy.optimize import minimize
from statistics import mode

################################################################
#################### PEAK METRIC ###############################
################################################################
# Distance from peak to sample
def d_pP(p,P,prm):
    q1 = prm['q1']
    delta = prm['delta']
    
    out = 0
    for j in range(P.shape[0]):
        pj = P.iloc[j]
        # Distance measure
        out += (1/np.asarray([np.abs(p['Angle'] - pj['Angle']), delta]).max())**(q1)
    out = 1/out**(1/q1)
    return out
    
# Distance from sample to sample
def D_PP(P1,P2,prm):
    
    q2 = prm['q2']
    # First sample distance
    out1 = 0
    for i in range(len(P1)):
        out1 += np.abs((d_pP(P1.iloc[i], P2, prm)))**(q2) 
    out1 **= (1/q2)
    # Second sample distance
    out2 = 0
    for i in range(len(P2)):
        out2 += np.abs(d_pP(P2.iloc[i], P1, prm))**(q2) 
    out2 **= (1/q2)
    # Total
    out = out1/(len(P1)**(1/q2)) + out2/(len(P2)**(1/q2))
    
    return out

# Proportional distance from sample to sample
def D_PPpr(P1,P2,prm):
    
    q2 = prm['q2']
    gamma = prm['gamma']
    
    # Get maximum intensity
    max1 = P1.max(axis= 0)['Intensity']
    max2 = P2.max(axis= 0)['Intensity']
    
    # First sample distance
    out1 = 0
    for i in range(len(P1)):
        out1 += ((P1.iloc[i]['Intensity']/max1)**gamma)*np.abs((d_pP(P1.iloc[i], P2, prm)))**(q2) 
    out1 **= (1/q2)
    # Second sample distance
    out2 = 0
    for i in range(len(P2)):
        out2 += ((P2.iloc[i]['Intensity']/max2)**gamma)*np.abs(d_pP(P2.iloc[i], P1, prm))**(q2) 
    out2 **= (1/q2)
    # Total
    out = out1/(len(P1)**(1/q2)) + out2/(len(P2)**(1/q2))
    
    return(out)
    
# Ranked distance from sample to sample
def D_PPrk(P1,P2,prm):
    
    q2 = prm['q2']
    beta = prm['beta']
    
    # Organize samples by intensity
    P1 = P1.sort_values(by = ['Intensity'], ascending = False)
    P2 = P2.sort_values(by = ['Intensity'], ascending = False)

    # First sample distance
    out1 = 0
    for i in range(len(P1)):
        out1 += beta**i*(np.abs((d_pP(P1.iloc[i], P2, prm)))**(q2))
    out1 **= (1/q2)
    # Second sample distance
    out2 = 0
    for i in range(len(P2)):
        out2 += beta**i*(np.abs((d_pP(P2.iloc[i], P1, prm)))**(q2))
    out2 **= (1/q2)
    # Total
    out = out1/(len(P1)**(1/q2)) + out2/(len(P2)**(1/q2))
    
    return(out)

# Distance from sample to sample with alpha optimization
def D_PPalpha(P1,P2,prm, function = D_PP):
    # Transformation to required format
    # fun_D1 : Function for optimizing alpha
    def fun_alpha(alpha):
        P2_tmp = list(np.asarray(P2) - alpha)
        out = function(P1, P2_tmp, prm)
        return out
    
    alpha0 = 0
    
    res = minimize(fun_alpha, alpha0, method='nelder-mead',
                   options={'xtol': 1e-8, 'disp': True})
    
    distance = res['fun']
    alpha = res['x'][0]
    
    return {'Distance': distance , 'alpha': alpha}

################################################################
#################### DISTANCES MATRIX ##########################
################################################################
    
# Distances matrix
def distances_matrix(classess, list_peaks, prm, D = D_PP):
    # Inicialize
    distances = np.zeros(shape=(len(classess),len(classess)))
    # Progress inicialize
    idx = 1
    
    # Loop over all elements
    n = len(classess)
    for i in range(n):
        # Looop over all next elements
        for j in range(i,n):
            # Progress update
            print(str(idx) + '/' + str(int(n*(n-1)/2 + n)))
            # Calculate distance
            dist = D(list_peaks[i],list_peaks[j],prm)
            # Save distance (Symmetric matrix)
            distances[i,j] = dist
            distances[j,i] = dist
            
            idx = idx + 1
         
    return pd.DataFrame(distances)

def distancesC_matrix(distances_matrix, classess):
    df = pd.DataFrame(distances_matrix).copy()
    df['classess'] = classess
    
    df = df.groupby(['classess']).mean()
                
    return df.T


################################################################
#################### RESULTS GATHERING #########################
################################################################
    

def KNN_predict(distances_matrix, classess, k):
    predictions = []
    # Creates prediction for every row
    for i in range(distances_matrix.shape[0]):
        # Select row
        tmp_dist = list(distances_matrix[i])
        # Create classess copy 
        tmp_class = classess.copy()
        
        # Eliminates self from distance list
        tmp_dist.pop(i)
        tmp_class.pop(i)
        
        # Finds nearest distances
        k_nearest = np.sort(tmp_dist)
        if k == 1:
            k_nearest = [k_nearest[0]]
        else:
            k_nearest = k_nearest[0:k]
        
        # Sves classess from elements
        k_classes = [classess[j] for j in range(len(tmp_dist)) if tmp_dist[j] in k_nearest]
        predictions.append(mode(k_classes))
        
    return predictions



    
################################################################
#################### ALPHA OPTIMIZATION ########################
################################################################



################################################################
#################### LOSS FUNCTION #############################
################################################################
    
        
    
    
    
    
    
    
    
    