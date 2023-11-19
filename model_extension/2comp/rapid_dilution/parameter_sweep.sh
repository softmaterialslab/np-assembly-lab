#!/bin/bash

# EEE2 concentrations:  0.6 0.57 0.55 0.53 0.5 0.4 0.2 0.1 0.04 0.01
# E2 concentrations:    0.3 0.28 0.25 0.22 0.2 0.18 0.15 0.1 0.04 0.01 
# Q2 concentrations:    0.2 0.16 0.15 0.14 0.12 0.1 0.08 0.06 0.04 0.01
# K2 concentrations:    0.2 0.15 0.12 0.1 0.08 0.07 0.06 0.05 0.04 0.01

for USERVLP in "E2" #"EEE2" "E2"
do
if [ "$USERVLP" = "EEE2" ]; then
  echo "its EEE2!"
  USERVLPCHARGE="-2085"
  USERSIGMAHCRAW="5.15"
  for USERSALTCONC in 0.6 0.57 0.55 0.53 0.5 0.4 0.2 0.1 0.04 0.01 
  do        
    if [ "$USERSALTCONC" = 0.6 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.053505529124341"
        USERVLPLinkerEScutoff="0.6045365500835798"
        USERLinkerEScutoff="0.16092519609103764" 
    elif [ "$USERSALTCONC" = 0.57 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0551128166388066"
        USERVLPLinkerEScutoff="0.6059652500964381"
        USERLinkerEScutoff="0.1621753086022888"     
    elif [ "$USERSALTCONC" = 0.56 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.055827166645236"
        USERVLPLinkerEScutoff="0.6065010126012601"
        USERLinkerEScutoff="0.1627110711071107"     
    elif [ "$USERSALTCONC" = 0.55 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0563629291500578"
        USERVLPLinkerEScutoff="0.607036775106082"
        USERLinkerEScutoff="0.1632468336119326"     
    elif [ "$USERSALTCONC" = 0.53 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0577916291629161"
        USERVLPLinkerEScutoff="0.6081083001157258"
        USERLinkerEScutoff="0.1641397711199691" 
    elif [ "$USERSALTCONC" = 0.52 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0585059791693454"
        USERVLPLinkerEScutoff="0.6086440626205477"
        USERLinkerEScutoff="0.164675533624791"    
    elif [ "$USERSALTCONC" = 0.5 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0599346791822037"
        USERVLPLinkerEScutoff="0.6098941751317988"
        USERLinkerEScutoff="0.16574705863443487"     
    elif [ "$USERSALTCONC" = 0.4 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0686854667609618"
        USERVLPLinkerEScutoff="0.6175734377009129"
        USERLinkerEScutoff="0.17253338369551238"     
    elif [ "$USERSALTCONC" = 0.2 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1049387295872444"
        USERVLPLinkerEScutoff="0.6484690754789764"
        USERLinkerEScutoff="0.1998572714414298"     
    elif [ "$USERSALTCONC" = 0.1 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1592293300758647"
        USERVLPLinkerEScutoff="0.694723238395268"
        USERLinkerEScutoff="0.23968228429985852"     
    elif [ "$USERSALTCONC" = 0.04 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.2729895685997172"
        USERVLPLinkerEScutoff="0.7904461392567826"
        USERLinkerEScutoff="0.3196894850199306"     
    elif [ "$USERSALTCONC" = 0.01 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.6031978590716214"
        USERVLPLinkerEScutoff="1.0627920792079206"
        USERLinkerEScutoff="0.5372090619776263"     
    fi  
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
  for USERSALTCONC in 0.3 #0.24 # 0.3 0.28 0.25 0.22 0.2 0.18 0.15 0.1 0.04 0.01 
  do
        
    if [ "$USERSALTCONC" = 0.3 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0820795293815095"
        USERVLPLinkerEScutoff="0.6290030378037803"
        USERLinkerEScutoff="0.18271287128712868" 
    elif [ "$USERSALTCONC" = 0.28 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0856512794136555"
        USERVLPLinkerEScutoff="0.6318604378294971"
        USERLinkerEScutoff="0.18539168381123824"     
    elif [ "$USERSALTCONC" = 0.25 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0917232544683038"
        USERVLPLinkerEScutoff="0.6372180628777162"
        USERLinkerEScutoff="0.19003495885302812"     
    elif [ "$USERSALTCONC" = 0.24 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0940448919891987"
        USERVLPLinkerEScutoff="0.6391825253953966"
        USERLinkerEScutoff="0.19164224636749386" 
    elif [ "$USERSALTCONC" = 0.23 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.096545117011701"
        USERVLPLinkerEScutoff="0.6413255754146843"
        USERLinkerEScutoff="0.19360670888517423"     
    elif [ "$USERSALTCONC" = 0.22 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0990453420342032"
        USERVLPLinkerEScutoff="0.6434686254339719"
        USERLinkerEScutoff="0.19557117140285454"     
    elif [ "$USERSALTCONC" = 0.2 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1049387295872444"
        USERVLPLinkerEScutoff="0.6484690754789764"
        USERLinkerEScutoff="0.1998572714414298"     
    elif [ "$USERSALTCONC" = 0.18 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.111903642149929"
        USERVLPLinkerEScutoff="0.6543624630320174"
        USERLinkerEScutoff="0.20503630898804162"     
    elif [ "$USERSALTCONC" = 0.15 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1249405297672623"
        USERVLPLinkerEScutoff="0.6656134756332774"
        USERLinkerEScutoff="0.21468003407483605"     
    elif [ "$USERSALTCONC" = 0.1 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1592293300758647"
        USERVLPLinkerEScutoff="0.694723238395268"
        USERLinkerEScutoff="0.23968228429985852"     
    elif [ "$USERSALTCONC" = 0.04 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.2729895685997172"
        USERVLPLinkerEScutoff="0.7904461392567826"
        USERLinkerEScutoff="0.3196894850199306"     
    elif [ "$USERSALTCONC" = 0.01 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.6031978590716214"
        USERVLPLinkerEScutoff="1.0627920792079206"
        USERLinkerEScutoff="0.5372090619776263"     
    fi      
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
  for USERSALTCONC in 0.2 0.16 0.15 0.14 0.12 0.1 0.08 0.06 0.04 0.01
  do
    if [ "$USERSALTCONC" = 0.2 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1049387295872444"
        USERVLPLinkerEScutoff="0.6484690754789764"
        USERLinkerEScutoff="0.1998572714414298" 
    elif [ "$USERSALTCONC" = 0.17 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1158325671852898"
        USERVLPLinkerEScutoff="0.6577556255625562"
        USERLinkerEScutoff="0.2078937090137585"     
    elif [ "$USERSALTCONC" = 0.16 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.120118667223865"
        USERVLPLinkerEScutoff="0.6615059630963095"
        USERLinkerEScutoff="0.21110828404268994"     
    elif [ "$USERSALTCONC" = 0.15 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1249405297672623"
        USERVLPLinkerEScutoff="0.6656134756332774"
        USERLinkerEScutoff="0.21468003407483605"     
    elif [ "$USERSALTCONC" = 0.14 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1302981548154813"
        USERVLPLinkerEScutoff="0.67007816317346"
        USERLinkerEScutoff="0.2184303716085894"     
    elif [ "$USERSALTCONC" = 0.12 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1427992799279927"
        USERVLPLinkerEScutoff="0.6807934132698984"
        USERLinkerEScutoff="0.2277169216921692"     
    elif [ "$USERSALTCONC" = 0.1 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1592293300758647"
        USERVLPLinkerEScutoff="0.694723238395268"
        USERLinkerEScutoff="0.23968228429985852"     
    elif [ "$USERSALTCONC" = 0.06 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.2153058055805581"
        USERVLPLinkerEScutoff="0.7420489263212035"
        USERLinkerEScutoff="0.2796858846598945"     
    elif [ "$USERSALTCONC" = 0.04 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.2729895685997172"
        USERVLPLinkerEScutoff="0.7904461392567826"
        USERLinkerEScutoff="0.3196894850199306"     
    elif [ "$USERSALTCONC" = 0.01 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.6031978590716214"
        USERVLPLinkerEScutoff="1.0627920792079206"
        USERLinkerEScutoff="0.5372090619776263"     
    fi      
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
  for USERSALTCONC in 0.2 0.15 0.12 0.1 0.08 0.07 0.06 0.05 0.04 0.01
  do
    if [ "$USERSALTCONC" = 0.2 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1049387295872444"
        USERVLPLinkerEScutoff="0.6484690754789764"
        USERLinkerEScutoff="0.1998572714414298" 
    elif [ "$USERSALTCONC" = 0.15 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1249405297672623"
        USERVLPLinkerEScutoff="0.6656134756332774"
        USERLinkerEScutoff="0.21468003407483605"     
    elif [ "$USERSALTCONC" = 0.12 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1427992799279927"
        USERVLPLinkerEScutoff="0.6807934132698984"
        USERLinkerEScutoff="0.2277169216921692"     
    elif [ "$USERSALTCONC" = 0.1 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1592293300758647"
        USERVLPLinkerEScutoff="0.694723238395268"
        USERLinkerEScutoff="0.23968228429985852"     
    elif [ "$USERSALTCONC" = 0.08 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.181731355278385"
        USERVLPLinkerEScutoff="0.7138321010672495"
        USERLinkerEScutoff="0.2557551594445159"     
    elif [ "$USERSALTCONC" = 0.75 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.046540616561656"
        USERVLPLinkerEScutoff="0.5984645750289314"
        USERLinkerEScutoff="0.15556757104281854"     
    elif [ "$USERSALTCONC" = 0.07 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1967327054133985"
        USERVLPLinkerEScutoff="0.7263332261797607"
        USERLinkerEScutoff="0.2664704095409541"     
    elif [ "$USERSALTCONC" = 0.06 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.2153058055805581"
        USERVLPLinkerEScutoff="0.7420489263212035"
        USERLinkerEScutoff="0.2796858846598945"     
    elif [ "$USERSALTCONC" = 0.05 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.2397722933007587"
        USERVLPLinkerEScutoff="0.7625864890060434"
        USERLinkerEScutoff="0.2966516973125884"     
    elif [ "$USERSALTCONC" = 0.04 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.2729895685997172"
        USERVLPLinkerEScutoff="0.7904461392567826"
        USERLinkerEScutoff="0.3196894850199306"     
    elif [ "$USERSALTCONC" = 0.01 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.6031978590716214"
        USERVLPLinkerEScutoff="1.0627920792079206"
        USERLinkerEScutoff="0.5372090619776263"     
    fi    
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
