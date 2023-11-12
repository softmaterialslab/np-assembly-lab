# model extension

* Important updates on 1-component, 2-component, 3-component, and 4-component systems. Each will have a folder containing: LAMMPS input script, initializing data file, jobscript (for hpc runs), cleanlog to create thermo.dat files, perf files to suggest how many cores are optimal, output files and expected sizes (based on selections of dump parameters)

## 1-comp

* 540 vlps, 100x = 54000 linkers

* thermo freq: 1000, dump vlp freq: 1000, dump all freq: 10000 produces 20 MB for vlp movie and 200 MB for all movie in a 1 mil run.

* todo 
- "fix", "dump" names
- charge values mismatch?
- warning on more than one ke/atom compute?
- run longer (> 1m) to see steady state in PE, rep snap
