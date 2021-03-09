#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import openpyxl
import pandas as pd

# Append densities to mass exchange
try:
    densities = pd.read_csv(os.path.join(folder,'densities.csv'),index_col=0)
except:
    print("Imported Simulations:\n",uniqueSim)
    print("Please enter the vegetation density of each simulation:")
    density = dict()
    for sim in uniqueSim:
        density[sim] = float(input(sim+":"))
    densities = pd.DataFrame.from_dict(density, orient = 'index')
    densities.reset_index(level=0, inplace=True)
    colName = ['Simulation','Density']
    densities.columns = colName
    densities.to_csv(os.path.join(folder,'densities.csv'))
    del sim, colName

try:
    massExchange.insert(1,'Veg. Density',densities['Density'])
except:pass

massExchange.style.format({'Veg. Density': "{:.4%}"})
massExchange.sort_values(by=['Veg. Density'], inplace=True)

massExchange['Case'] = range(len(massExchange))

# Retrieve mean residence time
massExchange.eval('mrtTracer = 1/kTracer', inplace=True)
massExchange.eval('mrtVelocity = 1/kVelocity', inplace=True)

fileName = os.path.join(folder,'results/CSV/massExchange.xlsx')
massExchange.to_excel(fileName, index=False)

densities.sort_values(by=['Density'], inplace=True)
densities.reset_index(drop=True, inplace=True)
del fileName

# Mixing Layer Thickness
try:
    for sim in uniqueSim:
        thickness[sim].eval('xL = x/0.25', inplace=True)
        thickness[sim].rename(columns={'xL':'(x-x0)/L'}, inplace=True)
except:pass
