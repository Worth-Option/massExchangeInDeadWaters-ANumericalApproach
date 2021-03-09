#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  preProcessing.py
#  
#  Copyright 2020 Luiz Oliveira
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

"""
Main module

This script analyses the output of simulations ran on OpenFoam
The analysis steps are performed by the modules in the bin folder
"""

import sys
import os
import shutil
import time
start_time = time.time()

# Check for necessary directories
if not os.path.exists('preTreatment'):
    os.makedirs('preTreatment')
    print("The directory preTreatment/ was created, please populate with the "
          "desired csv files to be analysed.")
    sys.exit('The directory preTreatment/ did not exist.')
elif not os.listdir('preTreatment'):
    sys.exit('The directory preTreatment/ is empty.')
    
# Clear the previous results directories
if os.path.exists('preTreatment/results'):
    shutil.rmtree('preTreatment/results')
os.makedirs('preTreatment/results')
os.makedirs('preTreatment/results/Excel')
os.makedirs('preTreatment/results/CSV')
os.makedirs('preTreatment/results/Plot')

# Define Global Variables
H = 0.10
U = 0.101
W = 0.15
L = 0.25
Y0 = 0.30
X0 = 0.25
RHO = 1e-6

# Import CSV
exec(open("bin/importCSV.py").read())
print("""Importing Done...
Elapsed Time %.3f s\n""" %(time.time() - start_time))

# Data Processing
try:
    exec(open("bin/dataProcess.py").read())
    print("""Processing Done...
Elapsed Time %.3f s\n""" %(time.time() - start_time))
except:
    print("""No data was processed.
The script jumped into the next section: Mass Fitting""")
    print("Elapsed Time %.3f s\n" %(time.time() - start_time))

# Mass Fitting
try: 
    exec(open("bin/mass.py").read())
    print("""Mass Fitting Done...
Elapsed Time %.3f s\n""" %(time.time() - start_time))
except:
    print("""No mass data was processed.
The script jumped into the next section: Mixing Layer Thickness""")
    print("Elapsed Time %.3f s\n" %(time.time() - start_time))
    
# Mixing Layer Thickness
try: 
    exec(open("bin/thickness.py").read())
    print("""Mixing Layer Thickness Calculated...
Elapsed Time %.3f s\n""" %(time.time() - start_time))
except:
    print("""No mixing layer thickness data was processed.
The script jumped into the next section: Plotting""")
    print("Elapsed Time %.3f s\n" %(time.time() - start_time))
    
# Plot Data
try:
    exec(open("bin/plot.py").read())
    print("""Plotting Done...
Elapsed Time %.3f s\n""" %(time.time() - start_time))
except:print("No plotting was done.\n")

print("""All Done...
Execution Time %.3f seconds""" %(time.time() - start_time))
del start_time
