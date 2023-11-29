# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 17:19:17 2023

@author: cfaccini
"""

import numpy as np
import math
from matplotlib import pyplot as plt 


def yukawa(r, q1, q2, kappa, d1, d2):
    lb = 0.714 #Bjerrum length, in nm
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
Qv = -2122  #VLP charge, units of e

Dv = 56 #VLP diameter, in nm
dd = 6.7 #dendrimer diameter, in nm

# sigmahc = 5.15 #in nm

#============================
# salt concentrations in MOLARS
cmin = 0.01
cmax = 0.7
cstep = 0.01

c = np.arange(cmin, cmax, cstep)
kappa = 3.287*np.sqrt(c)

VV_es = np.zeros(len(c))
Vd_es = np.zeros(len(c))
dd_es = np.zeros(len(c))

with open('cutoffs.txt', 'w') as file:
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
        
        VV_es[i] = re11/Dv
        Vd_es[i] = re12/Dv
        dd_es[i] = re22/Dv
        
        file.write(f'{salt}     {re11/Dv}   {re12/Dv}   {re22/Dv}\n')

file.close()