#!/bin/bash

# EEE2+E2+Q2+K2 concentrations:  0.6 0.55 0.5 0.4 0.35 0.325 0.3 0.27 0.245 0.2 0.18 0.16 0.125 0.1 0.04

# check the cutoff values below
# double check everything

for FOURCOMP in "EEE2E2Q2K2" 
do
if [ "$FOURCOMP" = "EEE2E2Q2K2" ]; then
  echo "its EEE2 and E2 and Q2 and K2!"
  USERVLP1="EEE2"
  USERVLP2="E2"
  USERVLP3="Q2"
  USERVLP4="K2"
  USERVLP1CHARGE="-2122"
  USERSIGMAHC1RAW="5.16"
  USERVLP2CHARGE="-1500"
  USERSIGMAHC2RAW="5.16"
  USERVLP3CHARGE="-1165"
  USERSIGMAHC3RAW="4"
  USERVLP4CHARGE="-622"
  USERSIGMAHC4RAW="4"
  for USERSALTCONC in 0.6 #0.55 0.5 0.4 0.35 0.325 0.3 0.27 0.245 0.2 0.18 0.16 0.125 0.1 0.04
  do      
    if [ "$USERSALTCONC" = 0.6 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0536841166259483"
        USERVLPLinkerEScutoff="0.6045365500835798"
        USERLinkerEScutoff="0.16092519609103764" 
    elif [ "$USERSALTCONC" = 0.57 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0554699916420212"
        USERVLPLinkerEScutoff="0.6061438375980455"
        USERLinkerEScutoff="0.1621753086022888"     
    elif [ "$USERSALTCONC" = 0.55 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0567201041532723"
        USERVLPLinkerEScutoff="0.6072153626076892"
        USERLinkerEScutoff="0.1632468336119326"     
    elif [ "$USERSALTCONC" = 0.54 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0572558666580942"
        USERVLPLinkerEScutoff="0.6077511251125112"
        USERLinkerEScutoff="0.1636040086151472"     
    elif [ "$USERSALTCONC" = 0.5 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0601132666838111"
        USERVLPLinkerEScutoff="0.6100727626334062"
        USERLinkerEScutoff="0.16574705863443487"     
    elif [ "$USERSALTCONC" = 0.4 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0690426417641763"
        USERVLPLinkerEScutoff="0.6177520252025201"
        USERLinkerEScutoff="0.17253338369551238"     
    elif [ "$USERSALTCONC" = 0.35 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0749360293172174"
        USERVLPLinkerEScutoff="0.6227524752475248"
        USERLinkerEScutoff="0.1771766587373023"     
    elif [ "$USERSALTCONC" = 0.325 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0785077793493634"
        USERVLPLinkerEScutoff="0.6257884627748488"
        USERLinkerEScutoff="0.17967688375980453"     
    elif [ "$USERSALTCONC" = 0.31 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0808294168702584"
        USERVLPLinkerEScutoff="0.6277529252925291"
        USERLinkerEScutoff="0.18146275877587756"     
    elif [ "$USERSALTCONC" = 0.3 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.082436704384724"
        USERVLPLinkerEScutoff="0.6291816253053877"
        USERLinkerEScutoff="0.18271287128712868"     
    elif [ "$USERSALTCONC" = 0.27 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0877943294329433"
        USERVLPLinkerEScutoff="0.6338249003471775"
        USERLinkerEScutoff="0.1868203838240967"     
    elif [ "$USERSALTCONC" = 0.245 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.0931519544811623"
        USERVLPLinkerEScutoff="0.6382895878873601"
        USERLinkerEScutoff="0.19074930885945737"     
    elif [ "$USERSALTCONC" = 0.2 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1054744920920663"
        USERVLPLinkerEScutoff="0.648826250482191"
        USERLinkerEScutoff="0.1998572714414298"     
    elif [ "$USERSALTCONC" = 0.18 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.112439404654751"
        USERVLPLinkerEScutoff="0.654719638035232"
        USERLinkerEScutoff="0.20503630898804162"     
    elif [ "$USERSALTCONC" = 0.16 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1206544297286871"
        USERVLPLinkerEScutoff="0.6616845505979169"
        USERLinkerEScutoff="0.21110828404268994"     
    elif [ "$USERSALTCONC" = 0.125 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1399418799022758"
        USERVLPLinkerEScutoff="0.6781146007457888"
        USERLinkerEScutoff="0.22521669666966695"     
    elif [ "$USERSALTCONC" = 0.1 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.1597650925806866"
        USERVLPLinkerEScutoff="0.6949018258968753"
        USERLinkerEScutoff="0.23968228429985852"     
    elif [ "$USERSALTCONC" = 0.04 ]; then
        echo $USERSALTCONC
        USERVLPEScutoff="1.2738825061077537"
        USERVLPLinkerEScutoff="0.7909819017616047"
        USERLinkerEScutoff="0.3196894850199306"     
    fi        
  dir="$USERVLP1"_"$USERVLP2"_"$USERVLP3"_"$USERVLP4"_c"$USERSALTCONC"
  cp -a template/ $dir
  cd $dir
    sed -i 's/USERVLP1CHARGE/'$USERVLP1CHARGE'/g' in.4comp.template
    sed -i 's/USERVLP2CHARGE/'$USERVLP2CHARGE'/g' in.4comp.template
    sed -i 's/USERVLP3CHARGE/'$USERVLP3CHARGE'/g' in.4comp.template
    sed -i 's/USERVLP4CHARGE/'$USERVLP4CHARGE'/g' in.4comp.template
    sed -i 's/USERSIGMAHC1RAW/'$USERSIGMAHC1RAW'/g' in.4comp.template
    sed -i 's/USERSIGMAHC2RAW/'$USERSIGMAHC2RAW'/g' in.4comp.template
    sed -i 's/USERSIGMAHC3RAW/'$USERSIGMAHC3RAW'/g' in.4comp.template
	sed -i 's/USERSIGMAHC4RAW/'$USERSIGMAHC4RAW'/g' in.4comp.template
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' in.4comp.template
    sed -i 's/USERVLPEScutoff/'$USERVLPEScutoff'/g' in.4comp.template
    sed -i 's/USERLinkerEScutoff/'$USERLinkerEScutoff'/g' in.4comp.template
    sed -i 's/USERVLPLinkerEScutoff/'$USERVLPLinkerEScutoff'/g' in.4comp.template
    sed -i 's/USERVLP1/'$USERVLP1'/g' assembly.pbs
    sed -i 's/USERVLP2/'$USERVLP2'/g' assembly.pbs
    sed -i 's/USERVLP3/'$USERVLP3'/g' assembly.pbs
    sed -i 's/USERVLP4/'$USERVLP4'/g' assembly.pbs
    sed -i 's/USERSALTCONC/'$USERSALTCONC'/g' assembly.pbs
    sbatch assembly.pbs
    cd ..
  done
fi
done
