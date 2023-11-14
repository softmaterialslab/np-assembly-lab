"""
Created on Mon Oct 24 13:51:15 2022
@author: cfaccini
writes lammps script for specific Qv, qd, sigmahc and c
"""
import numpy as np
import math
from matplotlib import pyplot as plt 

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

#=====================================================

#number of steps:
steps = 1e8

#charges in e:
Q1 = -1500     #charge of VLP1 usually the highest-charge
Q2 = -1080      #charge of VLP2
Q3 = -600        #charge of VLP3
qd = 45         #dendrimer charge
#note: due to the way the initial_coords file is written, particles 1,2 and 4 are VLPs, and 3 is dendrimer!

D = 56 # in nm. NP diameter
dd = 6.7 # in nm. dendrimer diameter
lb = 0.714 # bjerrum lenth in water, room temp.

c = 0.225 #in Molars


#sigmahc for the interaction between VLPs and dendrimers:
#standard values are: 
    #EEE2 = 5.1nm
    #E2 = 4.75nm
    #Q2 = 4.45nm
    #K2 = 4.15nm
    
sigmahc_V1 = 4.75
sigmahc_V2 = 4.45
sigmahc_V3 = 4.15    #attention! this is usually the smaller value!

#=====================================================
#=====================================================

sigmahc_V1_ru = sigmahc_V1/D  #sigma_hc in reduced units
sigmahc_V2_ru = sigmahc_V2/D  #sigma_hc in reduced units
sigmahc_V3_ru = sigmahc_V3/D  #sigma_hc in reduced units

rmaxljV1 = sigmahc_V1*(2**(1/6))  #lj cutoff without delta. I"m assuming sigmahc_V1 is the largest.
rmaxV1_ru = rmaxljV1/D

lb = 0.714 # bjerrum lenth in water, room temp.
kappa = np.sqrt(8 * np.pi * lb * 0.6022*c)

