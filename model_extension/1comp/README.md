* 1-component files

*script_for_cutoff_sweep:
	
this python code will generate blocks of code for each VLP with the ES cutoff values for V-V, V-d, and d-d.
To use, enter the desired salt concentrations in molars for each VLP, run the script, then copy each generated block into the approproate locatin in the parameter_sweep.sh file.
remeber to also update the salt concentrations on the sweep file!

* updated DLVO charge calculation to include a *(1.000676522) factor: this performs the unit change from electron charge e to lj units.
Note: 1.000676522 = e charge / sqrt(4 pi epsilon_0 D epsilon) = 1.6021E-19 / 1.6011E-19
with 	D = 56 nm
	epsilon_0 = 8.854E-12 F/m
	epsilon = kBT = 4.1143E-21 m^2 kg / s^2