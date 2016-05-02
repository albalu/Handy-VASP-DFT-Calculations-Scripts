#!/usr/bin/env python

import numpy as np
import os

try:
	with open('EIGENVAL', 'r') as eigenval:
		counter = 0
		for line in eigenval:
			counter += 1
			if	
except IOError:
	raise IOError('EIGENVAL file must be present')
