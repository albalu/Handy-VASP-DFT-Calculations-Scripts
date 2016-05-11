#!/usr/bin/env python
# This code extracts the energy information from Quantum ESPRESSO output and converts it into VASP file format, EIGENVAL
# It also read the lattice matrix and volume information from the QE output file and converts it to VASP OUTCAR format
# The generated EIGENVAL and OUTCAR files are compatible with aMoBT
# Please contact alireza@wustl.edu if you had any questions. Bug reports are very much appreciated.
# By: Alireza Faghaninia

import os
import numpy as np
import re
import argparse

### Check the input arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f","--QE_file", help="The name of the Quantum ESPRESSO output file", required = True)
parser.add_argument("-e","--destination_energy", help="The energy file (i.e. EIGENVAL)", required = False, default='EIGENVAL')
parser.add_argument("-o","--destination_output", help="The output file (i.e. OUTCAR)", required = False, default='OUTCAR')
args = parser.parse_args()

### Check if EIGENVAL already exists
filename = args.destination_energy
if os.path.isfile('./'+filename):
	print('Warning an '+ filename + ' file already exists.'),
	answer = raw_input("Replace? ")
	if answer in ['y', 'Y', 'yes', 'Yes', 'YES', 'yeah', 'Yeah']:	
		os.system('rm '+filename)
	else:
		print('Program stopped!')
		exit(0)

### Check if OUTCAR already exists
filename = args.destination_output
if os.path.isfile('./'+filename):
	print('Warning an '+ filename + ' file already exists.'),
	answer = raw_input("Replace? ")
	if answer in ['y', 'Y', 'yes', 'Yes', 'YES', 'yeah', 'Yeah']:	
		os.system('rm '+filename)
	else:
		print('Program stopped!')
		exit(0)

### Read the Quantum ESPRESSO output file
prev = 0 
big = range(10000)
big = [str(i) for i in big]
kpoints_lst = []
energy_lst = []
k_counter = 0
with open(args.QE_file) as openfile:
	for li in openfile:
		if "unit-cell volume          =" in li:
			volume_au = re.findall("[-+]?\d+[\.]?\d*", li)
			volume = float(volume_au[0])*0.148188994		# The constant is a.u.^3 to A^3 conversion factor
		if "number of electrons       =" in li:
			elec_lst = re.findall("[-+]?\d+[\.]?\d*", li)
			nelec = float(elec_lst[0])
		if "celldm(1)" in li:
			a0 = float(re.findall("[-+]?\d+[\.]?\d*", li)[1])*0.52917721092
		if "a(1) = (" in li:
			a1 = re.findall("[-+]?\d+[\.]?\d*", li)[1:4]
		if "a(2) = (" in li:
			a2 = re.findall("[-+]?\d+[\.]?\d*", li)[1:4]
		if "a(3) = (" in li:
			a3 = re.findall("[-+]?\d+[\.]?\d*", li)[1:4]
		if "b(1) = (" in li:
			b1 = re.findall("[-+]?\d+[\.]?\d*", li)[1:4]
		if "b(2) = (" in li:
			b2 = re.findall("[-+]?\d+[\.]?\d*", li)[1:4]
		if "b(3) = (" in li:
			b3 = re.findall("[-+]?\d+[\.]?\d*", li)[1:4]
		if " k =" in li:
			k_counter += 1
			tmp_lst = re.findall("[-+]?\d+[\.]?\d*", li)
			kpoints_lst = kpoints_lst + tmp_lst[0:3]
			li = next(openfile)
			li = next(openfile) 
			while li.split() != []:
				temp = re.findall("[-+]?\d+[\.]?\d*", li)
				energy_lst = energy_lst + temp
				li = next(openfile)
			if k_counter == 1:
				nbands = len(energy_lst)

a1 = [float(i)*a0 for i in a1]
a2 = [float(i)*a0 for i in a2]
a3 = [float(i)*a0 for i in a3]
b1 = [float(i)/a0 for i in b1]
b2 = [float(i)/a0 for i in b2]
b3 = [float(i)/a0 for i in b3]

### Convert k-point list to a nkx3 float matrix
kpoints_lst = [float(i) for i in kpoints_lst]
kpoints = np.matrix(kpoints_lst)/2
kpoints.shape = (k_counter,3)

### Convert energy list to a nkxnbands float matrix
energy_lst = [float(i) for i in energy_lst]
energy = np.matrix(energy_lst)
energy.shape = (k_counter, nbands)

### Write the output in EIGENVAL format
with file(args.destination_energy, 'w') as endata:
	endata.write('    2    2    1    1\n  0.2376594E+02  0.4065993E-09  0.4065993E-09  0.4065993E-09  0.5000000E-15\n  1.000000000000000E-004\n  CAR\n unknown system\n')
	endata.write('%5d %5d %5d\n' % (nelec,k_counter,nbands))
	k_counter = 0
	for k in kpoints:
		endata.write('\n')
		np.savetxt(endata, np.c_[k, 1.0], fmt='%15.7E')
		for i in range(nbands):
			endata.write('%4d' % (i+1))
			endata.write('%16.6f\n' % energy[k_counter,i])
		k_counter += 1

### Write the output in OUTCAR format
with file(args.destination_output, 'w') as outdata:
	outdata.write('Converted Quantum ESPRESSO output to OUTCAR format suitable for aMoBT\n')
	outdata.write('%s%12.2f\n' % ('  volume of cell :', volume))
	outdata.write('      direct lattice vectors                 reciprocal lattice vectors\n')
	outdata.write('   %13.9f%13.9f%13.9f   %13.9f%13.9f%13.9f\n' % (a3[0], a3[1], a3[2], b3[0], b3[1], b3[2]))
	outdata.write('   %13.9f%13.9f%13.9f   %13.9f%13.9f%13.9f\n' % (a1[0], a1[1], a1[2], b1[0], b1[1], b1[2]))
	outdata.write('   %13.9f%13.9f%13.9f   %13.9f%13.9f%13.9f\n' % (a2[0], a2[1], a2[2], b2[0], b2[1], b2[2]))
