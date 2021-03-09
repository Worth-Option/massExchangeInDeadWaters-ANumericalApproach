#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  multipleSimulationPlot.py
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
Data is imported from multipleSimulationProcess.py and ploted into jpg figures
"""

# Libraries
import os
import matplotlib.pyplot as plt

#plt.rcParams.update({
#    "text.usetex": True,
#    "font.family": "sans-serif",
#    "font.sans-serif": ["Helvetica"]})

figFolder = os.path.abspath('treatment/results/Plots')
selFigFolder = os.path.abspath('treatment/results/SelectPlots')

def plotVar(varName, axis, title, col, admensional):
# =============================================================================
#     Runs through all plots from a variable and plots it
# =============================================================================
    
    for plane in planes:
        anySim = uniqueSim[0]
        for direction in data[varName][anySim][plane].keys():
            fig, ax = plt.subplots(figsize=(9,6), dpi=300)
            for sim in uniqueSim:
                df = data[varName][sim][plane][direction]
                lbl = densities.loc[densities['Simulation'] == sim]
                lbl = lbl['Density'].iloc[0]
                ax.plot(df.iloc[:,0], df.iloc[:,col]/admensional,
                        label='{:.4%}'.format(lbl))
    
            ax.legend(loc='best',fontsize='x-large')
            if title != "None":
                ax.set_title(title,fontsize='xx-large')
            if direction == 'x':
                axis[0] = '(x-x0)/L'
            elif direction == 'y':
                axis[0] = '(y-yo)/H'
            elif direction == 'z':
                axis[0] = 'z/H'
                
            plt.grid()
            plt.autoscale(enable=True, tight=True)
            plt.xlabel(axis[0],fontsize='x-large')
            plt.ylabel(axis[1],fontsize='x-large')
            
            # Save the image in memory in JPG format
            figName = varName+'_'+plane+'_Dir_'+direction+'.jpg'
            figName = os.path.join(figFolder, figName)
            plt.savefig(figName, box_inches='tight')
            plt.close()

# =============================================================================
# Variables
# =============================================================================

noTitle = "None"
            
## RMean
axisNames = ['(x-x0)/L','Rmag/U²']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude'
plotVar('RMean', axisNames, noTitle, 7, U**2)

## UMean
axisNames = ['(x-x0)/L','uMag/U']
plotTitle = 'Time Averaged velocity magnitude'
plotVar('UMean', axisNames, noTitle, 4, U)

axisNames = ['(x-x0)/L','u/U']
plotTitle = 'Time Averaged velocity magnitude'
plotVar('UMean', axisNames, noTitle, 1, U)

axisNames = ['(x-x0)/L','v/U']
plotTitle = 'Time Averaged velocity magnitude'
plotVar('UMean', axisNames, noTitle, 2, U)

axisNames = ['(x-x0)/L','w/U']
plotTitle = 'Time Averaged velocity magnitude'
plotVar('UMean', axisNames, noTitle, 3, U)

## lambVectorMean
axisNames = ['(x-x0)/L','lambVectorMag']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude'
plotVar('lambVectorMean', axisNames, noTitle, 4, 1)

## pMean
axisNames = ['(x-x0)/L',r'(pL)/($\rho$ U)']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude'
plotVar('pMean', axisNames, noTitle, 1, L/(RHO*U))

## vorticity
axisNames = ['z/H', 'vorticity [1/s]']
plotTitle = 'Time Averaged vorticity magnitude'
plotVar('vorticityMean', axisNames, noTitle, 4, 1)

# =============================================================================
# Mass Exchange
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)
ax1 = ax.twinx()

#for sim in uniqueSim:
#    case = massExchange.loc[massExchange['Simulation'] == sim]
#    vDensity = case['Veg. Density'].iloc[0]*100
#    caseName = 'Case '+str(densities.loc[densities['Simulation'] == sim].index[0])
    
ln1 = ax.plot(massExchange['Veg. Density']*100, massExchange['kTracer'], 'bo',
        label=r'$k_{DZ}$', lw=2, ms=6)
ln2 = ax1.plot(massExchange['Veg. Density']*100, massExchange['mrtTracer'], 'ks', 
         label=r'$T_{DZ}$', lw=2, ms=5)
    
# Primary Axis
#ax.set_xlabel('Vegetation Density [%]',fontsize='x-large')
#ax.set_ylabel('Mass Exchange Coefficient [non-dimensional]',fontsize='x-large')
ax.set_xlabel('a [%]',fontsize='x-large')
ax.set_ylabel('k [non-dimensional]',fontsize='x-large')
ax.set_xlim(0, 11)

# Secondary Axis
ax1.set_ylabel(r'$T_{DZ}$ [s]',fontsize='x-large')

plt.autoscale(enable=True, tight=True)

# Legend
lns = ln1+ln2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=7)

#plt.legend(bbox_to_anchor=(1.15,1), loc="upper left")
#plt.tight_layout(rect=[0,0,0.75,1])
#ax.set_title('Mass Exchange variation through all vegetation densities',
#             fontsize='xx-large')
#plt.subplots_adjust(right=0.7)

# Save the image in memory in JPG format
figName = 'massExchange.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ln1, ln2, ax, fig, labs

# =============================================================================
# Tracer decay
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(tracerData['x068']['Time'],
              tracerData['x068']['Numerical'],
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(tracerData['x062']['Time'],
              tracerData['x062']['Numerical'],
              '--', label='Case 1', lw=2, ms=6)
ln2 = ax.plot(tracerData['x063']['Time'],
              tracerData['x063']['Numerical'],
              '-.', label='Case 2', lw=2, ms=6)
ln3 = ax.plot(tracerData['x064']['Time'],
              tracerData['x064']['Numerical'],
              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.plot(tracerData['x065']['Time'],
              tracerData['x065']['Numerical'],
              '-.', label='Case 4', lw=2, ms=6)
ln5 = ax.plot(tracerData['x066']['Time'],
              tracerData['x066']['Numerical'],
              '--', label='Case 5', lw=2, ms=6)
ln6 = ax.plot(tracerData['x067']['Time'],
              tracerData['x067']['Numerical'],
              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.plot(tracerData['x115']['Time'],
              tracerData['x115']['Numerical'],
              '-.', label='Case 7', lw=2, ms=6)
ln8 = ax.plot(tracerData['x116']['Time'],
              tracerData['x116']['Numerical'],
              ':', label='Case 8', lw=2, ms=6)
ln9 = ax.plot(tracerData['x117']['Time'],
              tracerData['x117']['Numerical'],
              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.plot(tracerData['x115']['Time'],
               tracerData['x115']['Numerical'],
              '--', label='Case 10', lw=2, ms=6)

# Primary Axis
ax.set_xlabel('Time [s]',fontsize='x-large')
ax.set_ylabel('Concentration',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln2+ln3+ln4+ln5+ln6+ln7+ln8+ln9+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs)

# Save the image in memory in JPG format
figName = 'tracerDecay.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Tracer decay (SemiLog Y)
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.semilogy(tracerData['x068']['Time'],
              tracerData['x068']['Numerical'],
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.semilogy(tracerData['x062']['Time'],
              tracerData['x062']['Numerical'],
              '--', label='Case 1', lw=2, ms=6)
ln2 = ax.semilogy(tracerData['x063']['Time'],
              tracerData['x063']['Numerical'],
              '-.', label='Case 2', lw=2, ms=6)
ln3 = ax.semilogy(tracerData['x064']['Time'],
              tracerData['x064']['Numerical'],
              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.semilogy(tracerData['x065']['Time'],
              tracerData['x065']['Numerical'],
              '-.', label='Case 4', lw=2, ms=6)
ln5 = ax.semilogy(tracerData['x066']['Time'],
              tracerData['x066']['Numerical'],
              '--', label='Case 5', lw=2, ms=6)
ln6 = ax.semilogy(tracerData['x067']['Time'],
              tracerData['x067']['Numerical'],
              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.semilogy(tracerData['x115']['Time'],
              tracerData['x115']['Numerical'],
              '-.', label='Case 7', lw=2, ms=6)
ln8 = ax.semilogy(tracerData['x116']['Time'],
              tracerData['x116']['Numerical'],
              ':', label='Case 8', lw=2, ms=6)
ln9 = ax.semilogy(tracerData['x117']['Time'],
              tracerData['x117']['Numerical'],
              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.semilogy(tracerData['x115']['Time'],
               tracerData['x115']['Numerical'],
              '--', label='Case 10', lw=2, ms=6)

# Primary Axis
ax.set_xlabel('Time [s]',fontsize='x-large')
ax.set_ylabel('Concentration',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln2+ln3+ln4+ln5+ln6+ln7+ln8+ln9+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs)

# Save the image in memory in JPG format
figName = 'tracerDecaySemiLogY.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# X-Velocity at XY PLANE versus (y-y0)/H Unique
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(data['UMean']['x068']['p17']['y']['(y-y0)/H'],
              data['UMean']['x068']['p17']['y']['u']/U,
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(data['UMean']['x062']['p17']['y']['(y-y0)/H'],
              data['UMean']['x062']['p17']['y']['u']/U,
              '--', label='Case 1', lw=2, ms=6)
ln4 = ax.plot(data['UMean']['x065']['p17']['y']['(y-y0)/H'],
              data['UMean']['x065']['p17']['y']['u']/U,
              '-.', label='Case 4', lw=2, ms=6)
ln7 = ax.plot(data['UMean']['x115']['p17']['y']['(y-y0)/H'],
              data['UMean']['x115']['p17']['y']['u']/U,
              '-.', label='Case 7', lw=2, ms=6)
ln10 = ax.plot(data['UMean']['x115']['p17']['y']['(y-y0)/H'],
               data['UMean']['x115']['p17']['y']['u']/U,
              ':', label='Case 10', lw=2, ms=6)

# Primary Axis
ax.set_xlabel(r'(y-$y_0$)/H',fontsize='x-large')
ax.set_ylabel('u/U',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln4+ln7+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=7)

# Save the image in memory in JPG format
figName = 'velXYPlane.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Y-Velocity at Interface versus z/H Unique
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(data['UMean']['x068']['p00']['z']['v']/U,
              data['UMean']['x068']['p00']['z']['z/H'],
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(data['UMean']['x062']['p00']['z']['v']/U,
              data['UMean']['x062']['p00']['z']['z/H'],
              '--', label='Case 1', lw=2, ms=6)
#ln2 = ax.plot(data['UMean']['x063']['p00']['z']['v']/U,
#              data['UMean']['x063']['p00']['z']['z/H'],
#              '-.', label='Case 2', lw=2, ms=6)
#ln3 = ax.plot(data['UMean']['x064']['p00']['z']['v']/U,
#              data['UMean']['x064']['p00']['z']['z/H'],
#              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.plot(data['UMean']['x065']['p00']['z']['v']/U,
              data['UMean']['x065']['p00']['z']['z/H'],
              '-.', label='Case 4', lw=2, ms=6)
#ln5 = ax.plot(data['UMean']['x066']['p00']['z']['v']/U,
#              data['UMean']['x066']['p00']['z']['z/H'],
#              '--', label='Case 5', lw=2, ms=6)
#ln6 = ax.plot(data['UMean']['x067']['p00']['z']['v']/U,
#              data['UMean']['x067']['p00']['z']['z/H'],
#              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.plot(data['UMean']['x115']['p00']['z']['v']/U,
              data['UMean']['x115']['p00']['z']['z/H'],
              '-.', label='Case 7', lw=2, ms=6)
#ln8 = ax.plot(data['UMean']['x116']['p00']['z']['v']/U,
#              data['UMean']['x116']['p00']['z']['z/H'],
#              ':', label='Case 8', lw=2, ms=6)
#ln9 = ax.plot(data['UMean']['x117']['p00']['z']['v']/U,
#              data['UMean']['x117']['p00']['z']['z/H'],
#              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.plot(data['UMean']['x115']['p00']['z']['v']/U,
              data['UMean']['x115']['p00']['z']['z/H'],
              ':', label='Case 10', lw=2, ms=6)

# Primary Axis
ax.set_xlabel('v/U',fontsize='x-large')
ax.set_ylabel('z/H',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln4+ln7+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=7)

# Save the image in memory in JPG format
figName = 'yVelatInterfaceZAxis.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Y-Velocity at Interface versus z/H 1
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(data['UMean']['x068']['p00']['z']['v']/U,
              data['UMean']['x068']['p00']['z']['z/H'],
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(data['UMean']['x062']['p00']['z']['v']/U,
              data['UMean']['x062']['p00']['z']['z/H'],
              '--', label='Case 1', lw=2, ms=6)
ln2 = ax.plot(data['UMean']['x063']['p00']['z']['v']/U,
              data['UMean']['x063']['p00']['z']['z/H'],
              '-.', label='Case 2', lw=2, ms=6)
ln3 = ax.plot(data['UMean']['x064']['p00']['z']['v']/U,
              data['UMean']['x064']['p00']['z']['z/H'],
              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.plot(data['UMean']['x065']['p00']['z']['v']/U,
              data['UMean']['x065']['p00']['z']['z/H'],
              '-.', label='Case 4', lw=2, ms=6)
ln5 = ax.plot(data['UMean']['x066']['p00']['z']['v']/U,
              data['UMean']['x066']['p00']['z']['z/H'],
              '--', label='Case 5', lw=2, ms=6)
    
# Primary Axis
ax.set_xlabel('v/U',fontsize='x-large')
ax.set_ylabel('z/H',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln2+ln3+ln4+ln5
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=7)

# Title
plt.title('a)', loc='left', fontweight='bold')

# Save the image in memory in JPG format
figName = 'yVelatInterfaceZAxis1.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Y-Velocity at Interface versus z/H 2
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln5 = ax.plot(data['UMean']['x066']['p00']['z']['v']/U,
              data['UMean']['x066']['p00']['z']['z/H'],
              '-', label='Case 5', lw=2, ms=6)
ln6 = ax.plot(data['UMean']['x067']['p00']['z']['v']/U,
              data['UMean']['x067']['p00']['z']['z/H'],
              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.plot(data['UMean']['x115']['p00']['z']['v']/U,
              data['UMean']['x115']['p00']['z']['z/H'],
              '-.', label='Case 7', lw=2, ms=6)
ln8 = ax.plot(data['UMean']['x116']['p00']['z']['v']/U,
              data['UMean']['x116']['p00']['z']['z/H'],
              ':', label='Case 8', lw=2, ms=6)
ln9 = ax.plot(data['UMean']['x117']['p00']['z']['v']/U,
              data['UMean']['x117']['p00']['z']['z/H'],
              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.plot(data['UMean']['x115']['p00']['z']['v']/U,
              data['UMean']['x115']['p00']['z']['z/H'],
              '--', label='Case 10', lw=2, ms=6)
    
# Primary Axis
ax.set_xlabel('v/U',fontsize='x-large')
ax.set_ylabel('z/H',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln5+ln6+ln7+ln8+ln9+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=7)

# Title
plt.title('b)', loc='left', fontweight='bold')

# Save the image in memory in JPG format
figName = 'yVelatInterfaceZAxis2.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Y-Velocity at Interface versus (x-x0)/L Unique
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(data['UMean']['x068']['p00']['x']['(x-x0)/L'],
              data['UMean']['x068']['p00']['x']['v']/U,
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(data['UMean']['x062']['p00']['x']['(x-x0)/L'],
              data['UMean']['x062']['p00']['x']['v']/U,
              '--', label='Case 1', lw=2, ms=6)
ln2 = ax.plot(data['UMean']['x063']['p00']['x']['(x-x0)/L'],
              data['UMean']['x063']['p00']['x']['v']/U,
              '-.', label='Case 2', lw=2, ms=6)
ln3 = ax.plot(data['UMean']['x064']['p00']['x']['(x-x0)/L'],
              data['UMean']['x064']['p00']['x']['v']/U,
              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.plot(data['UMean']['x065']['p00']['x']['(x-x0)/L'],
              data['UMean']['x065']['p00']['x']['v']/U,
              '-.', label='Case 4', lw=2, ms=6)
ln5 = ax.plot(data['UMean']['x066']['p00']['x']['(x-x0)/L'],
              data['UMean']['x066']['p00']['x']['v']/U,
              '--', label='Case 5', lw=2, ms=6)
ln6 = ax.plot(data['UMean']['x067']['p00']['x']['(x-x0)/L'],
              data['UMean']['x067']['p00']['x']['v']/U,
              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.plot(data['UMean']['x115']['p00']['x']['(x-x0)/L'],
              data['UMean']['x115']['p00']['x']['v']/U,
              '-.', label='Case 7', lw=2, ms=6)
ln8 = ax.plot(data['UMean']['x116']['p00']['x']['(x-x0)/L'],
              data['UMean']['x116']['p00']['x']['v']/U,
              ':', label='Case 8', lw=2, ms=6)
ln9 = ax.plot(data['UMean']['x117']['p00']['x']['(x-x0)/L'],
              data['UMean']['x117']['p00']['x']['v']/U,
              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.plot(data['UMean']['x115']['p00']['x']['(x-x0)/L'],
               data['UMean']['x115']['p00']['x']['v']/U,
              '--', label='Case 10', lw=2, ms=6)

# Primary Axis
ax.set_xlabel('(x-x0)/L',fontsize='x-large')
ax.set_ylabel('v/U',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln2+ln3+ln4+ln5+ln6+ln7+ln8+ln9+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs)

# Save the image in memory in JPG format
figName = 'yVelatInterfaceXAxis.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Y-Velocity at Interface versus (x-x0)/L 1
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(data['UMean']['x068']['p00']['x']['(x-x0)/L'],
              data['UMean']['x068']['p00']['x']['v']/U,
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(data['UMean']['x062']['p00']['x']['(x-x0)/L'],
              data['UMean']['x062']['p00']['x']['v']/U,
              '--', label='Case 1', lw=2, ms=6)
ln2 = ax.plot(data['UMean']['x063']['p00']['x']['(x-x0)/L'],
              data['UMean']['x063']['p00']['x']['v']/U,
              '-.', label='Case 2', lw=2, ms=6)
ln3 = ax.plot(data['UMean']['x064']['p00']['x']['(x-x0)/L'],
              data['UMean']['x064']['p00']['x']['v']/U,
              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.plot(data['UMean']['x065']['p00']['x']['(x-x0)/L'],
              data['UMean']['x065']['p00']['x']['v']/U,
              '-.', label='Case 4', lw=2, ms=6)
ln5 = ax.plot(data['UMean']['x066']['p00']['x']['(x-x0)/L'],
              data['UMean']['x066']['p00']['x']['v']/U,
              '--', label='Case 5', lw=2, ms=6)
    
# Primary Axis
ax.set_xlabel('(x-x0)/L',fontsize='x-large')
ax.set_ylabel('v/U',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln2+ln3+ln4+ln5
labs = [l.get_label() for l in lns]
ax.legend(lns, labs)

# Title
plt.title('a)', loc='left', fontweight='bold')

# Save the image in memory in JPG format
figName = 'yVelatInterfaceXAxis1.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Y-Velocity at Interface versus (x-x0)/L 2
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln5 = ax.plot(data['UMean']['x066']['p00']['x']['(x-x0)/L'],
              data['UMean']['x066']['p00']['x']['v']/U,
              '-', label='Case 5', lw=2, ms=6)
ln6 = ax.plot(data['UMean']['x067']['p00']['x']['(x-x0)/L'],
              data['UMean']['x067']['p00']['x']['v']/U,
              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.plot(data['UMean']['x115']['p00']['x']['(x-x0)/L'],
              data['UMean']['x115']['p00']['x']['v']/U,
              '-.', label='Case 7', lw=2, ms=6)
ln8 = ax.plot(data['UMean']['x116']['p00']['x']['(x-x0)/L'],
              data['UMean']['x116']['p00']['x']['v']/U,
              ':', label='Case 8', lw=2, ms=6)
ln9 = ax.plot(data['UMean']['x117']['p00']['x']['(x-x0)/L'],
              data['UMean']['x117']['p00']['x']['v']/U,
              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.plot(data['UMean']['x115']['p00']['x']['(x-x0)/L'],
               data['UMean']['x115']['p00']['x']['v']/U,
              '--', label='Case 10', lw=2, ms=6)
    
# Primary Axis
ax.set_xlabel('(x-x0)/L',fontsize='x-large')
ax.set_ylabel('v/U',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln5+ln6+ln7+ln8+ln9+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs)

# Title
plt.title('b)', loc='left', fontweight='bold')

# Save the image in memory in JPG format
figName = 'yVelatInterfaceXAxis2.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Internal thickness versus (x-x0)/L
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(thickness['x068']['(x-x0)/L'],
              thickness['x068']['internalThickness']/W,
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(thickness['x062']['(x-x0)/L'],
              thickness['x062']['internalThickness']/W,
              '--', label='Case 1', lw=2, ms=6)
ln2 = ax.plot(thickness['x063']['(x-x0)/L'],
              thickness['x063']['internalThickness']/W,
              '-.', label='Case 2', lw=2, ms=6)
ln3 = ax.plot(thickness['x064']['(x-x0)/L'],
              thickness['x064']['internalThickness']/W,
              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.plot(thickness['x065']['(x-x0)/L'],
              thickness['x065']['internalThickness']/W,
              '-.', label='Case 4', lw=2, ms=6)
ln5 = ax.plot(thickness['x066']['(x-x0)/L'],
              thickness['x066']['internalThickness']/W,
              '--', label='Case 5', lw=2, ms=6)
ln6 = ax.plot(thickness['x067']['(x-x0)/L'],
              thickness['x067']['internalThickness']/W,
              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.plot(thickness['x115']['(x-x0)/L'],
              thickness['x115']['internalThickness']/W,
              '-.', label='Case 7', lw=2, ms=6)
ln8 = ax.plot(thickness['x116']['(x-x0)/L'],
              thickness['x116']['internalThickness']/W,
              ':', label='Case 8', lw=2, ms=6)
ln9 = ax.plot(thickness['x117']['(x-x0)/L'],
              thickness['x117']['internalThickness']/W,
              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.plot(thickness['x115']['(x-x0)/L'],
               thickness['x115']['internalThickness']/W,
              '--', label='Case 10', lw=2, ms=6)
    
# Primary Axis
ax.set_xlabel('(x-x0)/L',fontsize='x-large')
ax.set_ylabel(r'$\delta_{in}$/W',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln2+ln3+ln4+ln5+ln6+ln7+ln8+ln9+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs)

# Save the image in memory in JPG format
figName = 'internalThickness.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# External thickness versus (x-x0)/L
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(thickness['x068']['(x-x0)/L'],
              thickness['x068']['externalThickness']/W,
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(thickness['x062']['(x-x0)/L'],
              thickness['x062']['externalThickness']/W,
              '--', label='Case 1', lw=2, ms=6)
ln2 = ax.plot(thickness['x063']['(x-x0)/L'],
              thickness['x063']['externalThickness']/W,
              '-.', label='Case 2', lw=2, ms=6)
ln3 = ax.plot(thickness['x064']['(x-x0)/L'],
              thickness['x064']['externalThickness']/W,
              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.plot(thickness['x065']['(x-x0)/L'],
              thickness['x065']['externalThickness']/W,
              '-.', label='Case 4', lw=2, ms=6)
ln5 = ax.plot(thickness['x066']['(x-x0)/L'],
              thickness['x066']['externalThickness']/W,
              '--', label='Case 5', lw=2, ms=6)
ln6 = ax.plot(thickness['x067']['(x-x0)/L'],
              thickness['x067']['externalThickness']/W,
              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.plot(thickness['x115']['(x-x0)/L'],
              thickness['x115']['externalThickness']/W,
              '-.', label='Case 7', lw=2, ms=6)
ln8 = ax.plot(thickness['x116']['(x-x0)/L'],
              thickness['x116']['externalThickness']/W,
              ':', label='Case 8', lw=2, ms=6)
ln9 = ax.plot(thickness['x117']['(x-x0)/L'],
              thickness['x117']['externalThickness']/W,
              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.plot(thickness['x115']['(x-x0)/L'],
               thickness['x115']['externalThickness']/W,
              '--', label='Case 10', lw=2, ms=6)
    
# Primary Axis
ax.set_xlabel('(x-x0)/L',fontsize='x-large')
ax.set_ylabel(r'$\delta_{out}$/W',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln2+ln3+ln4+ln5+ln6+ln7+ln8+ln9+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs)

# Save the image in memory in JPG format
figName = 'externalThickness.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs

# =============================================================================
# Total thickness versus (x-x0)/L
# =============================================================================
fig, ax = plt.subplots(figsize=(9,6), dpi=500)

ln0 = ax.plot(thickness['x068']['(x-x0)/L'],
              thickness['x068']['totalThickness']/W,
              '-', label='Case 0', lw=2, ms=6)
ln1 = ax.plot(thickness['x062']['(x-x0)/L'],
              thickness['x062']['totalThickness']/W,
              '--', label='Case 1', lw=2, ms=6)
ln2 = ax.plot(thickness['x063']['(x-x0)/L'],
              thickness['x063']['totalThickness']/W,
              '-.', label='Case 2', lw=2, ms=6)
ln3 = ax.plot(thickness['x064']['(x-x0)/L'],
              thickness['x064']['totalThickness']/W,
              ':', label='Case 3', lw=2, ms=6)
ln4 = ax.plot(thickness['x065']['(x-x0)/L'],
              thickness['x065']['totalThickness']/W,
              '-.', label='Case 4', lw=2, ms=6)
ln5 = ax.plot(thickness['x066']['(x-x0)/L'],
              thickness['x066']['totalThickness']/W,
              '--', label='Case 5', lw=2, ms=6)
ln6 = ax.plot(thickness['x067']['(x-x0)/L'],
              thickness['x067']['totalThickness']/W,
              '--', label='Case 6', lw=2, ms=6)
ln7 = ax.plot(thickness['x115']['(x-x0)/L'],
              thickness['x115']['totalThickness']/W,
              '-.', label='Case 7', lw=2, ms=6)
ln8 = ax.plot(thickness['x116']['(x-x0)/L'],
              thickness['x116']['totalThickness']/W,
              ':', label='Case 8', lw=2, ms=6)
ln9 = ax.plot(thickness['x117']['(x-x0)/L'],
              thickness['x117']['totalThickness']/W,
              '-.', label='Case 9', lw=2, ms=6)
ln10 = ax.plot(thickness['x115']['(x-x0)/L'],
               thickness['x115']['totalThickness']/W,
              '--', label='Case 10', lw=2, ms=6)
    
# Primary Axis
ax.set_xlabel('(x-x0)/L',fontsize='x-large')
ax.set_ylabel(r'$\delta$/W',fontsize='x-large')

plt.autoscale(enable=True, tight=True)
plt.grid()

# Legend
lns = ln0+ln1+ln2+ln3+ln4+ln5+ln6+ln7+ln8+ln9+ln10
labs = [l.get_label() for l in lns]
ax.legend(lns, labs)

# Save the image in memory in JPG format
figName = 'totalThickness.jpg'
figName = os.path.join(selFigFolder, figName)
plt.savefig(figName, box_inches='tight')
plt.close()

del lns, ax, fig, labs