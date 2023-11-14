# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:51:15 2022

@author: cfaccini
writes lammps script for specific Qv, qd, sigmahc and c
"""
import numpy as np
import math
import os
from pathlib import Path
from matplotlib import pyplot as plt 

#=====================================================
#Charges:
    #EEE2= -2085
    #E2 = -1500
    #Q2 = -1080
    #K2 = -600

steps = 1e6     
    
#charges in e:
Q1 = -1500    #charge of VLP1 usually the highest-charge
Q2 = -600    #charge of VLP2
qd = 45         #dendrimer charge

D = 56 # in nm. NP diameter
dd = 6.7 # in nm. dendrimer diameter
lb = 0.714 # bjerrum lenth in water, room temp.

# c = input('input salt concentration in Molars: ')
# c = float(c)
c = 0.05
kappa = np.sqrt(8 * np.pi * lb * 0.6022*c)

#calculate values in LJ units for LAMMPS:
    
NPcharge1 = (Q1 * (np.exp((1.64399 * D) * np.sqrt(c)) / (1 + ((1.64399 * D) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)
NPcharge2 = (Q2 * (np.exp((1.64399 * D) * np.sqrt(c)) / (1 + ((1.64399 * D) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)
dendcharge = (qd * (np.exp((1.64399 * dd) * np.sqrt(c)) / (1 + ((1.64399 * dd) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)

userInputSalt = D * np.sqrt(8*np.pi*lb*0.6022*c)     #in reduced units

# sigmahc = input('input sigma_hc value in nm (default is 4.5): ')
# sigmahc = float(sigmahc)
sigmahc13 = 4.75
sigmahc23 = 4.15    #attention! this is usually the smaller value!

sigmahc13_ru = sigmahc13/D  #sigma_hc in reduced units
sigmahc23_ru = sigmahc23/D  #sigma_hc in reduced units

rmaxlj13 = sigmahc13*(2**(1/6))  #lj cutoff without delta. I"m assuming sigmahc13 is the largest.
rmax13_ru = rmaxlj13/D

#=====================================================

def yukawa(r, q1, q2, kappa, d1, d2):
    lb = 0.714 #Bjerrum length, in nm
    aux1 = (q1/(1+kappa*(d1/2)))*np.exp(kappa*(d1/2))
    aux2 = (q2/(1+kappa*(d2/2)))*np.exp(kappa*(d2/2))
    ue = (1/r)*aux1*aux2*lb*np.exp(-kappa*r)
    
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

#lj2 is the unmodified LJ potential:

def lj2(r, d1, d2):
    sigma = (d1+d2)/2
    rmaxlj = sigma*(2**(1/6))  #lj cutoff without delta
    rcut = rmaxlj
    
    aux = sigma/r
    ulj = 1 + 4*(pow(aux, 12) - pow(aux, 6))
    # ulj = 4*(pow(aux, 12) - pow(aux, 6))
    # ulj[r<delta] = math.inf         #this is just because for r<delta, ulj = infty
    ulj[r>rcut] = 0.
    
    uljcut = ulj[r==rcut]
    
    return ulj, rcut, uljcut

r = np.linspace(0.001, 100, 10000)  #r is in nanometers

#calculate Yukawa potentials:
#VLP-VLP
ue11 = yukawa(r, Q1, Q1, kappa, D, D)
ue12 = yukawa(r, Q1, Q2, kappa, D, D)
ue22 = yukawa(r, Q2, Q2, kappa, D, D)

val11 = np.where(ue11 <= 0.005)
index11 = val11[0]
re11 = r[index11[0]]
val12 = np.where(ue12 <= 0.005)
index12 = val12[0]
re12 = r[index12[0]]
val22 = np.where(ue22 <= 0.005)
index22 = val22[0]
re22 = r[index22[0]]

#dend-VLP:
ue13 = yukawa(r, Q1, qd, kappa, D, dd)
ue23 = yukawa(r, Q2, qd, kappa, D, dd)

val13 = np.where(np.absolute(ue13) <= 0.005)
index13 = val13[0]
re13 = r[index13[0]]
val23 = np.where(np.absolute(ue23) <= 0.005)
index23 = val23[0]
re23 = r[index23[0]]

#dend-dend
ue33 = yukawa(r, qd, qd, kappa, dd, dd)

val33 = np.where(np.absolute(ue33) <= 0.005)
index33 = val33[0]
re33 = r[index33[0]]

#cutoffs:
VV11_es = re11/D    #ES 1-1 cutoff in reduced units
VV22_es = re22/D    #ES 2-2 cutoff in reduced units
VV12_es = re12/D    #ES 1-2 cutoff in reduced units

Vd13_es = re13/D
Vd23_es = re23/D
dd_es = re33/D

Vd_es = Vd13_es

#calculate lj potentials:
    
#VLP-VLP: unmod lj potential   
ulj11, rcut11, uljcut11 = lj2(r, D, D)
ulj12, rcut12, uljcut12 = lj2(r, D, D)
ulj22, rcut22, uljcut22 = lj2(r, D, D)

delta11 = 0
delta_VV = delta11/D

#VLP-dend: mod lj potentials
ulj13, rcut13, uljcut13 = lj1(r, sigmahc13, D, dd)
ulj23, rcut23, uljcut23 = lj1(r, sigmahc23, D, dd)

delta13 = (D + dd)/2 - sigmahc13
delta23 = (D + dd)/2 - sigmahc23
delta_Vd13 = delta13/D
delta_Vd23 = delta23/D

#dend-dend: unmod lj potential:
ulj33, rcut33, uljcut33 = lj2(r, dd, dd)    
delta33 = 0
delta_dd = delta33/D

#calculate net potentials:
unet13 = ue13 + ulj13
unet23 = ue23 + ulj23

rtouch = (D + dd)/2

saltconc=1000*c

plt.figure()
plt.rcParams.update({'font.size': 20})
plt.title('Net potential between VLP-dend, c=%i mM'%saltconc)
plt.xlabel('r ($nm$)')
plt.ylabel('$u_{net}$ ($k_B$T)')
plt.xlim(30, 37)
plt.ylim(-7, 5)
plt.axhline(y = 0, color ='black', linestyle = '-', lw = 0.5)
plt.axhline(y = -4.6, color ='black', linestyle = '--', lw = 0.5)
plt.axvline(x = rtouch, color ='black', linestyle = '-', lw = 0.5)
plt.plot(r, unet13, label = 'E2, $\sigma_{hc}$=%f' %sigmahc13)
plt.plot(r, unet23, label = 'K2, $\sigma_{hc}$=%f' %sigmahc23)

#=====================================================

def header():
    s = '''     
# 3D simulation of virus macroassembly

units lj
boundary p p p
atom_style hybrid charge sphere
neighbor	0.3	bin
neigh_modify	every	1	delay	0	check	yes '''
    return s

def datafile(filename):
    s = f'''
## Create Simulation Box, Atoms ##
#read_data	{filename}
#read_data	initCoords.assembly
read_restart    assemblyRestart.1000000

## Group Atoms by Type ##
group virus1    type	1
group virus2    type	2
group dend      type	3
group allViruses union virus1 virus2

## Defining Particle/Medium Properties ##
mass	1	1
mass	2	1
mass	3	0.0029024	# relative mass of dendrimer to P22
dielectric	78.54
 '''
    return s

def charge(npcharge1, npcharge2, dendcharge):
    s = f'''
set	type	1	charge	{npcharge1}	    # qV1_DLVO (in LJ units)   
set	type	2	charge	{npcharge2}	     # qV2_DLVO (in LJ units)  
set	type	3	charge	{dendcharge}	# qD_DLVO (in LJ units) 

## Ascribing Initial Velocities ##
velocity	all	create	1.	4928459	rot	yes	dist	gaussian	units	box	# 1-kB*T,random seed,zero net ang.mom.,gauss from MB stats
'''
    return s

def cutoffs(ljcut, salt, es_global, delta_VV, VV11_es, VV22_es, VV12_es, sigmahc13, sigmahc23, delta_Vd13, delta_Vd23, Vd_es, dd_es):
    s = f'''
## Ascribing interparticle potentials: ##
pair_style	hybrid/overlay	lj/expand	{ljcut}	coul/debye	{salt}	{es_global}	# LJ_cut without delta, kappa, Global ES_cut
pair_coeff	1	1	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	1	1	coul/debye	{VV11_es}	# V1-V1 ES_cut
pair_coeff	2	2	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	2	2	coul/debye	{VV22_es}	# V2-V2 ES_cut
pair_coeff	1	2	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	1	2	coul/debye	{VV12_es}	# V1-V2 ES_cut
pair_coeff	1	3	lj/expand	1	{sigmahc13}	{delta_Vd13}	# epsilon, sigma_hc, delta_V1-D
pair_coeff	1	3	coul/debye	{Vd_es}	# V-D ES_cut
pair_coeff	2	3	lj/expand	1	{sigmahc23}	{delta_Vd23}	# epsilon, sigma_hc, delta_V2-D
pair_coeff	2	3	coul/debye	{Vd_es}	# V-D ES_cut
pair_coeff	3	3	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_D-D
pair_coeff	3	3	coul/debye	{dd_es}	# D-D ES_cut
pair_modify	shift	yes	# the additive e_LJ for repulsion-only      
    '''
    return s

def footer():
    s = '''

## Ensemble Fixes (+ for output) ##
variable	myTStep	equal	0.000025
timestep	${myTStep}
variable	myDStep	equal	1000
fix	ens	all	nvt	temp	1.	1.	0.0025	# T_start, T_stop, T_damp=100*timestep

## Define Computes for Output ##
compute	myVirus1T	virus1	temp
compute	myVirus2T	virus2	temp
compute	myDendT 	dend	temp
compute	virus1PotVec	virus1	pe/atom
compute virus1KeVec 	virus1	ke/atom
compute	virus2PotVec	virus2	pe/atom
compute virus2KeVec 	virus2	ke/atom
compute dendPotVec	dend	pe/atom
compute dendKeVec	dend	ke/atom
# compute	VirusPEperatom	virus	reduce	ave c_virusPotVec
# compute	VirusKEperatom	virus	reduce	ave c_virusKeVec
# compute	DendPEperatom	dend	reduce	ave c_dendPotVec
# compute	DendKEperatom	dend	reduce	ave c_dendKeVec

## Defining Output Information ##

dump	posD	all	custom	${myDStep}	dump.melt	id	type	x	y	z	# c_atomPot	c_atomKin
dump    allV    allViruses  custom  ${myDStep}    outfiles/dump.melt    id	type	x	y	z	# c_atomPot	c_atomKin 
dump	v1OnlyD	virus1	custom	1000	outfiles/dumpVirus1Only.melt	id	type	x	y	z	# c_atomPot	c_atomKin
dump	v2OnlyD	virus2	custom	1000	outfiles/dumpVirus2Only.melt	id	type	x	y	z	# c_atomPot	c_atomKin
#dump	posAvgD	all	custom	1250000	dumpAvg.melt	id	type	f_posAvg[1]	f_posAvg[2]	f_posAvg[3]
#dump	posInsD	all	custom	625000	dump.*	id	type	x	y	z

thermo_style	custom	step etotal  pe  ke  #press
thermo_modify norm no
thermo	2500

restart		1000000	outfiles/assemblyRestart.*	# creates 3 restart files throughout run
run		10000000

undump  posD
undump	allV
undump	v1OnlyD
undump	v2OnlyD
# uncompute	myVirus1T
# uncompute	myVirus2T
# uncompute	myDendT
# uncompute	virus1PotVec
# uncompute	myVirus1Pot
# uncompute	virus2PotVec
# uncompute	myVirus2Pot
# uncompute	dendPotVec
# uncompute	myDendPot
    '''
    return s

script = header()
script+=datafile('filename')            #datafile with initial coordinates
script+= charge(NPcharge1, NPcharge2, dendcharge)         #VLP1 charge, VLP2 charge, dendrimer charge (in reduced units)
script+= cutoffs(rmax13_ru, userInputSalt, VV11_es, delta_VV, VV11_es, VV22_es, VV12_es, sigmahc13_ru, sigmahc23_ru, delta_Vd13, delta_Vd23, Vd_es, dd_es)
script+= footer()

