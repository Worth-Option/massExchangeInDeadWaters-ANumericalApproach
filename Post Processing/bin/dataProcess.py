#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  dataProcess.py
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
This code processes the data imported from importcsv.py
The data is ensembled averaged and then exported to plot.py script
"""

import re
import pandas as pd
import openpyxl
from scipy.interpolate import interp1d

def dfRename(var, dtf):
    names = ['x', 'y', 'z']
    names.extend(var)
    dtf.columns = names

def clearLimits(df,x0,x1,y0,y1,z0,z1):
# =============================================================================
#     Clear extra values inside variables.
#     This script uses user values of the bound coordinates
# =============================================================================

    df.drop(df[df.x < x0].index, inplace=True)
    df.drop(df[df.x > x1].index, inplace=True)
    df.drop(df[df.y < y0].index, inplace=True)
    df.drop(df[df.y > y1].index, inplace=True)
    df.drop(df[df.z < z0].index, inplace=True)
    df.drop(df[df.z > z1].index, inplace=True)
    return df

def excelExport(var, name):
# =============================================================================
#     Creates and appends planes into an spreadsheet
# =============================================================================
    
    if not os.path.isfile('preTreatment/results/Excel/'+name+'.xlsx'):
        wb = openpyxl.Workbook()
        wb.save('preTreatment/results/Excel/'+name+'.xlsx')

    with pd.ExcelWriter('preTreatment/results/Excel/'+name+'.xlsx',
                        engine="openpyxl", mode='a') as writer:
        for df_name, df in var.items():
            df.to_excel(writer, sheet_name=df_name, index=False)
            
def csvExport(df, name):
# =============================================================================
#     Creates and appends planes into separated csv files
# =============================================================================
    df.to_csv('preTreatment/results/CSV/'+name+'.csv')

def varTreatment(planes, physicalVar, colNames, nColumns, direction,
                 varName, roundPar, first, last):
# =============================================================================
#     Treats data in an ensemble averaging proceedure in the provided direction
# =============================================================================

    # Local Variable Declaration
    varDict = dict()
    kk = first * nColumns
    startPos = first
    stopPos = last * nColumns
    ll = 0
  
    # Reads all the files and ensemble in a dict in that each ii is a plane
    for ii in planes:
        key = ii
        key = int(re.sub('\D', '',key))
        if key < startPos:
            continue
        if kk > stopPos: 
            break
        for jj in range(nColumns):
            ll = kk + jj
            if ll%nColumns == 0: # number of columns
                varDict[ii] = physicalVar.iloc[:,ll]
            else:
                varDict[ii] = \
                    pd.concat([varDict[ii], physicalVar.iloc[:,ll]], axis=1)
                    
        kk = kk + nColumns

        dfRename(colNames, varDict[ii])
        clearLimits(varDict[ii], 0.25, 0.50, 0.30, 0.45, 0, 0.1)
        varDict[ii] = varDict[ii].dropna(axis=0, how='all')
        varDict[ii] = varDict[ii].dropna(axis=1, how='all')

        # Get vector magnitude
        if nColumns > 4:
            df = pd.DataFrame()
            for i in colNames:
                df[i] = varDict[ii][i]**2
            df['mag'] = (df.sum(axis=1))**(1/2)
            varDict[ii]['mag'] = df.mag
            expColNames = colNames + ['mag']
        else:
            expColNames = colNames
            
        if direction == "x":
            varDict[ii] = varDict[ii].drop(columns=['y', 'z'])
            varDict[ii] = varDict[ii].\
            groupby(varDict[ii].x.round(roundPar),as_index=False).mean()
            varDict[ii][direction] = (varDict[ii][direction] - 0.25)/L
            varDict[ii].columns = ['('+direction+'-x0)'+'/L'] + expColNames
        elif direction == 'y':
            varDict[ii] = varDict[ii].drop(columns=['x', 'z'])
            varDict[ii] = varDict[ii].\
            groupby(varDict[ii].y.round(roundPar),as_index=False).mean()
            varDict[ii][direction] = (varDict[ii][direction] - 0.30)/H
            varDict[ii].columns = ['('+direction+'-y0)'+'/H'] + expColNames
        elif direction == 'z':
            varDict[ii] = varDict[ii].drop(columns=['x', 'y'])
            varDict[ii] = varDict[ii].\
            groupby(varDict[ii].z.round(roundPar),as_index=False).mean()
            varDict[ii][direction] = varDict[ii][direction]/H
            varDict[ii].columns = [direction+'/H'] + expColNames
            
        excelExport(varDict, varName+"Dir_"+direction)
        csvName = varName.split("_")[0]
        csvExport(varDict[ii], csvName+"_"+ii+"_Dir_"+direction)
    return varDict


# =============================================================================
# Planes 0 -> 4
# Vertical Planes Varying the Y axis from Y = 0.30 to Y = 0.45
# =============================================================================
## RMean
colNames = ['xx', 'yy', 'zz', 'xy', 'yz', 'xz']
RMean_00_04_Dirx = varTreatment(uniqueRaw, RMean, colNames, 9,'x',
                               'RMean_00_4_',2, 0, 4)
RMean_00_04_Dirz = varTreatment(uniqueRaw, RMean, colNames, 9,'z',
                               'RMean_00_4_',2, 0, 4)

## UMean
colNames = ['u', 'v', 'w']
UMean_00_04_Dirx = varTreatment(uniqueRaw, UMean, colNames, 6,'x',
                               'UMean_00_4_',2, 0, 4)
UMean_00_04_Dirz = varTreatment(uniqueRaw, UMean, colNames, 6,'z',
                               'UMean_00_4_',2, 0, 4)

## lambVectorMean
colNames = ['lambVectorMean_x', 'lambVectorMean_y', 'lambVectorMean_z']
lambVectorMean_00_04_Dirx = varTreatment(uniqueRaw, lambVectorMean, colNames, 6,
                                    'x','lambVectorMean_00_4_',3, 0, 4)
lambVectorMean_00_04_Dirz = varTreatment(uniqueRaw, lambVectorMean, colNames,
                                    6,'z','lambVectorMean_00_4_',2, 0, 4)

## pMean
colNames = ['pMean']
pMean_00_04_Dirx = varTreatment(uniqueRaw, pMean, colNames, 4,'x',
                               'pMean_00_4_',3, 0, 4)
pMean_00_04_Dirz = varTreatment(uniqueRaw, pMean, colNames, 4,'z',
                               'pMean_00_4_',2, 0, 4)

## vorticityMean
colNames = ['vorticityMean_x', 'vorticityMean_y', 'vorticityMean_z']
vorticityMean_00_04_Dirx = varTreatment(uniqueRaw, vorticityMean, colNames, 6,
                                  'x','vorticityMean_00_4_',3, 0, 4)
vorticityMean_00_04_Dirz = varTreatment(uniqueRaw, vorticityMean, colNames, 6,
                                  'z','vorticityMean_00_4_',2, 0, 4)

# =============================================================================
# Planes 5 -> 11
# Vertical Planes Varying the X axis from X = 0.25 to X = 0.50
# =============================================================================
## RMean
colNames = ['xx', 'yy', 'zz', 'xy', 'yz', 'xz']
RMean_05_11_Diry = varTreatment(uniqueRaw, RMean, colNames, 9,'y',
                                'RMean_05_11_',2, 5, 11)
RMean_05_11_Dirz = varTreatment(uniqueRaw, RMean, colNames, 9,'z',
                                'RMean_05_11_',2, 5, 11)

## UMean
colNames = ['u', 'v', 'w']
UMean_05_11_Diry = varTreatment(uniqueRaw, UMean, colNames, 6,'y',
                                'UMean_05_11_',2, 5, 11)
UMean_05_11_Dirz = varTreatment(uniqueRaw, UMean, colNames, 6,'z',
                                'UMean_05_11_',2, 5, 11)

## lambVectorMean
colNames = ['lambVectorMean_x', 'lambVectorMean_y', 'lambVectorMean_z']
lambVectorMean_05_11_Diry = varTreatment(uniqueRaw, lambVectorMean, colNames, 6,
                                    'y','lambVectorMean_05_11_',3, 5, 11)
lambVectorMean_05_11_Dirz = varTreatment(uniqueRaw, lambVectorMean, colNames,
                                    6,'z','lambVectorMean_05_11_',2, 5, 11)

## pMean
colNames = ['pMean']
pMean_05_11_Diry = varTreatment(uniqueRaw, pMean, colNames, 4,'y',
                                'pMean_05_11_',3, 5, 11)
pMean_05_11_Dirz = varTreatment(uniqueRaw, pMean, colNames, 4,'z',
                                'pMean_05_11_',2, 5, 11)

## vorticityMean
colNames = ['vorticityMean_x', 'vorticityMean_y', 'vorticityMean_z']
vorticityMean_05_11_Diry = varTreatment(uniqueRaw, vorticityMean, colNames, 6,
                                  'y','vorticityMean_05_11_',3, 5, 11)
vorticityMean_05_11_Dirz = varTreatment(uniqueRaw, vorticityMean, colNames, 6,
                                  'z','vorticityMean_05_11_',2, 5, 11)

# =============================================================================
# Planes 12 -> 21
# Horizontal Planes Varying the Z axis from Z = 0 to Z = 0.10
# =============================================================================
## RMean
colNames = ['xx', 'yy', 'zz', 'xy', 'yz', 'xz']
RMean_12_21_Dirx = varTreatment(uniqueRaw, RMean, colNames, 9,'x',
                                'RMean_12_21_',2, 12, 21)
RMean_12_21_Diry = varTreatment(uniqueRaw, RMean, colNames, 9,'y',
                                'RMean',2, 12, 21)

## UMean
colNames = ['u', 'v', 'w']
UMean_12_21_Dirx = varTreatment(uniqueRaw, UMean, colNames, 6,'x',
                                'UMean_12_21_',2, 12, 21)
UMean_12_21_Diry = varTreatment(uniqueRaw, UMean, colNames, 6,'y',
                                'UMean_12_21_',2, 12, 21)

## lambVectorMean
colNames = ['lambVectorMean_x', 'lambVectorMean_y', 'lambVectorMean_z']
lambVectorMean_12_21_Dirx = varTreatment(uniqueRaw, lambVectorMean, colNames, 6,
                                    'x','lambVectorMean_12_21_',3, 12, 21)
lambVectorMean_12_21_Diry = varTreatment(uniqueRaw, lambVectorMean, colNames,
                                    6,'y','lambVectorMean_12_21_',2, 12, 21)

## pMean
colNames = ['pMean']
pMean_12_21_Dirx = varTreatment(uniqueRaw, pMean, colNames, 4,'x',
                                'pMean_12_21_',3, 12, 21)
pMean_12_21_Diry = varTreatment(uniqueRaw, pMean, colNames, 4,'y',
                                'pMean_12_21_',2, 12, 21)

## vorticityMean
colNames = ['vorticityMean_x', 'vorticityMean_y', 'vorticityMean_z']
vorticityMean_12_21_Dirx = varTreatment(uniqueRaw, vorticityMean, colNames, 6,
                                  'x','vorticityMean_12_21_',3, 12, 21)
vorticityMean_12_21_Diry = varTreatment(uniqueRaw, vorticityMean, colNames, 6,
                                  'y','vorticityMean_5_11_',2, 12, 21)

# =============================================================================
# Validation Data
# =============================================================================
## Data Treatment
colNames = ['u', 'v', 'w']
fig4aOur = varTreatment(['p17'], UMean, colNames, 6, "y",'UMean_p17_',
                            3, 17, 17)
fig4aOur = fig4aOur['p17']
fig4aOur.u = fig4aOur.u/U

# Errors from experimental
error = dict()
error['X'] = literatureExp.iloc[:,0]
error['Numerical_u'] = interp1d(fig4aOur.iloc[:,0],fig4aOur.u)(literatureExp.iloc[:,0])
error['Experimental_u'] = literatureExp.iloc[:,1]

error = pd.DataFrame(data=error)
error.eval('Error = Experimental_u - Numerical_u', inplace=True)
error.eval('Abs_Error = abs(Experimental_u - Numerical_u)', inplace=True)
error.eval('Rel_Error = (Experimental_u - Numerical_u)/Experimental_u', inplace=True)
error.eval('Abs_Rel_Error = abs((Experimental_u - Numerical_u)/Experimental_u)', inplace=True)

description = error.describe()

if not os.path.isfile('preTreatment/results/Excel/validationData.xlsx'):
    wb = openpyxl.Workbook()
    wb.save('preTreatment/results/Excel/validationData.xlsx')

with pd.ExcelWriter('preTreatment/results/Excel/validationData.xlsx',
                    engine="openpyxl", mode='a') as writer:
    error.to_excel(writer, sheet_name='Errors', index=False)
    description.to_excel(writer, sheet_name='Statistical Description')

del lambVectorMean, pMean, RMean, vorticityMean, colNames
