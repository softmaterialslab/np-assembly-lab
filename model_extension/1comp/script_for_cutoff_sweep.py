# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 13:30:56 2023

@author: cfaccini
creates the lines to be added to the parameter weep file, with the cutoff values for each salt concentration.
Calculations done for EEE2 Q=-2085e, q=45e. Cutoff parameter is |ue|<0.005kBT
"""

import numpy as np

lb = 0.714 #Bjerrum length, in nm
aux = np.sqrt(8*lb*0.6022*np.pi)    # the 0.6022 converts the unit of c from Molars to nm^-3

    
def yukawa(r, q1, q2, kappa, d1, d2):
    aux1 = (q1/(1+kappa*(d1/2)))*np.exp(kappa*(d1/2))
    aux2 = (q2/(1+kappa*(d2/2)))*np.exp(kappa*(d2/2))
    ue = (1/r)*aux1*aux2*lb*np.exp(-kappa*r)
    val = np.where(np.absolute(ue) <= 0.005)
    index = val[0]
    re = r[index[0]]
    ue[r>re] = 0.
    return ue
    
r = np.linspace(0.001, 100, 10000)

qd = 45  #dendrimer charge, units of e
Qv = -2085  #VLP charge, units of e

Dv = 56 #VLP diameter, in nm
dd = 6.7 #dendrimer diameter, in nm

#INCLUDE HERE DESIRED SALT CONCENTRATIONS IN MOLARS:
#c = [0.6, 0.57, 0.55, 0.53, 0.5, 0.45, 0.4, 0.35, 0.32, 0.3, 0.28, 0.25, 0.2, 0.18, 0.16, 0.15, 0.14, 0.12, 0.1, 0.08, 0.075, 0.07, 0.06, 0.05, 0.04, 0.01]

# EEE2 concentrations:
c_EEE2 = [0.60, 0.57, 0.56, 0.55, 0.53, 0.50, 0.40, 0.20, 0.10, 0.04, 0.01]
# E2 concentrations:
c_E2 = [0.30, 0.28, 0.25, 0.24, 0.22, 0.20, 0.18, 0.15, 0.10, 0.04, 0.01] 
# Q2 concentrations:
c_Q2 = [0.20, 0.17, 0.16, 0.15, 0.14, 0.12, 0.10, 0.06, 0.04, 0.01]
# K2 concentrations:
c_K2 = [0.20, 0.15, 0.12, 0.10, 0.08, 0.75, 0.07, 0.06, 0.05, 0.04, 0.01]

concs = [c_EEE2, c_E2, c_Q2, c_K2]

VLPS = ['EEE2', 'E2', 'Q2', 'K2']

def header():
    s = '''
    #copy folowing lines to the sweep parameter file:
        '''
    return s

def firstc(salt, VVes, Vdes, ddes):
    s = f'''
    if [ "$USERSALTCONC" = {salt} ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="{VVes}"
        USERVLPLinkerEScutoff="{ddes}"
        USERLinkerEScutoff="{Vdes}" '''
               
    return s

def allc(salt, VVes, Vdes, ddes):
    s = f'''
    elif [ "$USERSALTCONC" = {salt} ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="{VVes}"
        USERVLPLinkerEScutoff="{ddes}"
        USERLinkerEScutoff="{Vdes}"     '''
               
    return s

def finish():
    s = '''
    fi    '''
    return s

cutoffs_EEE2 = header()
cutoffs_E2 = header()
cutoffs_Q2 = header()
cutoffs_K2 = header()

for j in range(len(VLPS)):
    VLP = VLPS[j]
    print(VLP)
    c = concs[j]
    kappa = aux*np.sqrt(c)

    for i in range(len(c)):
        salt = c[i]
        kappa1 = kappa[i]
        ue_VV = yukawa(r, Qv, Qv, kappa1, Dv, Dv)
        ue_Vd = yukawa(r, Qv, qd, kappa1, Dv, dd)
        ue_dd = yukawa(r, qd, qd, kappa1, dd, dd)
            
        val11 = np.where(ue_VV < 0.005)
        index11 = val11[0]
        re11 = r[index11[0]]
        val12 = np.where(np.absolute(ue_Vd) <= 0.005)
        index12 = val12[0]
        re12 = r[index12[0]]
        val22 = np.where(ue_dd <= 0.005)
        index22 = val22[0]
        re22 = r[index22[0]]
            
        VVes = re11/Dv
        Vdes = re12/Dv
        ddes = re22/Dv
        
        if j == 0:        
            if i == 0:
                cutoffs_EEE2+= firstc(salt, VVes, Vdes, ddes)
            else:
                cutoffs_EEE2+= allc(salt, VVes, Vdes, ddes)
        if j == 1:
            if i == 0:
                cutoffs_E2+= firstc(salt, VVes, Vdes, ddes)
            else:
                cutoffs_E2+= allc(salt, VVes, Vdes, ddes)
        if j == 2:
            if i == 0:
                cutoffs_Q2+= firstc(salt, VVes, Vdes, ddes)
            else:
                cutoffs_Q2+= allc(salt, VVes, Vdes, ddes)
        if j == 3:
            if i == 0:
                cutoffs_K2+= firstc(salt, VVes, Vdes, ddes)
            else:
                cutoffs_K2+= allc(salt, VVes, Vdes, ddes)
            
        
cutoffs_EEE2+= finish()
cutoffs_E2+= finish()
cutoffs_Q2+= finish()
cutoffs_K2+= finish()
        
        

