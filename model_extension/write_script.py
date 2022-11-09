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

#=====================================================

Qv = input('input VLP charge in e: ')
Qv = float(Qv)
qd = input('input dendrimer charge in e (default is 45): ')
qd = float(qd)

D = 56 # in nm. NP diameter
dd = 6.7 # in nm. dendrimer diameter
lb = 0.714 # bjerrum lenth in water, room temp.

c = input('input salt concentration in Molars: ')
c = float(c)
kappa = np.sqrt(8 * np.pi * lb * 0.6022*c)

#calculate values in LJ units for LAMMPS:
NPcharge = (Qv * (np.exp((1.64399 * D) * np.sqrt(c)) / (1 + ((1.64399 * D) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)
dendcharge = (qd * (np.exp((1.64399 * dd) * np.sqrt(c)) / (1 + ((1.64399 * dd) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)
userInputSalt = D * np.sqrt(8*np.pi*lb*0.6022*c)     #in reduced units

sigmahc = input('input sigma_hc value in nm (default is 4.5): ')
sigmahc = float(sigmahc)

sigmahc_ru = sigmahc/D  #sigma_hc in reduced units

rmaxlj = sigmahc*(2**(1/6))  #lj cutoff without delta
rmax_ru = rmaxlj/D

#=====================================================

def yukawa(r, q1, q2, kappa, d1, d2):
    lb = 0.714 #Bjerrum length, in nm
    aux1 = (q1/(1+kappa*(d1/2)))*np.exp(kappa*(d1/2))
    aux2 = (q2/(1+kappa*(d2/2)))*np.exp(kappa*(d2/2))
    ue = (1/r)*aux1*aux2*lb*np.exp(-kappa*r)
    
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

r = np.linspace(0.001, 100, 10000)  #r is in nanometers

#calculate Yukawa potentials:
ue11 = yukawa(r, Qv, Qv, kappa, D, D)
ue12 = yukawa(r, Qv, qd, kappa, D, dd)
ue22 = yukawa(r, qd, qd, kappa, dd, dd)

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


#calculate (modified) lj potentials:
    
ulj11, rcut11, uljcut11 = lj(r, sigmahc, D, D)
ulj12, rcut12, uljcut12 = lj(r, sigmahc, D, dd)
ulj22, rcut22, uljcut22 = lj(r, sigmahc, dd, dd)

delta11 = D - sigmahc
delta_VV = delta11/D
delta12 = (D + dd)/2 - sigmahc
delta_Vd = delta12/D
delta22 = dd - sigmahc
delta_dd = delta22/D

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
read_data	initCoords_100x.assembly

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
'''
    return s

def cutoffs1(ljcut, salt, es_global):
    s = f'''
## Ascribing interparticle potentials: ##
pair_style	hybrid/overlay	lj/expand	{ljcut}	coul/debye	{salt}	{es_global}	# LJ_cut without delta, kappa, Global ES_cut
    '''
    return s

def cutoffs2(sigmahc, delta_VV, VV_es, delta_Vd, Vd_es, delta_dd, dd_es):
    s = f'''
pair_coeff	1	1	lj/expand	1	{sigmahc}	{delta_VV}	# epsilon, sigma_hc, delta_V-V
pair_coeff	1	1	coul/debye	{VV_es}	# V-V ES_cut
pair_coeff	1	2	lj/expand	1	{sigmahc}	{delta_Vd}	# epsilon, sigma_hc, delta_V-D
pair_coeff	1	2	coul/debye	{Vd_es}	# V-D ES_cut
pair_coeff	2	2	lj/expand	1	{sigmahc}	{delta_dd}	# epsilon, sigma_hc, delta_D-D
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
compute	myVirusT	virus	temp
compute	myDendT 	dend	temp
compute	virusPotVec	virus	pe/atom
compute virusKeVec 	virus	ke/atom
compute dendPotVec	dend	pe/atom
compute dendKeVec	dend	ke/atom
compute	VirusPEperatom	virus	reduce	ave c_virusPotVec
compute	VirusKEperatom	virus	reduce	ave c_virusKeVec
compute	DendPEperatom	dend	reduce	ave c_dendPotVec
compute	DendKEperatom	dend	reduce	ave c_dendKeVec



#print "OUTPUT COLUMNS: SIMULATION STEP NUMBER | TEMPERATURE | NP POTENTIAL ENERGY | SYSTEM VOLUME"

#thermo_style	custom	step	temp	c_myVirusT	c_myDendT	c_myVirusPot	c_myDendPot	etotal	ke	pe	vol	#press
#thermo_style	custom	step	temp	c_NanoparticlePE	vol	#press
#thermo	10000

#restart	500000	outfiles/assemblyRestart.*	# creates 5 restart files up to equilibration; can comment this
#run	1500000    #run for 2.5 million without dumping anything

## Defining Output Information ##
dump	posD	virus	custom	${myDStep}	outfiles/dump.melt	id	type	x	y	z	# c_atomPot	c_atomKin
#dump   	myimages virus image 100000 outfiles/image.*.jpg type type &
#               	axes yes 0.8 0.02 view 60 -30
#dump_modify    	myimages pad 3

#thermo_style	custom	step	temp	c_myVirusT	c_myDendT	c_myVirusPot	c_myDendPot	etotal	ke	pe	vol	#press
thermo_style	custom	step	c_VirusKEperatom	c_DendKEperatom	c_VirusPEperatom	c_DendPEperatom	etotal	#press
thermo_modify norm no
thermo	1000

#restart	500000	outfiles/assemblyRestart.*	# creates 5 restart files post equilibration; keep this
run	5000000

unfix	ens
undump	posD
#undump	vOnlyD
uncompute	myVirusT
uncompute	myDendT
uncompute	virusPotVec
uncompute	virusKeVec
uncompute	dendPotVec
uncompute	dendKeVec
uncompute	VirusKEperatom
uncompute	DendKEperatom
uncompute	VirusPEperatom
uncompute	DendPEperatom
#shell		echo "Lammps Simulation Ended"
#shell		./postprocessor -n USERINPUT_LIGAND_NUMBER -N USERINPUT_DATASETCOUNT
    '''
    return s

script = header()
script+=datafile('filename')            #datafile with initial coordinates
script+= virus_charge(NPcharge)         #VLP charge (in reduced units)
script+= dend_charge(dendcharge)        #dendrimer charge (in reduced units)
script+= cutoffs1(rmax_ru, userInputSalt, VV_es)  #ljcut without delta (in reduced units), userinputKAPPA (in reduced units), ES_global_cutoff (in reduced units)
script+= cutoffs2(sigmahc_ru, delta_VV, VV_es, delta_Vd, Vd_es, delta_dd, dd_es)    #sigmahc (in reduced units), delta_VV, VV_es, delta_Vd, Vd_es, delta_dd, dd_es 
script+= footer()

# path = r'C:\Users\cfaccini\OneDrive - Indiana University\IU\Vikram\vlp_project'
# path = os.path.join(path,str(Qv),str(sigmahc), str(c))

# path = Path(path)

# if not os.path.isdir(path):
#     path.mkdir(parents=True)
