# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:14:09 2023

@author: cfaccini
"""

import numpy as np
import math
from matplotlib import pyplot as plt 

#calculate and plot unet for each VLP + dend, at the Ic:
#1) each at the respective sigmahc
#2) all at a same sigmahc ( for each sigmahc we use)

#==============================================================
#yukawa potential:
    
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
    
#lj1 is the modified LJ potential:
    
def lj1(r, sigmahc, d1, d2):
    rmaxlj = sigmahc*(2**(1/6))  #lj cutoff without delta
    delta = (d1+d2)/2 - sigmahc
    rcut = rmaxlj + delta
    
    aux = sigmahc/(r - delta)
    ulj = 1+ 4*(pow(aux, 12) - pow(aux, 6))
    # ulj = 4*(pow(aux, 12) - pow(aux, 6))
    ulj[r<delta] = math.inf         #this is just because for r<delta, ulj = infty
    ulj[r>rcut] = 0.
    
    uljcut = ulj[r==rcut]
    
    return ulj, rcut, uljcut

#==============================================================
D = 56 # in nm. NP diameter
dd = 6.7 # in nm. dendrimer diameter
lb = 0.714 # bjerrum lenth in water, room temp.
rtouch = (D + dd)/2

r = np.linspace(0.001, 100, 10000)  #r is in nanometers
  
#sigmahc for the interaction between VLPs and dendrimers:

#Charges in e: 
# QV = [-600, -1080]
QV = [-600, -1080, -1500, -2085]
qd = 45

#estimated Ic in M
c = [0.080, 0.160, 0.25, 0.510]
kappa = 3.287*np.sqrt(c)

#calculate the yukawa potentials between each VLP-dend combo:

ue0 = yukawa(r, QV[0], qd, kappa[0], D, dd)
ue1 = yukawa(r, QV[1], qd, kappa[1], D, dd)
ue2 = yukawa(r, QV[2], qd, kappa[2], D, dd)
ue3 = yukawa(r, QV[3], qd, kappa[3], D, dd)


#sigmahc for the interaction between VLPs and dendrimers, in nm:
sigmahc = [4.15, 4.45, 4.75, 5.15]
rmaxlj = np.zeros(len(QV))
for i in range(len(QV)):
    rmaxlj[i] = sigmahc[i]*(2**(1/6))  #lj cutoff without delta    
rmax_ru = rmaxlj/D

#calculate the mod lj potentials between VLP-dend for each sigmahc value:

ulj0, rcut0, uljcut0 = lj1(r, sigmahc[0], D, dd)
ulj1, rcut0, uljcut0 = lj1(r, sigmahc[1], D, dd)
ulj2, rcut0, uljcut0 = lj1(r, sigmahc[2], D, dd)
ulj3, rcut0, uljcut0 = lj1(r, sigmahc[3], D, dd)

#calculate the net potentials:
unet00 = ue0 + ulj0     #K2, sigmahc=4.15
unet01 = ue0 + ulj1     #K2, sigmahc=4.45
unet02 = ue0 + ulj2     #K2, sigmahc=4.75
unet03 = ue0 + ulj3     #K2, sigmahc=5.15

unet10 = ue1 + ulj0     #Q2, sigmahc=4.15
unet11 = ue1 + ulj1     #Q2, sigmahc=4.45
unet12 = ue1 + ulj2     #Q2, sigmahc=4.75
unet13 = ue1 + ulj3     #Q2, sigmahc=5.15

unet20 = ue2 + ulj0     #E2, sigmahc=4.15
unet21 = ue2 + ulj1     #E2, sigmahc=4.45
unet22 = ue2 + ulj2     #E2, sigmahc=4.75
unet23 = ue2 + ulj3     #E2, sigmahc=5.15

unet30 = ue3 + ulj0     #EEE2, sigmahc=4.15
unet31 = ue3 + ulj1     #EEE2, sigmahc=4.45
unet32 = ue3 + ulj2     #EEE2, sigmahc=4.75
unet33 = ue3 + ulj3     #EEE2, sigmahc=5.15

#on to the plots:
# plt.figure()
# plt.rcParams.update({'font.size': 10})
# plt.title('Net potentials for each VLP-dend, at respective Ic and $\sigma_{hc}$')
# plt.xlabel('r (nm)')
# plt.ylabel('$u_{net}$ ($k_B$T)')    
# plt.plot(r, unet00, label = 'K2 at 75 mM, $\sigma_{hc}$=4.15nm')
# plt.plot(r-0.535, unet11, label = 'Q2 at 160 mM, $\sigma_{hc}$=4.45nm')
# plt.plot(r-0.402, unet22, label = 'E2 at 250 mM, $\sigma_{hc}$=4.75nm')
# plt.plot(r, unet33, label = 'EEE2 at 560 nm, $\sigma_{hc}$=5.15nm')
# plt.axhline(y = 0, color ='black', linestyle = '-', lw = 0.5)
# plt.axhline(y = -4.55, color ='black', linestyle = '--', lw = 0.5)
# plt.axvline(x = rtouch, color ='black', linestyle = '--', lw = 0.5)
# plt.xlim(29, 37)
# plt.ylim(-6, 5)

# plt.figure()
# plt.rcParams.update({'font.size': 10})
# plt.title('Net potentials for each VLP-dend at respective Ic, and $\sigma_{hc}$=4.15 nm')
# plt.xlabel('r (nm)')
# plt.ylabel('$u_{net}$ ($k_B$T)')    
# plt.plot(r, unet00, label = 'K2 at 75 mM')
# plt.plot(r, unet10, label = 'Q2 at 160 mM')
# plt.plot(r, unet20, label = 'E2 at 250 mM')
# plt.plot(r, unet30, label = 'EEE2 at 560 nm')
# plt.axhline(y = 0, color ='black', linestyle = '-', lw = 0.5)
# plt.axhline(y = -4.55, color ='black', linestyle = '--', lw = 0.5)
# plt.axvline(x = rtouch, color ='black', linestyle = '--', lw = 0.5)
# plt.xlim(29, 37)
# plt.ylim(-6, 5)

# plt.figure()
# plt.rcParams.update({'font.size': 10})
# plt.title('Net potentials for each VLP-dend at respective Ic, and $\sigma_{hc}$=4.45 nm')
# plt.xlabel('r (nm)')
# plt.ylabel('$u_{net}$ ($k_B$T)')    
# plt.plot(r, unet01, label = 'K2 at 75 mM')
# plt.plot(r, unet11, label = 'Q2 at 160 mM')
# plt.plot(r, unet21, label = 'E2 at 250 mM')
# plt.plot(r, unet31, label = 'EEE2 at 560 nm')
# plt.axhline(y = 0, color ='black', linestyle = '-', lw = 0.5)
# plt.axhline(y = -4.55, color ='black', linestyle = '--', lw = 0.5)
# plt.axvline(x = rtouch, color ='black', linestyle = '--', lw = 0.5)
# plt.xlim(29, 37)
# plt.ylim(-6, 5)

# plt.figure()
# plt.rcParams.update({'font.size': 10})
# plt.title('Net potentials for each VLP-dend at respective Ic, and $\sigma_{hc}$=4.75 nm')
# plt.xlabel('r (nm)')
# plt.ylabel('$u_{net}$ ($k_B$T)')    
# plt.plot(r, unet02, label = 'K2 at 75 mM')
# plt.plot(r, unet12, label = 'Q2 at 160 mM')
# plt.plot(r, unet22, label = 'E2 at 250 mM')
# plt.plot(r, unet32, label = 'EEE2 at 560 nm')
# plt.axhline(y = 0, color ='black', linestyle = '-', lw = 0.5)
# plt.axhline(y = -4.55, color ='black', linestyle = '--', lw = 0.5)
# plt.axvline(x = rtouch, color ='black', linestyle = '--', lw = 0.5)
# plt.xlim(29, 37)
# plt.ylim(-6, 5)

plt.figure()
plt.rcParams.update({'font.size': 10})
plt.title('Net potentials for each VLP-dend at respective Ic (cv=370nM) ')
plt.xlabel('r (nm)')
plt.ylabel('$u_{net}$ ($k_B$T)')    
plt.plot(r, unet00, label = 'K2 at 75 mM')
plt.plot(r, unet11, label = 'Q2 at 150 mM')
plt.plot(r, unet22, label = 'E2 at 240 mM')
plt.plot(r, unet33, label = 'EEE2 at 550 nm')
plt.axhline(y = 0, color ='black', linestyle = '-', lw = 0.5)
plt.axhline(y = -4.5, color ='black', linestyle = '--', lw = 0.5)
plt.axvline(x = rtouch, color ='black', linestyle = '--', lw = 0.5)
plt.xlim(29, 37)
plt.ylim(-6, 5)



