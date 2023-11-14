#!/bin/bash
for SALT in 300 500 550 600               ### enter salt values as desired for data postprocess, compute gr etc.
do
dir="c$SALT"
cd $dir		### enter the salt folder
cd outfiles/	### travel to where dump.melt is
tail -n 11700 dump.melt > last100frames.out	
### 11700 is the number of lines that will be cut from the end. these lines capture the last 100 frames of the simulation. we assume you ran to 10 million steps and frames are separated by 1000 steps. you can pick the line number Nf=1158418 corresponding to when TIMESTEP 9,901,000 is reached. you can also see the total number of lines N=1170117 in the dump.melt file. Then N-Nf+1 is 11700. You can get this also by noting that each frame in the movie file is 117 lines long. So last 100 frames are 11700 lines long, which is what we tail from the file. Change as needed depending on your simulation.
awk '/ITEM: TIMESTEP/{x="data"++i;}{print > x;}' last100frames.out
### this is the same awk file which now acts on the last 100 frames to create data1, data2, ..., data100 files used in computing gr.
cd ..	### get out of outfiles
cd ..	## get out of the salt folder
done