#calculate values in LJ units for LAMMPS:    
NPcharge1 = (Q1 * (np.exp((1.64399 * D) * np.sqrt(c)) / (1 + ((1.64399 * D) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)
NPcharge2 = (Q2 * (np.exp((1.64399 * D) * np.sqrt(c)) / (1 + ((1.64399 * D) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)
NPcharge3 = (Q3 * (np.exp((1.64399 * D) * np.sqrt(c)) / (1 + ((1.64399 * D) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)
dendcharge = (qd * (np.exp((1.64399 * dd) * np.sqrt(c)) / (1 + ((1.64399 * dd) * np.sqrt(c))))) * (1.6021 * 1e-19) / (1.6011 * 1e-19)

userInputSalt = D * np.sqrt(8*np.pi*lb*0.6022*c)     #in reduced units


#=====================================================

#calculate Yukawa potentials:
#VLP-VLP
ueV1 = yukawa(r, Q1, Q1, kappa, D, D)    
ueV2 = yukawa(r, Q2, Q2, kappa, D, D)
ueV3 = yukawa(r, Q3, Q3, kappa, D, D)

ueV12 = yukawa(r, Q1, Q2, kappa, D, D)
ueV13 = yukawa(r, Q1, Q3, kappa, D, D)
ueV23 = yukawa(r, Q2, Q3, kappa, D, D)

val11 = np.where(ueV1 <= 0.005)
index11 = val11[0]
re11 = r[index11[0]]

val22 = np.where(ueV2 <= 0.005)
index22 = val22[0]
re22 = r[index22[0]]

val33 = np.where(ueV3 <= 0.005)
index33 = val33[0]
re33 = r[index33[0]]    

val12 = np.where(ueV12 <= 0.005)
index12 = val12[0]
re12 = r[index12[0]]

val13 = np.where(ueV13 <= 0.005)
index13 = val13[0]
re13 = r[index13[0]]

val23 = np.where(ueV23 <= 0.005)
index23 = val23[0]
re23 = r[index23[0]]

#dend-VLP:
ue1d = yukawa(r, Q1, qd, kappa, D, dd)
ue2d = yukawa(r, Q2, qd, kappa, D, dd)
ue3d = yukawa(r, Q3, qd, kappa, D, dd)

val1d = np.where(np.absolute(ue1d) <= 0.005)
index1d = val1d[0]
re1d = r[index1d[0]]

val2d = np.where(np.absolute(ue2d) <= 0.005)
index2d = val2d[0]
re2d = r[index2d[0]]

val3d = np.where(np.absolute(ue3d) <= 0.005)
index3d = val3d[0]
re3d = r[index3d[0]]

#dend-dend
uedd = yukawa(r, qd, qd, kappa, dd, dd)

valdd = np.where(np.absolute(uedd) <= 0.005)
indexdd = valdd[0]
redd = r[indexdd[0]]

#cutoffs:
VV11_es = re11/D    #ES V1-V1 cutoff in reduced units
VV22_es = re22/D    #ES V2-V2 cutoff in reduced units
VV33_es = re33/D    #ES V3-V3 cutoff in reduced units
VV12_es = re12/D    #ES V1-V2 cutoff in reduced units
VV13_es = re13/D    #ES V1-V3 cutoff in reduced units
VV23_es = re23/D    #ES V2-V3 cutoff in reduced units    

Vd_es = re1d/D
dd_es = redd/D

#=====================================================
#calculate lj potentials:
    
#VLP-VLP: unmod lj potential   
ulj11, rcut11, uljcut11 = lj2(r, D, D)
ulj22, rcut22, uljcut22 = lj2(r, D, D)
ulj33, rcut33, uljcut33 = lj2(r, D, D)

ulj12, rcut12, uljcut12 = lj2(r, D, D)
ulj13, rcut13, uljcut13 = lj2(r, D, D)
ulj23, rcut23, uljcut23 = lj2(r, D, D)

delta11 = 0
delta_VV = delta11/D

#VLP-dend: mod lj potentials
ulj1d, rcut1d, uljcut1d = lj1(r, sigmahc_V1, D, dd)
ulj2d, rcut2d, uljcut2d = lj1(r, sigmahc_V2, D, dd)
ulj3d, rcut3d, uljcut3d = lj1(r, sigmahc_V3, D, dd)

delta_V1 = (D + dd)/2 - sigmahc_V1
delta_V2 = (D + dd)/2 - sigmahc_V2
delta_V3 = (D + dd)/2 - sigmahc_V3

delta_Vd1 = delta_V1/D
delta_Vd2 = delta_V2/D
delta_Vd3 = delta_V3/D

#dend-dend: unmod lj potential:
uljdd, rcutdd, uljcutdd = lj2(r, dd, dd)    
deltadd = 0
delta_dd = deltadd/D


#=====================================================
#this block is for plotting the net potentials only:
#calculate net potentials:
unet1d = ue1d + ulj1d
unet2d = ue2d + ulj2d
unet3d = ue3d + ulj3d

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
plt.plot(r, unet1d, label = 'E2, $\sigma_{hc}$=%f' %sigmahc_V1)
plt.plot(r, unet2d, label = 'Q2, $\sigma_{hc}$=%f' %sigmahc_V2)
plt.plot(r, unet3d, label = 'K2, $\sigma_{hc}$=%f' %sigmahc_V3)

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

def datafile():
    s ='''
## Create Simulation Box, Atoms ##
read_data	initCoords.assembly
#read_restart	assemblyRestart.10000000

## Group Atoms by Type ##
group virus1    type   1
group virus2    type   2
group virus3    type   4
group dend      type   3
group allViruses union virus1 virus2   virus3

## Defining Particle/Medium Properties ##
mass   1   1
mass   2   1
mass   4   1
mass   3   0.0029024	# relative mass of dendrimer to P22
dielectric	78.54

## Ascribing Initial Velocities ##
velocity	all	create	1.	4928459	rot	yes	dist	gaussian	units	box	# 1-kB*T,random seed,zero net ang.mom.,gauss from MB stats
 '''
    return s

def charge(c, npcharge1, npcharge2, npcharge3, dendcharge):
    s = f'''    
## Defining charges for {c}M ## 
set    type   1    charge  {npcharge1}     # qV1_DLVO (in LJ units)   
set    type   2    charge  {npcharge2}     # qV2_DLVO (in LJ units) 
set    type   4    charge  {npcharge3}     # qV3_DLVO (in LJ units)
set    type   3    charge  {dendcharge}    # qD_DLVO (in LJ units) 

''' 
    return s

def cutoffs(ljcut, salt, VV11_es, VV22_es, VV33_es, VV12_es, VV13_es, VV23_es, sigmahc_V1, sigmahc_V2, sigmahc_V3, delta_Vd1, delta_Vd2, delta_Vd3, Vd_es, dd_es, steps):
    s = f'''
## Ascribing interparticle potentials: ##
pair_style	hybrid/overlay	lj/expand	{ljcut}	coul/debye	{salt}	{VV11_es}	# LJ_cut without delta, kappa, Global ES_cut
pair_coeff	1	1	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	1	1	coul/debye	{VV11_es}	# V1-V1 ES_cut
pair_coeff	2	2	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	2	2	coul/debye	{VV22_es}	# V2-V2 ES_cut
pair_coeff	1	2	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	1	2	coul/debye	{VV12_es}	# V1-V2 ES_cut
pair_coeff	1	3	lj/expand	1	{sigmahc_V1}	{delta_Vd1}	# epsilon, sigma_hc, delta_V1-D
pair_coeff	1	3	coul/debye	{Vd_es}	# V-D ES_cut
pair_coeff	2	3	lj/expand	1	{sigmahc_V2}	{delta_Vd2}	# epsilon, sigma_hc, delta_V2-D
pair_coeff	2	3	coul/debye	{Vd_es}	# V-D ES_cut
pair_coeff	3	3	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_D-D
pair_coeff	3	3	coul/debye	{dd_es}	# D-D ES_cut
pair_coeff	1	4	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	1	4	coul/debye	{VV13_es}	# V1-V3 ES_cut
pair_coeff	2	4	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	2	4	coul/debye	{VV23_es}	# V2-V3 ES_cut
pair_coeff	3	4	lj/expand	1	{sigmahc_V3}	{delta_Vd3}	# epsilon, sigma_hc, delta_V3-D
pair_coeff	3	4	coul/debye	{Vd_es}	# V-D ES_cut
pair_coeff	4	4	lj/expand	1	1.	0	# epsilon, sigma_hc, delta_V-V
pair_coeff	4	4	coul/debye	{VV33_es}	# V3-V3 ES_cut
pair_modify	shift	yes	# the additive e_LJ for repulsion-only


## Ensemble Fixes (+ for output) ##
variable	myTStep	equal	0.000025
timestep	0.000025
variable	myDStep	equal	1000000
fix	ens	all	nvt	temp	1.	1.	0.0025	# T_start, T_stop, T_damp=100*timestep

## Defining Output Information ##

dump	posD	all	custom	1000000	outfiles/dump.melt	id	type	x	y	z	# c_atomPot	c_atomKin
dump    allV    allViruses  custom  5000    outfiles/dump_allV.melt    id	type	x	y	z	# c_atomPot	c_atomKin 
dump	v1OnlyD	virus1	custom	10000	outfiles/dumpVirus1Only.melt	id	type	x	y	z	# c_atomPot	c_atomKin
dump	v2OnlyD	virus2	custom	10000	outfiles/dumpVirus2Only.melt	id	type	x	y	z	# c_atomPot	c_atomKin
dump	v3OnlyD	virus3	custom	10000	outfiles/dumpVirus3Only.melt	id	type	x	y	z	# c_atomPot	c_atomKin

thermo_style	custom	step etotal  pe  ke 
thermo_modify norm no
thermo	10000


restart		{int(steps/50)}	outfiles/assemblyRestart.*	# creates restart files throughout run
run		{steps}

undump posD
undump allV
undump v1OnlyD
undump v2OnlyD
undump v3OnlyD  
    '''
    return s


def footer():
    s = '''

    '''
    return s

# first write header:

script = header()
script+=datafile()            #datafile with initial coordinates

script+= charge(c, NPcharge1, NPcharge2, NPcharge3, dendcharge)         #VLP1 charge, VLP2 charge, VLP3 charge, dendrimer charge (in reduced units)
    
script+= cutoffs(rmaxV1_ru, userInputSalt, VV11_es, VV22_es, VV33_es, VV12_es, VV13_es, VV23_es, sigmahc_V1_ru, sigmahc_V2_ru, sigmahc_V3_ru, delta_Vd1, delta_Vd2, delta_Vd3, Vd_es, dd_es, int(steps) )
    
#cutoffs(ljcut, salt, VV11_es, VV22_es, VV33_es, VV12_es, VV13_es, VV23_es, sigmahc_V1, sigmahc_V2, sigmahc_V3, delta_Vd1, delta_Vd2, delta_Vd3, Vd_es, dd_es, steps):
# script+= footer()

