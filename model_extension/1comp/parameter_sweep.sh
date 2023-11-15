#!/bin/bash

# EEE2 concentrations:  0.60 0.57 0.55 0.53 0.50 0.40 0.20 0.10 0.04 0.01
# E2 concentrations:    0.30 0.28 0.25 0.22 0.20 0.18 0.15 0.10 0.04 0.01 
# Q2 concentrations:    0.20 0.16 0.15 0.14 0.12 0.10 0.08 0.06 0.04 0.01
# K2 concentrations:    0.20 0.15 0.12 0.10 0.08 0.07 0.06 0.05 0.04 0.01

for USERVLP in "EEE2" "E2"
do
if [ "$USERVLP" = "EEE2" ]; then
  echo "its EEE2!"
  USERVLPCHARGE="-2085"
  USERSIGMAHCRAW="5.15"
  for USERSALTCONC in 0.6 0.55 
  do
  if [ "$USERSALTCONC" = 0.6 ]; then
    echo $USERSALTCONC
    USERVLPEScutoff="1.0563629291500578"
    USERVLPLinkerEScutoff="0.6045365500835798"
    USERLinkerEScutoff="0.16092519609103764"
  elif [ "$USERSALTCONC" = 0.55 ]; then
    USERVLPEScutoff="1.053505529124341"
    USERVLPLinkerEScutoff="0.607036775106082"
    USERLinkerEScutoff="0.1632468336119326"
  fi  
  dir="$USERVLP"_c"$USERSALTCONC"
  cp -a template/ $dir
  cd $dir
    sed -i 's/USERVLPCHARGE/'$USERVLPCHARGE'/g' in.lammps.template
    sed -i 's/USERSIGMAHCRAW/'$USERSIGMAHCRAW'/g' in.lammps.template
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' in.lammps.template
    sed -i 's/USERVLPEScutoff/'$USERVLPEScutoff'/g' in.lammps.template
    sed -i 's/USERLinkerEScutoff/'$USERLinkerEScutoff'/g' in.lammps.template
    sed -i 's/USERVLPLinkerEScutoff/'$USERVLPLinkerEScutoff'/g' in.lammps.template
    sed -i 's/USERVLP/'$USERVLP'/g' assembly.pbs
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' assembly.pbs
    # sbatch assemby.pbs
    cd ..
  done
elif [ "$USERVLP" = "E2" ]; then
  USERVLPCHARGE="-1500"
  USERSIGMAHCRAW="4.75"
  for USERSALTCONC in 0.3 0.25
  do
  if [ "$USERSALTCONC" = 0.3 ]; then
    USERVLPEScutoff="1.0820795293815095"
    USERVLPLinkerEScutoff="0.6290030378037803"
    USERLinkerEScutoff="0.18271287128712868"
  elif [ "$USERSALTCONC" = 0.25 ]; then
    USERVLPEScutoff="1.0917232544683038"
    USERVLPLinkerEScutoff="0.6372180628777162"
    USERLinkerEScutoff="0.19003495885302812"
  fi 
  dir="$USERVLP"_c"$USERSALTCONC"
  cp -a template/ $dir
  cd $dir
    sed -i 's/USERVLPCHARGE/'$USERVLPCHARGE'/g' in.lammps.template
    sed -i 's/USERSIGMAHCRAW/'$USERSIGMAHCRAW'/g' in.lammps.template
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' in.lammps.template
    sed -i 's/USERVLPEScutoff/'$USERVLPEScutoff'/g' in.lammps.template
    sed -i 's/USERLinkerEScutoff/'$USERLinkerEScutoff'/g' in.lammps.template
    sed -i 's/USERVLPLinkerEScutoff/'$USERVLPLinkerEScutoff'/g' in.lammps.template
    sed -i 's/USERVLP/'$USERVLP'/g' assembly.pbs
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' assembly.pbs
    # sbatch assemby.pbs
    cd ..
  done
fi
done
