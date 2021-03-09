#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  dataAnalysis.py
#
#  Copyright 2020 Luiz Oliveira <luiz@luizLinux>
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

This script analyses the output of preProcessing.py
The analysis steps are performed by the modules in the bin folder
"""

import sys
import os
import shutil
import time
start_time = time.time()

# Check for necessary directories
if not os.path.exists('treatment'):
    os.makedirs('treatment')
    print("The directory treatment/ was created, please populate with the "
          "desired csv files to be analysed.")
    sys.exit('The directory treatment/ did not exist.')
elif not os.listdir('treatment'):
    sys.exit('The directory treatment/ is empty.')

# Clear the previous results directories
if os.path.exists('treatment/results'):
    shutil.rmtree('treatment/results')
os.makedirs('treatment/results')
os.makedirs('treatment/results/Plots')
os.makedirs('treatment/results/SelectPlots')
os.makedirs('treatment/results/CSV')

# Define Global Variables
H = 0.10
U = 0.101
W = 0.15
L = 0.25
Y0 = 0.30
X0 = 0.25
RHO = 1e-6

# Import CSV
exec(open("bin/multipleSimulationImport.py").read())
print("""Importing Done...
Elapsed Time %.3f s\n""" %(time.time() - start_time))

# Process Data
exec(open("bin/multipleSimulationProcess.py").read())
print("""Processing Done...
Elapsed Time %.3f s\n""" %(time.time() - start_time))

# Data plot
exec(open("bin/multipleSimulationPlot.py").read())
print("""Plotting Done...
Elapsed Time %.3f s\n""" %(time.time() - start_time))

print("""All Done...
Execution Time %.3f seconds""" %(time.time() - start_time))
del start_time
