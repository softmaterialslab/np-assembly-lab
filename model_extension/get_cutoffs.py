# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 10:49:37 2022

@author: cfaccini
"""

#calculate the Yukawa and LJ potentials for the VLP-dendrimer interaction

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
    

def lj(r, sigmahc, d1, d2):
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

#============================    
plot_uy = 0     #1 plots, 0 doesn't
plot_lj = 0     #1 plots, 0 doesn't 
plot_net = 1     #1 plots, 0 doesn't 

calc_cutoff = 0     #for calculating the Yukawa cutoff
#============================

qd = 45  #dendrimer charge, units of e
Qv = -1500  #VLP charge, units of e

Dv = 56 #VLP diameter, in nm
dd = 6.7 #dendrimer diameter, in nm

#============================

c = 0.225  #salt concentration in Molars
kappa = 3.287*np.sqrt(c)

sigmahc = 0 #in nm
rmaxlj = sigmahc*(2**(1/6))  #lj cutoff without delta
rmax_ru = rmaxlj/Dv

print('Potentials calculated for c=', c, 'in Molars')
print('sigma_hc = ', sigmahc, 'nm, or ', sigmahc/Dv, 'in reduced units')
print('LJ cutoff without delta = ', rmaxlj, 'nm, or ', rmax_ru, 'in reduced units')
r = np.linspace(0.001, 100, 10000)

#calculate Yukawea potentials:
ue11 = yukawa(r, Qv, Qv, kappa, Dv, Dv)
ue12 = yukawa(r, Qv, qd, kappa, Dv, dd)
ue22 = yukawa(r, qd, qd, kappa, dd, dd)

#find cut-offs for Yukawa:
if calc_cutoff == 1:    
    val11 = np.where(ue11 < 0.005)
    index11 = val11[0]
    re11 = r[index11[0]]
    val12 = np.where(np.absolute(ue12) <= 0.005)
    index12 = val12[0]
    re12 = r[index12[0]]
    val22 = np.where(ue22 <= 0.005)
    index22 = val22[0]
    re22 = r[index22[0]]
    
    print('cutoff V-V_ES=', re11 , 'nm, or', re11/Dv , 'in reduced units')
    print('cutoff V-d_ES=', re12 , 'nm, or', re12/Dv , 'in reduced units')
    print('cutoff d-d_ES=', re22 , 'nm, or', re22/Dv , 'in reduced units')

#calculate (modified) lj potentials:
    
ulj11, rcut11, uljcut11 = lj(r, sigmahc, Dv, Dv)
ulj12, rcut12, uljcut12 = lj(r, sigmahc, Dv, dd)
ulj22, rcut22, uljcut22 = lj(r, sigmahc, dd, dd)

delta11 = Dv - sigmahc
d11_ru = delta11/Dv
delta12 = (Dv + dd)/2 - sigmahc
d12_ru = delta12/Dv
delta22 = dd - sigmahc
d22_ru = delta22/Dv

#calculate unet:

unet11 = ue11 + ulj11
unet12 = ue12 + ulj12
unet22 = ue22 + ulj22


closest = np.min(unet12)
val_closest = np.where(unet12==closest)
index = val_closest[0]
rclosest = r[index[0]]

print('distance of closest approach is ', rclosest, ' in nm, or ', rclosest/Dv, ' in reduced units')
print('V-d $u_{net}$ at $r_{closest}$ is ', closest, ' $k_BT$')

#plot Yukawa potentials:
if plot_uy == 1:
    # plt.figure()
    # plt.rcParams.update({'font.size': 20})
    # plt.title('Yukawa potential, 1-1')
    # plt.xlabel('r (nm)')
    # plt.ylabel('$u_y$ ($k_B$T)')
    # plt.ylim(-0.5, 10)
    # plt.plot(r, ue11, label = '1-1')
    
    # plt.figure()
    # plt.rcParams.update({'font.size': 20})
    # plt.title('Yukawa potential, 2-2')
    # plt.xlabel('r (nm)')
    # plt.ylabel('$u_y$ ($k_B$T)')
    # plt.ylim(-0.5, 10)
    # plt.plot(r, ue22, label = '2-2')
    
    plt.figure()
    plt.rcParams.update({'font.size': 20})
    plt.title('Yukawa potential, 1-2')
    plt.xlabel('r (nm)')
    plt.ylabel('$u_y$ ($k_B$T)')
    plt.ylim(-10, 0.5)
    plt.plot(r, ue12, label = '1-2')
   
#plot LJ potentials:
if plot_lj == 1:
    # plt.figure()
    # plt.rcParams.update({'font.size': 20})
    # plt.title('LJ potential, 1-1')
    # plt.xlabel('r (nm)')
    # plt.ylabel('$u_{lj}}$ ($k_B$T)')
    # plt.xlim(50, 60)
    # plt.ylim(-0.01, 10)
    # plt.plot(r, ulj11, label = '1-1')
    
    # plt.figure()
    # plt.rcParams.update({'font.size': 20})
    # plt.title('LJ potential, 2-2')
    # plt.xlabel('r (nm)')
    # plt.ylabel('$u_{lj}}$ ($k_B$T)')
    # plt.xlim(5, 20 )
    # plt.ylim(-0.01, 10)
    # plt.plot(r, ulj22, label = '2-2')
    
    plt.figure()
    plt.rcParams.update({'font.size': 20})
    plt.title('LJ, 1-2')
    plt.xlabel('r (nm)')
    plt.ylabel('$u_{lj}}$ ($k_B$T)')
    plt.xlim(30, 40)
    plt.ylim(-0.01, 10)
    plt.plot(r, ulj12, label = '1-2')

#plot net potential:
if plot_net ==1:
    # plt.figure()
    # plt.rcParams.update({'font.size': 20})
    # plt.title('net potential, 1-1')
    # plt.xlabel('r (nm)')
    # plt.ylabel('$u_{net}}$ ($k_B$T)')
    # plt.xlim(55, 60)
    # plt.ylim(-5, 10)
    # plt.plot(r, unet11, label = '1-1')    

    plt.figure()
    plt.rcParams.update({'font.size': 20})
    plt.title('net potential, 1-2')
    plt.xlabel('r (nm)')
    plt.ylabel('$u_{net}}$ ($k_B$T)')
    plt.xlim(30, 40)
    plt.ylim(-5, 10)
    plt.plot(r, unet12, label = '1-2')    

    # plt.figure()
    # plt.rcParams.update({'font.size': 20})
    # plt.title('net potential, 2-2')
    # plt.xlabel('r (nm)')
    # plt.ylabel('$u_{net}}$ ($k_B$T)')
    # plt.xlim(5, 20)
    # plt.ylim(-5, 10)
    # plt.plot(r, unet22, label = '2-2')    


# plt.figure()
# plt.rcParams.update({'font.size': 20})
# plt.title('Potentials, 1-1')
# plt.xlabel('r (nm)')
# plt.ylabel('$u_{lj}}$ ($k_B$T)')
# plt.xlim(55, 60)
# plt.ylim(-0.01, 10)
# plt.plot(r, ue11, label = 'Yukawa 1-1')
# plt.plot(r, ulj11, label = 'LJ 1-1')
# plt.plot(r, unet11, label = 'net potential 1-1')





