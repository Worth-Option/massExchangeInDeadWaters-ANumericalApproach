#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries
import os
import re
import pandas as pd
import openpyxl

files = os.listdir('treatment')
folder = os.path.abspath('treatment')

# Check for csv files
csvFiles = list()
for item in files:
    if re.search('.\.csv', item):
        csvFiles.append(item)
        
# Check for xlsx files
xlsxFiles = list()
for item in files:
    if re.search('.\.xlsx', item):
        xlsxFiles.append(item)

# Check for txt files
txtFiles = list()
for item in files:
    if re.search('.\.txt', item):
        txtFiles.append(item)

# Import generated data
uniqueSim = list()
uniqueVar = list()
xlsxVar = list()
direction = list()
planes = list()
data = dict()

for item in csvFiles:
    try:
        sim = re.split("_", item)[0]
        variableName = re.split("_", item)[1]
        if variableName[-4:] == '.csv':
            variableName = variableName[:-4]
        
        if sim not in uniqueSim:
            uniqueSim.append(sim)
        if variableName not in uniqueVar:
            uniqueVar.append(variableName)
        try:
            plane = re.split("_", item)[2]
            axis = re.split("_", item)[4]
            axis = axis[:-4] #Removes '.csv'
            if axis not in direction:
                direction.append(axis)
            if plane not in planes:
                planes.append(plane)
            del variableName, axis, plane
        except:continue
    except:continue

for item in xlsxFiles:
    try:
        sim = re.split("_", item)[0]
        variableName = re.split("_", item)[1]
        variableName = variableName[:-5]
        if sim not in uniqueSim:
            uniqueSim.append(sim)
        if variableName not in xlsxVar:
            xlsxVar.append(variableName)
    except:
        continue

for item in txtFiles:
    file = open(os.path.join(folder, item), "r")
    for line in file:
        if re.search('ktracer.', line):
            words = line.split()
            ktracer = float(words[2])
            continue
        elif re.search('kvelocity.', line):
            words = line.split()
            kvelocity = float(words[2])

    d = {'Simulation':[re.split("_", item)[0]], 'kTracer':[ktracer], 'kVelocity':[kvelocity]}
    df = pd.DataFrame(data=d)

    if 'massExchange' in locals() or 'massExchange' in globals():
        massExchange = massExchange.append(df, ignore_index=True)
    else:
        massExchange = df
        
    del item, d, df, words, line
    del ktracer, kvelocity

tracerData = dict()
for var in uniqueVar:
    if var != 'tracerData.csv':
        data[var] = dict()
    for sim in uniqueSim:
        data[var][sim] = dict()
        if var == 'tracerData':
            file = sim+"_tracerData.csv"
            pathToFile = os.path.join(folder, file)
            if os.path.exists(pathToFile):
                tracerData[sim] = pd.read_csv(pathToFile, index_col=0,
                          float_precision="high")
        else:
            for plane in planes:
                data[var][sim][plane] = dict()
                for axis in direction:
                    file = sim+"_"+var+"_"+plane+"_Dir_"+axis+".csv"
                    pathToFile = os.path.join(folder, file)
                    if os.path.exists(pathToFile):
                        data[var][sim][plane][axis] = pd.read_csv(pathToFile,\
                            index_col=0, float_precision="high")

thickness = dict()
for sim in uniqueSim:
    file = sim+"_thickness.xlsx"
    pathToFile = os.path.join(folder, file)
    if os.path.exists(pathToFile):
        thickness[sim] = pd.read_excel(pathToFile)

#del files, txtFiles, file, csvFiles, plane, var, sim, axis, pathToFile, direction
