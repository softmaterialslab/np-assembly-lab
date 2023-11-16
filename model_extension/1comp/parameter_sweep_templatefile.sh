#!/bin/bash

# EEE2 concentrations:  0.6 0.57 0.55 0.53 0.5 0.4 0.2 0.1 0.04 0.01
# E2 concentrations:    0.3 0.28 0.25 0.22 0.2 0.18 0.15 0.1 0.04 0.01 
# Q2 concentrations:    0.2 0.16 0.15 0.14 0.12 0.1 0.08 0.06 0.04 0.01
# K2 concentrations:    0.2 0.15 0.12 0.1 0.08 0.07 0.06 0.05 0.04 0.01

for USERVLP in "EEE2" #"E2"
do
if [ "$USERVLP" = "EEE2" ]; then
  echo "its EEE2!"
  USERVLPCHARGE="-2085"
  USERSIGMAHCRAW="5.15"
  for USERSALTCONC in #add salt concs. 
  do        
  #copy EEE2 cutoffs here
 
  dir="$USERVLP"_c"$USERSALTCONC"
  cp -a template/ $dir
  cd $dir
    sed -i 's/USERVLPCHARGE/'$USERVLPCHARGE'/g' in.1comp.template
    sed -i 's/USERSIGMAHCRAW/'$USERSIGMAHCRAW'/g' in.1comp.template
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' in.1comp.template
    sed -i 's/USERVLPEScutoff/'$USERVLPEScutoff'/g' in.1comp.template
    sed -i 's/USERLinkerEScutoff/'$USERLinkerEScutoff'/g' in.1comp.template
    sed -i 's/USERVLPLinkerEScutoff/'$USERVLPLinkerEScutoff'/g' in.1comp.template
    sed -i 's/USERVLP/'$USERVLP'/g' assembly.pbs
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' assembly.pbs
    sbatch assembly.pbs
    cd ..
  done
elif [ "$USERVLP" = "E2" ]; then
  echo "its E2!"
  USERVLPCHARGE="-1500"
  USERSIGMAHCRAW="4.75"
  for USERSALTCONC in #add salt concs.
  do
  #copy E2 cutoffs here
    
  dir="$USERVLP"_c"$USERSALTCONC"
  cp -a template/ $dir
  cd $dir
    sed -i 's/USERVLPCHARGE/'$USERVLPCHARGE'/g' in.1comp.template
    sed -i 's/USERSIGMAHCRAW/'$USERSIGMAHCRAW'/g' in.1comp.template
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' in.1comp.template
    sed -i 's/USERVLPEScutoff/'$USERVLPEScutoff'/g' in.1comp.template
    sed -i 's/USERLinkerEScutoff/'$USERLinkerEScutoff'/g' in.1comp.template
    sed -i 's/USERVLPLinkerEScutoff/'$USERVLPLinkerEScutoff'/g' in.1comp.template
    sed -i 's/USERVLP/'$USERVLP'/g' assembly.pbs
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' assembly.pbs
    sbatch assembly.pbs
    cd ..
  done
elif [ "$USERVLP" = "Q2" ]; then
  USERVLPCHARGE="-1080"
  USERSIGMAHCRAW="4.45"
  for USERSALTCONC in #add salt concs.
  do
  # copy Q2 cutoffs here
    
  dir="$USERVLP"_c"$USERSALTCONC"
  cp -a template/ $dir
  cd $dir
    sed -i 's/USERVLPCHARGE/'$USERVLPCHARGE'/g' in.1comp.template
    sed -i 's/USERSIGMAHCRAW/'$USERSIGMAHCRAW'/g' in.1comp.template
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' in.1comp.template
    sed -i 's/USERVLPEScutoff/'$USERVLPEScutoff'/g' in.1comp.template
    sed -i 's/USERLinkerEScutoff/'$USERLinkerEScutoff'/g' in.1comp.template
    sed -i 's/USERVLPLinkerEScutoff/'$USERVLPLinkerEScutoff'/g' in.1comp.template
    sed -i 's/USERVLP/'$USERVLP'/g' assembly.pbs
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' assembly.pbs
    sbatch assembly.pbs
    cd ..
  done
elif [ "$USERVLP" = "K2" ]; then
  USERVLPCHARGE="-600"
  USERSIGMAHCRAW="4.15"
  for USERSALTCONC in #add salt concs.
  do
  #copy K2 cutoffs here	
 
  dir="$USERVLP"_c"$USERSALTCONC"
  cp -a template/ $dir
  cd $dir
    sed -i 's/USERVLPCHARGE/'$USERVLPCHARGE'/g' in.1comp.template
    sed -i 's/USERSIGMAHCRAW/'$USERSIGMAHCRAW'/g' in.1comp.template
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' in.1comp.template
    sed -i 's/USERVLPEScutoff/'$USERVLPEScutoff'/g' in.1comp.template
    sed -i 's/USERLinkerEScutoff/'$USERLinkerEScutoff'/g' in.1comp.template
    sed -i 's/USERVLPLinkerEScutoff/'$USERVLPLinkerEScutoff'/g' in.1comp.template
    sed -i 's/USERVLP/'$USERVLP'/g' assembly.pbs
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' assembly.pbs
    sbatch assembly.pbs
    cd ..
  done
fi
done