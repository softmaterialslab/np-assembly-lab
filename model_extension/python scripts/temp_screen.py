# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:54:59 2024



@author: camila
"""

import numpy as np
import math
from matplotlib import pyplot as plt 


#lb = 0.714 #Bjerrum length, in nm

e = 1.60217663*(pow(10, -19)) #C, ectron charge
e0 = 8.854*(pow(10, -12)) #F/m, vacuum permittivity
kb = 1.380649*(pow(10,-23)) #J/K, boltzman cte

###########################
#
# TEMPERATURE DEPENDENCE

T0 = 298
T1=278
T2=288
T3=323
T4=348


Tk = T1 #K, temperature
Tc = Tk - 273.15 # temp in C

T = np.linspace(5, 50, 50)
#er = 87.74 - 0.40008*Tc + (9.398e-4)*(Tc**2) - (1.410e-6)*(Tc**3)

er = 87.74 - 0.40008*T + (9.398e-4)*(T**2) - (1.410e-6)*(T**3)
er2 = 1.003*er

#from NIST:
T2 = [20, 25]
e2 = [80.37 , 78.54]

T3 = [278, 288, 298, 308, 318]
T3C = [5, 15, 25, 35, 45]

er3 = np.zeros(len(T3C))

for i in range(len(T3C)):
	er3[i] = 1.003*(87.74 - 0.40008*T3C[i] + (9.398e-4)*(T3C[i]**2) - (1.410e-6)*(T3C[i]**3))



plt.figure()
plt.plot(T, er)
plt.plot(T, er2, label = '0.3$\%$ correction')
plt.plot(T2, e2, 'ro', label = 'NIST values' )
plt.plot(T3C, er3, 'bs', label = 'test values')
plt.xlabel('T (C)')
plt.ylabel('$\epsilon$')
plt.tightlayout()