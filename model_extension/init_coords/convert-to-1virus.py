# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 18:38:52 2023

@author: camil
"""
from os.path import join
import pandas as pd
from numpy import where
import re

def while_replace(string):
	while '  ' in string:
		string = string.replace('  ', ' ')
	return string

folders_to_do = ["2-comp_cv37nM", "2-comp-cv370nM"]

fname_to_read = "initCoords.assembly"

header_lines = 9

for folder in folders_to_do:
	
	file_to_read = join(folder, fname_to_read)
	
	dat = pd.read_csv(file_to_read, skiprows=header_lines, header=None, 
		   sep=" ", dtype=str)
#	new_type = where(dat[1]==2, 1, dat[1])
	new_type = where(dat[1]=="2", "1", where(dat[1]=="3", "2", dat[1]))
	
	new_dat = dat.copy()
	
	new_dat[1] = new_type
	
	string_dat = new_dat.to_string(header=False, index=False, 
				index_names=False, justify="left")
	string_dat = while_replace(string_dat)
	
	old_header = ""
	with open(file_to_read, 'r') as fin:
		for i, line in enumerate(fin.readlines()):
			old_header += line
			if i == header_lines-1:
				break
	new_header = old_header.replace("3 atom types", "2 atom types")
	
	file_to_write = join(folder, "initCoords1comp.assembly")
	
	with open(file_to_write, "w+") as fout:
		fout.write(new_header + string_dat)
	
	
	

