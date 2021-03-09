#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  plot.py
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
Data is imported from dataProcess.py and ploted into png figures
"""

# Libraries
import re
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.offsetbox import AnchoredText

def plotVar(varName, axis, title, name, col, admensional, first, last):
# =============================================================================
#     Runs through all plots from a variable and plots it
# =============================================================================
    fig, ax = plt.subplots(figsize=(9,6), dpi=300)

    for key, df in varName.items():
        nKey = key
        nKey = int(re.sub('\D', '',nKey))
        if nKey >= first and nKey <= last:
            if 'z' not in varName[key].iloc[:,0].name:
                ax.plot(varName[key].iloc[:,0],
                        varName[key].iloc[:,col]/admensional, label=key)
            else:
                ax.plot(varName[key].iloc[:,col]/admensional,
                        varName[key].iloc[:,0], label=key)

    ax.legend(loc='best',fontsize='x-large')
    if title != "None":
        ax.set_title(title,fontsize='xx-large')

    plt.grid()
    plt.autoscale(enable=True, tight=True)
    plt.xlabel(axis[0],fontsize='x-large')
    plt.ylabel(axis[1],fontsize='x-large')
    plt.savefig('preTreatment/results/Plot/'+name+'.png', bbox_inches='tight',
                format='png')
    plt.close()

# =============================================================================
# Planes 0 -> 4
# Vertical Planes Varying the Y axis from Y = 0.30 to Y = 0.45
# =============================================================================

noTitle = "None"
    
## RMean Dir_x_00_04
axisNames = ['(x-x0)/L','Rmag/U²']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude at vertical XZ planes'
figureName = 'RMean_mag_Dir_x_00_04'
plotVar(RMean_00_04_Dirx, axisNames, noTitle, figureName, 7, U**2, 0, 4)

## RMean Dir_x_00_04
axisNames = ['Rmag/U²', 'z/H']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude at vertical XZ planes'
figureName = 'RMean_mag_Dir_x_00_04'
plotVar(RMean_00_04_Dirz, axisNames, noTitle, figureName, 7, U**2, 0, 4)

## UMean Dir_x_00_04
axisNames = ['(x-x0)/L','u/U']
plotTitle = 'Time Averaged x-velocity at vertical XZ planes'
figureName = 'UMean_U_Dir_x_00_04'
plotVar(UMean_00_04_Dirx, axisNames, noTitle, figureName, 1, U, 0, 4)

axisNames = ['(x-x0)/L','v/U']
plotTitle = 'Time Averaged y-velocity at vertical XZ planes'
figureName = 'UMean_V_Dir_x_00_04'
plotVar(UMean_00_04_Dirx, axisNames, noTitle, figureName, 2, U, 0, 4)

axisNames = ['(x-x0)/L','w/U']
plotTitle = 'Time Averaged z-velocity at vertical XZ planes'
figureName = 'UMean_W_Dir_x_00_04'
plotVar(UMean_00_04_Dirx, axisNames, noTitle, figureName, 3, U, 0, 4)

axisNames = ['(x-x0)/L','uMag/U']
plotTitle = 'Time Averaged velocity magnitude at vertical XZ planes'
figureName = 'UMean_mag_Dir_x_00_04'
plotVar(UMean_00_04_Dirx, axisNames, noTitle, figureName, 4, U, 0, 4)

## UMean Dir_z_00_04
axisNames = ['u/U', 'z/H']
plotTitle = 'Time Averaged x-velocity at vertical XZ planes'
figureName = 'UMean_U_Dir_z_00_04'
plotVar(UMean_00_04_Dirz, axisNames, noTitle, figureName, 1, U, 0, 4)

axisNames = ['v/U', 'z/H']
plotTitle = 'Time Averaged y-velocity at vertical XZ planes'
figureName = 'UMean_V_Dir_z_00_04'
plotVar(UMean_00_04_Dirz, axisNames, noTitle, figureName, 2, U, 0, 4)

axisNames = ['w/U', 'z/H']
plotTitle = 'Time Averaged z-velocity at vertical XZ planes'
figureName = 'UMean_W_Dir_z_00_04'
plotVar(UMean_00_04_Dirz, axisNames, noTitle, figureName, 3, U, 0, 4)

axisNames = ['uMag/U', 'z/H']
plotTitle = 'Time Averaged velocity magnitude at vertical XZ planes'
figureName = 'UMean_mag_Dir_z_00_04'
plotVar(UMean_00_04_Dirz, axisNames, noTitle, figureName, 4, U, 0, 4)

## lambVectorMean Dir_x_00_04
axisNames = ['(x-x0)/L','lambVectorMean [m/s2]']
plotTitle = 'Time Averaged Lamb Vector magnitude at vertical XZ planes'
figureName = 'lambVectorMean_mag_Dir_x_00_04'
plotVar(lambVectorMean_00_04_Dirx, axisNames, noTitle, figureName, 4, 1, 0, 4)

## lambVectorMean Dir_z_00_04
axisNames = ['lambVectorMean [m/s2]', 'z/H']
plotTitle = 'Time Averaged Lamb Vector magnitude at vertical XZ planes'
figureName = 'lambVectorMean_mag_Dir_z_00_04'
plotVar(lambVectorMean_00_04_Dirz, axisNames, noTitle, figureName, 4, 1, 0, 4)

## pMean Dir_x_00_04
axisNames = ['(x-x0)/L',r'(pL)/($\rho$ U)']
plotTitle = 'Time Averaged Pressure at vertical XZ planes'
figureName = 'pMean_Dir_x_00_04'
plotVar(pMean_00_04_Dirx, axisNames, noTitle, figureName, 1, L/(RHO*U), 0, 4)

## pMean Dir_z_00_04
axisNames = [r'(pL)/($\rho$ U)', 'z/H']
plotTitle = 'Time Averaged Pressure at vertical XZ planes'
figureName = 'pMean_Dir_z_00_04'
plotVar(pMean_00_04_Dirz, axisNames, noTitle, figureName, 1, L/(RHO*U), 0, 4)

## vorticity Dir_x_00_04
axisNames = ['(x-x0)/L','vorticity[1/s]']
plotTitle = 'Time Averaged vorticity magnitude at vertical XZ planes'
figureName = 'vorticity_Dir_x_00_04'
plotVar(vorticityMean_00_04_Dirx, axisNames, noTitle, figureName, 4, 1, 0, 4)

## vorticity Dir_z_00_04
axisNames = ['vorticity [1/s]', 'z/H']
plotTitle = 'Time Averaged vorticity magnitude at vertical XZ planes'
figureName = 'vorticity_Dir_z_00_04'
plotVar(vorticityMean_00_04_Dirz, axisNames, noTitle, figureName, 4, 1, 0, 4)

# =============================================================================
# Planes 5 -> 11
# Vertical Planes Varying the X axis from X = 0.25 to X = 0.50
# =============================================================================
## RMean Dir_y_05_11
axisNames = ['Rmag/U²', '(y-y0)/H']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude at vertical YZ planes'
figureName = 'RMean_mag_Dirx_05_11'
plotVar(RMean_05_11_Diry, axisNames, noTitle, figureName, 7, U**2, 5, 11)

## RMean Dir_z_05_11
axisNames = ['Rmag/U²', 'z/H']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude at vertical YZ planes'
figureName = 'RMean_mag_Dir_z_05_11'
plotVar(RMean_05_11_Dirz, axisNames, noTitle, figureName, 7, U**2, 5, 11)

## UMean Dir_y_05_11
axisNames = ['(y-y0)/H','u/U']
plotTitle = 'Time Averaged x-velocity at vertical YZ planes'
figureName = 'UMeanYZPlanes_U_Diry'
plotVar(UMean_05_11_Diry, axisNames, noTitle, figureName, 1, U, 5, 11)

axisNames = ['(y-y0)/H','v/U']
plotTitle = 'Time Averaged y-velocity at vertical YZ planes'
figureName = 'UMeanYZPlanes_V_Diry'
plotVar(UMean_05_11_Diry, axisNames, noTitle, figureName, 2, U, 5, 11)

axisNames = ['(y-y0)/H','w/U']
plotTitle = 'Time Averaged z-velocity at vertical YZ planes'
figureName = 'UMeanYZPlanes_W_Diry'
plotVar(UMean_05_11_Diry, axisNames, noTitle, figureName, 3, U, 5, 11)

axisNames = ['(y-y0)/H','uMag/U']
plotTitle = 'Time Averaged velocity magnitude at vertical YZ planes'
figureName = 'UMeanYZPlanes_mag_Diry'
plotVar(UMean_05_11_Diry, axisNames, noTitle, figureName, 4, U, 5, 11)

## UMean Dir_z_05_11
axisNames = ['u/U', 'z/H']
plotTitle = 'Time Averaged x-velocity at vertical YZ planes'
figureName = 'UMeanYZPlanes_U_Dirz'
plotVar(UMean_05_11_Dirz, axisNames, noTitle, figureName, 1, U, 5, 11)

axisNames = ['v/U', 'z/H']
plotTitle = 'Time Averaged y-velocity at vertical YZ planes'
figureName = 'UMeanYZPlanes_V_Dirz'
plotVar(UMean_05_11_Dirz, axisNames, noTitle, figureName, 2, U, 5, 11)

axisNames = ['w/U', 'z/H']
plotTitle = 'Time Averaged z-velocity at vertical YZ planes'
figureName = 'UMeanYZPlanes_W_Dirz'
plotVar(UMean_05_11_Dirz, axisNames, noTitle, figureName, 3, U, 5, 11)

axisNames = ['uMag/U', 'z/H']
plotTitle = 'Time Averaged velocity magnitude at vertical YZ planes'
figureName = 'UMeanYZPlanes_mag_Dirz'
plotVar(UMean_05_11_Dirz, axisNames, noTitle, figureName, 4, U, 5, 11)

## lambVectorMean Dir_y_05_11
axisNames = ['(x-x0)/L','lambVectorMean [m/s2]']
plotTitle = 'Time Averaged Lamb Vector magnitude at vertical YZ planes'
figureName = 'lambVectorMean_mag_Dir_y_05_11'
plotVar(lambVectorMean_05_11_Diry, axisNames, noTitle, figureName, 4, 1, 5, 11)

## lambVectorMean Dir_z_05_11
axisNames = ['lambVectorMean [m/s2]', 'z/H']
plotTitle = 'Time Averaged Lamb Vector magnitude at vertical YZ planes'
figureName = 'lambVectorMean_mag_Dir_z_05_11'
plotVar(lambVectorMean_05_11_Dirz, axisNames, noTitle, figureName, 4, 1, 5, 11)

## pMean Dir_y_05_11
axisNames = ['(x-x0)/L',r'(pL)/($\rho$ U)']
plotTitle = 'Time Averaged Pressure at vertical YZ planes'
figureName = 'pMean_Dir_y_05_11'
plotVar(pMean_05_11_Diry, axisNames, noTitle, figureName, 1, L/(RHO*U), 5, 11)

## pMean Dir_z_05_11
axisNames = [r'(pL)/($\rho$ U)', 'z/H']
plotTitle = 'Time Averaged Pressure at vertical YZ planes'
figureName = 'pMean_Dir_z_05_11'
plotVar(pMean_05_11_Dirz, axisNames, noTitle, figureName, 1, L/(RHO*U), 5, 11)

## vorticity Dir_y_05_11
axisNames = ['(x-x0)/L','vorticity[1/s]']
plotTitle = 'Time Averaged vorticity magnitude at vertical YZ planes'
figureName = 'vorticity_Dir_y_05_11'
plotVar(vorticityMean_05_11_Diry, axisNames, noTitle, figureName, 4, 1, 5, 11)

## vorticity Dir_z_05_11
axisNames = ['vorticity [1/s]', 'z/H']
plotTitle = 'Time Averaged vorticity magnitude at vertical YZ planes'
figureName = 'vorticity_Dir_z_05_11'
plotVar(vorticityMean_05_11_Dirz, axisNames, noTitle, figureName, 4, 1, 5, 11)


# =============================================================================
# Planes 12 -> 21
# Horizontal Planes Varying the Z axis from Z = 0 to Z = 0.10
# =============================================================================
## RMean Dir_x_12_21
axisNames = ['(x-x0)/L', 'Rmag/U²']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude at horizontal XY planes'
figureName = 'RMean_mag_Dir_x_12_21'
plotVar(RMean_12_21_Dirx, axisNames, noTitle, figureName, 7, U**2, 12, 21)

## RMean Dir_y_12_21
axisNames = ['(y-y0)/H', 'Rmag/U²']
plotTitle = 'Time Averaged Reynolds Stresses Magnitude at horizontal XY planes'
figureName = 'RMean_mag_Dir_y_12_21'
plotVar(RMean_12_21_Diry, axisNames, noTitle, figureName, 7, U**2, 12, 21)

## UMean Dir_x_12_21
axisNames = ['(x-x0)/L','u/U']
plotTitle = 'Time Averaged x-velocity at horizontal XY planes'
figureName = 'UMean_U_Dir_x_12_21'
plotVar(UMean_12_21_Dirx, axisNames, noTitle, figureName, 1, U, 12, 21)

axisNames = ['(x-x0)/L','v/U']
plotTitle = 'Time Averaged y-velocity at horizontal XY planes'
figureName = 'UMean_V_Dir_x_12_21'
plotVar(UMean_12_21_Dirx, axisNames, noTitle, figureName, 2, U, 12, 21)

axisNames = ['(x-x0)/L','w/U']
plotTitle = 'Time Averaged z-velocity at horizontal XY planes'
figureName = 'UMean_W_Dir_x_12_21'
plotVar(UMean_12_21_Dirx, axisNames, noTitle, figureName, 3, U, 12, 21)

axisNames = ['(x-x0)/L','uMag/U']
plotTitle = 'Time Averaged velocity magnitude at horizontal XY planes'
figureName = 'UMean_mag_Dir_x_12_21'
plotVar(UMean_12_21_Dirx, axisNames, noTitle, figureName, 4, U, 12, 21)

## UMean Dir_y_12_21
axisNames = ['(y-y0)/H','u/U']
plotTitle = 'Time Averaged x-velocity at horizontal XY planes'
figureName = 'UMean_U_Dir_y_12_21'
plotVar(UMean_12_21_Diry, axisNames, noTitle, figureName, 1, U, 12, 21)

axisNames = ['(y-y0)/H','v/U']
plotTitle = 'Time Averaged y-velocity at horizontal XY planes'
figureName = 'UMean_V_Dir_y_12_21'
plotVar(UMean_12_21_Diry, axisNames, noTitle, figureName, 2, U, 12, 21)

axisNames = ['(y-y0)/H','w/U']
plotTitle = 'Time Averaged z-velocity at horizontal XY planes'
figureName = 'UMean_W_Dir_y_12_21'
plotVar(UMean_12_21_Diry, axisNames, noTitle, figureName, 3, U, 12, 21)

axisNames = ['(y-y0)/H','uMag/U']
plotTitle = 'Time Averaged velocity magnitude at horizontal XY planes'
figureName = 'UMean_mag_Dir_y_12_21'
plotVar(UMean_12_21_Diry, axisNames, noTitle, figureName, 4, U, 12, 21)

## lambVectorMean Dir_y_12_21
axisNames = ['(x-x0)/L','lambVectorMean [m/s2]']
plotTitle = 'Time Averaged Lamb Vector magnitude at horizontal XY planes'
figureName = 'lambVectorMean_mag_Dir_y_12_21'
plotVar(lambVectorMean_12_21_Diry, axisNames, noTitle, figureName, 4, 1, 12, 21)

## lambVectorMean Dir_z_12_21
axisNames = ['lambVectorMean [m/s2]', 'z/H']
plotTitle = 'Time Averaged Lamb Vector magnitude at horizontal XY planes'
figureName = 'lambVectorMean_mag_Dir_z_12_21'
plotVar(lambVectorMean_12_21_Diry, axisNames, noTitle, figureName, 4, 1, 12, 21)

## pMean Dir_y_12_21
axisNames = ['(x-x0)/L',r'(pL)/($\rho$ U)']
plotTitle = 'Time Averaged Pressure at horizontal XY planes'
figureName = 'pMean_Dir_y_12_21'
plotVar(pMean_12_21_Diry, axisNames, noTitle, figureName, 1, L/(RHO*U), 12, 21)

## pMean Dir_z_12_21
axisNames = [r'(pL)/($\rho$ U)', 'z/H']
plotTitle = 'Time Averaged Pressure at horizontal XY planes'
figureName = 'pMean_Dir_z_12_21'
plotVar(pMean_12_21_Diry, axisNames, noTitle, figureName, 1, L/(RHO*U), 12, 21)

## vorticity Dir_y_12_21
axisNames = ['(x-x0)/L','vorticity[1/s]']
plotTitle = 'Time Averaged vorticity magnitude at horizontal XY planes'
figureName = 'vorticity_Dir_y_12_21'
plotVar(vorticityMean_12_21_Diry, axisNames, noTitle, figureName, 4, 1, 12, 21)

## vorticity Dir_z_12_21
axisNames = ['vorticity [1/s]', 'z/H']
plotTitle = 'Time Averaged vorticity magnitude at horizontal XY planes'
figureName = 'vorticity_Dir_z_12_21'
plotVar(vorticityMean_12_21_Diry, axisNames, noTitle, figureName, 4, 1, 12, 21)

# =============================================================================
# Validation Graph
# =============================================================================

## Figure 4
#fig4, ax4 = plt.subplots(figsize=(9,6), dpi=300)
#ax4.plot(literatureExp.iloc[:,0], literatureExp.iloc[:,1],'k.',
#         label='Experimental (Xiang et al., 2019)')
#ax4.plot(literatureLES.iloc[:,0], literatureLES.iloc[:,1],'--',
#         label='Numerical (Xiang et al., 2019)')
#l, caps, c = plt.errorbar(errorbarcsv.iloc[:,1], errorbarcsv.u/U, errorbarcsv.iloc[:,9]/U,
#             elinewidth = 2, capsize = 5, capthick = 1,
#             marker = 'o', markevery=5, errorevery = 5,
#             uplims = True, lolims = True, 
#             lw=1.5, aa = True, label='Presented Model')
#
#for cap in caps:
#    cap.set_marker("_")
#
#ax4.legend(loc='best',fontsize='x-large')
#   
##ax4.set_title('Time Averaged x-velocity at 0.6H'
##             ,fontsize='xx-large')
#
#plt.grid()
#plt.autoscale(enable=True, tight=True)
#plt.xlabel('(y-y0)/H',fontsize='x-large')
#plt.ylabel('u/U',fontsize='x-large')
#plt.savefig('preTreatment/results/Plot/validationWithErrorbar.jpg', bbox_inches='tight')

# Figure 4
fig4, ax4 = plt.subplots(figsize=(9,6), dpi=300)
ax4.plot(literatureExp.iloc[:,0], literatureExp.iloc[:,1],'k.',
         label='Experimental (Xiang et al., 2019)')
ax4.plot(literatureLES.iloc[:,0], literatureLES.iloc[:,1],'--',
         label='Numerical (Xiang et al., 2019)')
ax4.plot(fig4aOur.iloc[:,0], fig4aOur.u,
         label='Presented Model')

ax4.legend(loc='best',fontsize='x-large')

#ax4.set_title('Time Averaged x-velocity at 0.6H'
#             ,fontsize='xx-large')

plt.grid()
plt.autoscale(enable=True, tight=True)
plt.xlabel('(y-y0)/H',fontsize='x-large')
plt.ylabel('u/U',fontsize='x-large')
plt.savefig('preTreatment/results/Plot/validation.jpg', bbox_inches='tight')

# Mass Decay
figm, axm = plt.subplots(figsize=(9,6), dpi=300)
axm.plot(tracerData.time,modelmass,label='Fitted Curve',color='r')
axm.plot(tracerData.time,tracerData.tracerVol,label='Numerical')

axm.legend(loc='best',fontsize='x-large')

#axm.set_title('Mass Ejection from Groyne Field Volume'
#             ,fontsize='xx-large')

at = AnchoredText('C(t)=$C_{0}$$e^{-t/Td}$\n$k_{ajusted}$ = %.4f' % k,
                  prop=dict(size=15), frameon=True,
                  loc='lower left')
axm.add_artist(at)

#axm.set_yscale('log')
plt.autoscale(enable=True, tight=True)
plt.grid()
plt.xlabel('t [s]',fontsize='x-large')
plt.ylabel('Concentration [non-dimensional]',fontsize='x-large')
plt.savefig('preTreatment/results/Plot/massDecay.jpg', bbox_inches='tight')

# Mass Decay semilogy
figm, axm = plt.subplots(figsize=(9,6), dpi=300)
axm.semilogy(tracerData.time,modelmass,label='Fitted Curve',color='r')
axm.semilogy(tracerData.time,tracerData.tracerVol,label='Numerical')

axm.legend(loc='best',fontsize='x-large')

#axm.set_title('Mass Ejection from Groyne Field Volume'
#             ,fontsize='xx-large')

at = AnchoredText('C(t)=$C_{0}$$e^{-t/Td}$\n$k_{ajusted}$ = %.4f' % k,
                  prop=dict(size=15), frameon=True,
                  loc='lower left')
axm.add_artist(at)

axm.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
axm.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%.1f'))
plt.autoscale(enable=True, tight=True)
plt.grid()
plt.xlabel('t [s]',fontsize='x-large')
plt.ylabel('Concentration [non-dimensional]',fontsize='x-large')
plt.savefig('preTreatment/results/Plot/massDecaySemiLogY.jpg', bbox_inches='tight')

del figm, axm, at, fig4, ax4, axisNames, noTitle, figureName , plotTitle

# Mass Decay per Part
figm, axm = plt.subplots(figsize=(9,6), dpi=300)
for ii in regions:
    axm.plot(interfaceTracer[ii].time,interfaceTracer[ii].tracer, label=ii)

axm.legend(loc='best',fontsize='x-large')

axm.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
axm.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%.1f'))
plt.autoscale(enable=True, tight=True)
plt.grid()
plt.xlabel('t [s]',fontsize='x-large')
plt.ylabel('Concentration [non-dimensional]',fontsize='x-large')
plt.savefig('preTreatment/results/Plot/massDecayPerPart.jpg', bbox_inches='tight')

# Mass Decay per Part semilog y
figm, axm = plt.subplots(figsize=(9,6), dpi=300)
for ii in regions:
    axm.semilogy(interfaceTracer[ii].time,interfaceTracer[ii].tracer, label=ii)

axm.legend(loc='best',fontsize='x-large')

axm.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
axm.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%.3f'))
plt.autoscale(enable=True, tight=True)
plt.grid()
plt.xlabel('t [s]',fontsize='x-large')
plt.ylabel('Concentration [non-dimensional]',fontsize='x-large')
plt.savefig('preTreatment/results/Plot/massDecayPerPartSemiLogY.jpg', bbox_inches='tight')


