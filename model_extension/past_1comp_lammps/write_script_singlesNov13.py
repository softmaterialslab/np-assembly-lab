# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:51:15 2022

@author: cfaccini
writes lammps script for specific Qv, qd, sigmahc and c
"""
import numpy as np
import math
# import get_values
# import get_cutoffs
import os
from pathlib import Path
from matplotlib import pyplot as plt 

#=====================================================

# Qv = input('input VLP charge in e: ')
# Qv = float(Qv)
# qd = input('input dendrimer charge in e (default is 45): ')
# qd = float(qd)

Qv = -2085
qd = 45

D = 56 # in nm. NP diameter
dd = 6.7 # in nm. dendrimer diameter
lb = 0.714 # bjerrum lenth in water, room temp.

# c = input('input salt concentration in Molars: ')
# c = float(c)
c = 0.53
kappa = np.sqrt(8 * np.pi * lb * 0.602*c)

#calculate values in LJ units for LAMMPS:
# NPcharge = (Qv * (np.exp((1.64399 * D) * np.sqrt(c)) / (1 + ((1.64399 * D) * np.sqrt(c))))) * (1.60217663 * 1e-19) / (1.6011 * 1e-19)
# dendcharge = (qd * (np.exp((1.64399 * dd) * np.sqrt(c)) / (1 + ((1.64399 * dd) * np.sqrt(c))))) * (1.60217663  * 1e-19) / (1.6011 * 1e-19)

NPcharge = (Qv * np.exp(D/2 * np.sqrt(8*np.pi*lb*0.6022*c)) / (1+((D/2 * np.sqrt(8*np.pi*lb*0.6022*c))))) *  ((1.6021 * 1e-19) / (1.6011 * 1e-19))
dendcharge = (qd * np.exp(dd/2 * np.sqrt(8*np.pi*lb*0.6022*c)) / (1+((dd/2 * np.sqrt(8*np.pi*lb*0.6022*c))))) *  ((1.6021 * 1e-19) / (1.6011 * 1e-19))
                                          

userInputSalt = D * np.sqrt(8*np.pi*lb*0.6022*c)     #in reduced units

# sigmahc = input('input sigma_hc value in nm (default is 4.5): ')
# sigmahc = float(sigmahc)
sigmahc = 5.15

sigmahc_ru = sigmahc/D  #sigma_hc in reduced units

rmaxlj = sigmahc*(2**(1/6))  #lj cutoff without delta
rmax_ru = rmaxlj/D

rcut_VV = (2**(1/6)) #because sigma=D/D in this case
rcut_dd = (2**(1/6))*(dd/D) #because sigma=DD/DD in this case

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
ue11 = yukawa(r, Qv, Qv, kappa, D, D)   #V-V
ue12 = yukawa(r, Qv, qd, kappa, D, dd)  #V-d
ue22 = yukawa(r, qd, qd, kappa, dd, dd) #d-d

val11 = np.where(ue11 < 0.005)
index11 = val11[0]
re11 = r[index11[0]]
val12 = np.where(np.absolute(ue12) <= 0.005)
index12 = val12[0]
re12 = r[index12[0]]
val22 = np.where(ue22 <= 0.005)
index22 = val22[0]
re22 = r[index22[0]]

VV_es = re11/D  #ES cutoff in reduced units
Vd_es = re12/D
dd_es = re22/D


#calculate lj potentials:
    
ulj11, rcut11, uljcut11 = lj2(r, D, D)              #unmod lj for V-V
ulj12, rcut12, uljcut12 = lj1(r, sigmahc, D, dd)    #modified lj for V-d
ulj22, rcut22, uljcut22 = lj2(r, dd, dd)            #unmod lj for d-d

delta11 = 0
delta_VV = delta11/D
delta12 = (D + dd)/2 - sigmahc
delta_Vd = delta12/D
delta22 = 0
delta_dd = delta22/D

#calculate net potentials:
unet12 = ue12 + ulj12

rtouch = (D + dd)/2
saltconc=1000*c

# plt.figure()
# plt.rcParams.update({'font.size': 20})
# plt.title('Net potential between VLP-dend, c=%i mM'%saltconc)
# plt.xlabel('r ($nm$)')
# plt.ylabel('$u_{net}$ ($k_B$T)')
# plt.xlim(30, 37)
# plt.ylim(-7, 5)
# plt.axhline(y = 0, color ='black', linestyle = '-', lw = 0.5)
# plt.axhline(y = -4.5, color ='black', linestyle = '-', lw = 0.5)
# plt.axvline(x = rtouch, color ='black', linestyle = '-', lw = 0.5)
# plt.plot(r, unet12, label = 'K2: $\sigma_{hc}$=%f' %sigmahc)

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
read_data	initCoords1comp.assembly

## Group Atoms by Type ##
group virus type	1
group dend type	2

## Defining Particle/Medium Properties ##
mass	1	1
mass	2	0.0029024	# relative mass of dendrimer to P22
dielectric	78.54
 '''
    return s

def virus_charge(npcharge):
    s = f'''
set	type	1	charge	{npcharge}	# qV_DLVO (in LJ units)    
'''
    return s

def dend_charge(dendcharge):
    s = f'''
set	type	2	charge	{dendcharge}	# qD_DLVO (in LJ units)

## Ascribing Initial Velocities ##
velocity	all	create	1.	4928459	rot	yes	dist	gaussian	units	box	# 1-kB*T,random seed,zero net ang.mom.,gauss from MB stats

## Ascribing interparticle potentials: ##
'''
    return s

def cutoffs1(ljcut, salt, es_global):
    s = f'''

pair_style	hybrid/overlay	lj/expand	{ljcut}	coul/debye	{salt}	{es_global}	# LJ_cut without delta, kappa, Global ES_cut
    '''
    return s

def cutoffs_VV(VV_es, rcut_VV):
    s = f'''
pair_coeff	1	1	lj/expand	1	1.	0 {rcut_VV}	# epsilon, sigma_hc, delta_V-V, rcut_VV=2^(1/6) D/D
pair_coeff	1	1	coul/debye	{VV_es}	# V-V ES_cut   
    '''
    return s

def cutoffs_Vd(sigmahc, delta_Vd, Vd_es, ljcut):
    s = f'''
pair_coeff	1	2	lj/expand	1	{sigmahc}	{delta_Vd}  {ljcut}   	# epsilon, sigma_hc, delta_V-D
pair_coeff	1	2	coul/debye	{Vd_es}	# V-D ES_cut
  
    '''
    return s

def cutoffs_dd(dd_es, rcut_dd):
    s = f'''
pair_coeff	2	2	lj/expand	1	0.11964285714285713	0. {rcut_dd}	# epsilon, sigma_dd=6.7nm/56nm, delta_D-D, delta_d-d, rcut_VV=2^(1/6) d/D
pair_coeff	2	2	coul/debye	{dd_es}	# D-D ES_cut 
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

# compute	VirusPEperatom	virus	reduce	ave c_virusPotVec
# compute	VirusKEperatom	virus	reduce	ave c_virusKeVec
# compute	DendPEperatom	dend	reduce	ave c_dendPotVec
# compute	DendKEperatom	dend	reduce	ave c_dendKeVec


#print "OUTPUT COLUMNS: SIMULATION STEP NUMBER | TEMPERATURE | NP POTENTIAL ENERGY | SYSTEM VOLUME"

#restart	500000	outfiles/assemblyRestart.*	# creates 5 restart files up to equilibration; can comment this
#run	1500000    #run for 2.5 million without dumping anything

## Defining Output Information ##
dump	allV	all	custom	${myDStep}	outfiles/dump_all.melt	id	type	x	y	z	# c_atomPot	c_atomKin
dump	posD	virus	custom	${myDStep}	outfiles/dump_V.melt	id	type	x	y	z	# c_atomPot	c_atomKin


#thermo_style	custom	step	temp	c_myVirusT	c_myDendT	c_myVirusPot	c_myDendPot	etotal	ke	pe	vol	#press
thermo_style	custom	step etotal  pe  ke 
thermo_modify norm no
thermo	1000

restart	500000	outfiles/assemblyRestart.*	# creates restart files post equilibration; keep this
run	1000000

unfix	ens
undump	posD
undump  allV
#undump	vOnlyD


    '''
    return s

script = header()
script+=datafile('filename')            #datafile with initial coordinates
script+= virus_charge(NPcharge)         #VLP charge (in reduced units)
script+= dend_charge(dendcharge)        #dendrimer charge (in reduced units)
#first pair is V-V:
script+= cutoffs1(rcut_VV, userInputSalt, VV_es)  #ljcut without delta (in reduced units), userinputKAPPA (in reduced units), ES_global_cutoff (in reduced units)
script+= cutoffs_VV(VV_es, rcut_VV)
#next is V-d interactions:
script+= cutoffs_Vd(sigmahc_ru, delta_Vd, Vd_es, rmax_ru)    #sigmahc (in reduced units), delta_Vd, Vd_es
#finally, d-d:
script+= cutoffs_dd(dd_es, rcut_dd)

script+= footer()

# path = r'C:\Users\cfaccini\OneDrive - Indiana University\IU\Vikram\vlp_project'
# path = os.path.join(path,str(Qv),str(sigmahc), str(c))

# path = Path(path)

# if not os.path.isdir(path):
#     path.mkdir(parents=True)



