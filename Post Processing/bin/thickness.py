#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  thickness.py
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
Data related to the mixing layer thickness is calculated in this module
"""

import re
import numpy as np
import pandas as pd

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

def dfRename(var, dtf):
    names = ['x', 'y', 'z']
    names.extend(var)
    dtf.columns = names
    
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

def ui(planes, physicalVar, colNames, nColumns, first, last):
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
        clearLimits(varDict[ii], 0.25, 0.50, 0, 0.45, 0, 0.1)
        varDict[ii] = varDict[ii].dropna(axis=0, how='all')
        varDict[ii] = varDict[ii].dropna(axis=1, how='all')
        varDict[ii].drop(columns=['y','v', 'w'], inplace=True)
    return varDict['p00']
    

# =============================================================================
# Mixing Layer Thickness Calculation
# =============================================================================
clearLimits(thickness['raw'], 0.25, 0.50, 0, 0.45, 0, 0.1)
thickness['raw'].x = thickness['raw'].x - 0.25

numZPlanes = 1
numXPlanes = 8

xMax = max(thickness['raw'].x)
zMax = max(thickness['raw'].z)

xtol = round(xMax/((numXPlanes + 1)*16), 6)
ztol = round(zMax/((numZPlanes + 1)*16), 6)

zz = zMax/(numZPlanes + 1)
aux = thickness['raw']
for ii in range(numZPlanes):
    xx = 0
    nameZ = 'z' + str(ii)
    thickness[nameZ] = dict()
    for jj in range(numXPlanes+2): #Origin and Destination
        nameX = 'x' + str(jj)
        xlim = [xx-xtol, xx+xtol]
        zlim = [zz-ztol, zz+ztol]
        thickness[nameZ][nameX] = dict()
        aux2 = aux[np.logical_and(\
                  np.logical_and(aux['z'] > zlim[0], aux['z'] < zlim[1]),\
                  np.logical_and(aux['x'] > xlim[0], aux['x'] < xlim[1]))]
        thickness[nameZ][nameX]['cav'] = aux2[aux2['y'] > 0.3].mean()
        thickness[nameZ][nameX]['channel'] = aux2[aux2['y'] < 0.3].mean()
        thickness[nameZ][nameX]['absGradient'] = max(aux2['absGradient'])
        
        xx = xx + xMax/(numXPlanes + 1)
    zz = zz + zMax/(numZPlanes + 1)

del ii, jj, aux, aux2, xx, zz, nameX, nameZ, xlim, zlim                   

# Organise data by planes
aux = thickness
thickness = dict()
zz = zMax/(numZPlanes + 1)
for ii in range(numZPlanes):
    xx = 0
    nameZ = 'z' + str(ii)
    thickness[nameZ] = dict()
    for jj in range(numXPlanes+2):
        nameX = 'x' + str(jj)
        if 'Ue' not in thickness[nameZ].keys():
            thickness[nameZ]['Ue'] = aux[nameZ][nameX]['cav'].to_frame().transpose()
            thickness[nameZ]['Um'] = aux[nameZ][nameX]['channel'].to_frame().transpose()
            thickness[nameZ]['maxGrad'] = dict() #k: x coord v: maxGrad
        else:
            thickness[nameZ]['Ue'] = thickness[nameZ]['Ue']\
            .append(aux[nameZ][nameX]['cav'].to_frame().transpose(),\
                    ignore_index = True)
            thickness[nameZ]['Um'] = thickness[nameZ]['Um']\
            .append(aux[nameZ][nameX]['channel'].to_frame().transpose(),\
                    ignore_index = True)
        thickness[nameZ]['maxGrad'][jj] = [aux[nameZ][nameX]['absGradient']]
        xx = xx + xMax/(numXPlanes + 1)
    thickness[nameZ]['Ue'].drop(columns=['y','absGradient'], inplace = True)
    thickness[nameZ]['Um'].drop(columns=['y','absGradient'], inplace = True)
    ue = ['x','z','Ue']
    um = ['x','z','Um']
    thickness[nameZ]['Ue'].columns = ue
    thickness[nameZ]['Um'].columns = um
    thickness[nameZ]['U'] = thickness[nameZ]['Ue']
    thickness[nameZ]['U']['Um'] = thickness[nameZ]['Um']['Um']
    thickness[nameZ]['maxGrad'] = pd.DataFrame(data=thickness[nameZ]['maxGrad'])
    thickness[nameZ] = thickness[nameZ]['U'].join(thickness[nameZ]['maxGrad'].\
             transpose())
    colNames = ['x','z','Ue','Um','maxGrad']
    thickness[nameZ].columns = colNames
    zz = zz + zMax/(numZPlanes + 1)

del ii, jj, ue, um, colNames  

# Calculates and appends Ui
colNames = ['u', 'v', 'w']
Uinterface = ui(uniqueRaw, UMean, colNames, 6, 0, 0)
Uinterface.x = Uinterface.x - 0.25

del colNames, UMean

zz = zMax/(numZPlanes + 1)
aux = Uinterface
Uinterface = dict()
for ii in range(numZPlanes):
    xx = 0
    nameZ = 'z' + str(ii)
    Uinterface[nameZ] = dict()
    for jj in range(numXPlanes+2): #Origin and Destination
        nameX = 'x' + str(jj)
        xlim = [xx-xtol, xx+xtol]
        zlim = [zz-ztol, zz+ztol]
        aux2 = aux[np.logical_and(\
                  np.logical_and(aux['z'] > zlim[0], aux['z'] < zlim[1]),\
                  np.logical_and(aux['x'] > xlim[0], aux['x'] < xlim[1]))]
        Uinterface[nameZ][nameX] = aux2.mean()

        xx = xx + xMax/(numXPlanes + 1)
    zz = zz + zMax/(numZPlanes + 1)
    
del ii, jj, aux, aux2, xx, zz, xtol, ztol, nameX, nameZ, xlim, zlim

# Organise data by planes
aux = Uinterface
Uinterface = dict()
zz = zMax/(numZPlanes + 1)
for ii in range(numZPlanes):
    xx = 0
    nameZ = 'z' + str(ii)
    Uinterface[nameZ] = dict()
    for jj in range(numXPlanes+2):
        nameX = 'x' + str(jj)
        Uinterface[nameZ][jj] = [aux[nameZ][nameX]['u']]
        xx = xx + xMax/(numXPlanes + 1)
        
    Uinterface[nameZ] = pd.DataFrame(data=Uinterface[nameZ]).transpose()
    try:
        thickness[nameZ].insert(3,'Ui',Uinterface[nameZ])
        thickness[nameZ].eval('internalThickness = (Ui-Ue)/maxGrad', inplace=True)
        thickness[nameZ].eval('externalThickness = (Um-Ui)/maxGrad', inplace=True)
        thickness[nameZ].eval('totalThickness = internalThickness + externalThickness',\
                 inplace=True)
        thickness[nameZ].eval('deltaInPerW = internalThickness/@W', inplace=True)
        thickness[nameZ].eval('deltaOutPerW = externalThickness/@W', inplace=True)
        thickness[nameZ].eval('deltaTotalPerW = totalThickness/@W', inplace=True)
    except:pass
    zz = zz + zMax/(numZPlanes + 1)

del ii, jj, zz, aux, Uinterface, nameX, nameZ

# Save to Excel
excelExport(thickness, 'thickness')
