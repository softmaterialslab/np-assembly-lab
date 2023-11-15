* 1-component files

The 'script_for_cutoffs_sweep.py' file generates the blocks with the "if c=x, cutoffs are...." statements, which must be pasted into the parameter_sweep file at the indicated locations for each VLP type.

Workflow is as follows:
1) identify the desired salt concentrations for each VLP type
2) run python code to generate the cutoff statements for the selected c values
3) update sweep file: hardcode selected c values and paste the blocs to the correct place in the sweep file.
4) run sweep!