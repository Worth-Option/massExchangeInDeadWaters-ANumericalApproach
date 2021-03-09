#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  importCSV.py
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
Data is imported from text files to be later processed and ploted
"""

# Libraries
import os
import re
import pandas as pd

# Import Literature
literatureExp = pd.read_csv('dataset/fig4/fig4a.csv', header = 1, usecols=(0,1))
literatureExp.columns = ['(y-y0)/H','u/U']
literatureExp = literatureExp.dropna()
literatureLES = pd.read_csv('dataset/fig4/fig4a.csv', header = 1, usecols=(2,3))
literatureLES.columns = ['(y-y0)/H','u/U']
massLiterature = pd.read_csv('dataset/mass/mass.csv', header = 1)
massLiterature.columns = ['Vegetation Density', 'Td']
massLiterature.Td = massLiterature.Td * U / H

# Tracer data
try:
    tracerData = pd.read_csv('preTreatment/tracerVolAve.dat',
                             delimiter='\t', header = 3)
    tracerData.columns = ['time', 'tracerVol']
    tracerData.tracerVol[0] = 1
    massTimeZero = tracerData.time[0]
    tracerData.time = tracerData.time - massTimeZero
except:pass

# Partial Tracer at Interface
try:
    interfaceTracer = dict()
    regions = ['Bottom', 'Middle', 'Top']
    for reg in regions:
        interfaceTracer[reg] = pd.read_csv('preTreatment/tracer'+reg+'.dat',\
                                            delimiter='\t', header = 4)
        interfaceTracer[reg].columns = ['time', 'tracer']
        interfaceTracer[reg].time = interfaceTracer[reg].time - massTimeZero
    Eraw = pd.read_csv('preTreatment/velocityInterface.dat', delimiter='\t',\
                    header = 4)
    Eraw.columns = ['time', 'absVelInt']
    Eraw.time = Eraw.time - massTimeZero
    Eraw.absVelInt = Eraw.absVelInt/(2*H*L)
except:pass

# Generic Planes
files = os.listdir('preTreatment')

# Check for csv files
rawFiles = list()
csvFiles = list()
datFiles = list()
uniqueRaw = list()
uniqueVar = list()

# Removes ':' from file name
for item in files:
    if ':' in item:    
        newname = item.split(':')[1]
        os.rename('preTreatment/'+item, 'preTreatment/'+newname)
        
files = os.listdir('preTreatment')

for item in files:
      if re.search('.\.raw', item):
          rawFiles.append(item)

for item in files:
      if re.search('.\.csv', item):
          csvFiles.append(item)
          
for item in files:
      if re.search('.\.dat', item):
          datFiles.append(item)

csvFiles.sort() 
datFiles.sort() 
rawFiles.sort()

for item in rawFiles:
    try:
        plane = re.findall("_([\d\D]..)", item)[0]
        variableName = re.split("_", item)[0]
        if plane not in uniqueRaw:
            uniqueRaw.append(plane)
        if variableName not in uniqueVar:
            uniqueVar.append(variableName)
    except:continue

def cleanHeader(name):
    fh = open('preTreatment/'+name, "rt")
    data = fh.read()
    # data = re.sub(r':\S+ ', r'', data)
    data = data.replace('# ', '')
    data = data.replace('  ', ' ') #removes double spacing
    
    fh.close()
    fh = open('preTreatment/'+name, "wt")
    fh.write(data)
    fh.close()

# Import generated data
for item in rawFiles:
    for item2 in uniqueRaw:
        try:
            plane = re.findall("_([\d\D]..)", item)[0]
            if plane == item2:
                cleanHeader(item)
                variableName = re.split("_", item)[0]
                aux = pd.read_csv('preTreatment/'+item, sep=" ", header=1,
                                  float_precision="high",skipinitialspace=True)
                #if aux.isnull().values.any():continue
                try:
                    if variableName not in locals():vars()[variableName] = aux
                    else:
                        vars()[variableName] = pd.concat([vars()[variableName],aux],
                                              ignore_index=True, axis=1)
                        vars()[variableName] = vars()[variableName].dropna(axis=0, how='all')
                        vars()[variableName] = vars()[variableName].dropna(axis=1, how='all')
                except:continue
        except:continue

thickness = dict()
for item in csvFiles:
    try:
        thickness['raw'] = pd.read_csv('preTreatment/'+item, header=0,\
                                float_precision='high')
        if len(thickness['raw'].columns) == 8:
            thickness['raw'].drop(['Gradients_0','Gradients_1','Gradients_2'],\
                     axis=1, inplace=True)
        colNames = ['x', 'y', 'z', 'UMean_X', 'absGradient']
        thickness['raw'].columns = colNames
        
        del colNames
    except:continue

try:
    del aux, variableName, item2, plane
except:pass

del files, item, rawFiles, csvFiles, reg
