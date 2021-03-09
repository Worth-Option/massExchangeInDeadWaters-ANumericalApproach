#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  mass.py
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
Mass quantities are analysed in two ways: by tracer volume and y-velocity
"""

# Libraries
from datetime import datetime
import numpy as np
import pandas as pd
import openpyxl
from scipy.optimize import curve_fit


# Extracting date for report
now = datetime.now()
today = now.strftime("%d/%m/%Y %H:%M:%S")

# Define Fitting Function
def model(x, td):
    """
    First Order Mass Decay Equation
    """
    return np.exp(-x/td)

td, pcov = curve_fit(model, tracerData.time, tracerData.tracerVol, p0=(40),
                     maxfev=5000)

k = W / (td * U)

modelmass = model(tracerData.time, td)

tdExp = massLiterature.iloc[1,1]

tdRelError = ((td - tdExp)/tdExp)*100
tdAbsError = tdExp - td

kexp = W / (tdExp * U) # Non-dimensional experimental value
kRelError = ((k - kexp)/kexp)*100
kAbsError = kexp - k

# Mass as function of velocity
E = Eraw.absVelInt.mean()

tdvel = W/E
kvel = W / (tdvel * U)

# Mass Summary
file = open("preTreatment/results/massExchange.txt","w")
file.write("Mass Exchange Values (Simulated - Tracer)\n")
file.write("ktracer = %.4f\n" %k)
file.write("Mean Residence Time = %.2f\n---\n" %td)
file.write("Mass Exchange Values (Simulated - Interface Velocity)\n")
file.write("kvelocity = %.4f\n" %kvel)
file.write("Mean Residence Time = %.2f\n---\n" %tdvel)
file.write("Mass Exchange Values (Xiang)\n")
file.write("kexp = %.4f\n" %kexp)
file.write("Mean Residence Time = %.2f\n---\n" %tdExp)
file.write("Error analysis\n")
file.write("Relative error\n")
file.write("\tError = (Simulated.our - Xiang)/(Xiang)\n")
file.write("MRT = %.2f %%\n" %tdRelError)
file.write("k = %.2f %%\n" %kRelError)
file.write("Absolute error\n")
file.write("MRT = %.2f\n" %tdAbsError)
file.write("k = %.2f\n" %kAbsError)
file.write("---\nData analysed in {} (GMT-4)".format(today))
file.close()

# Construct mass dataFrame
tracerDataExport = tracerData
tracerDataExport['modelled'] = modelmass
colNames = ['Time','Numerical','Modelled']
tracerDataExport.columns = colNames

tracerDataExport.to_csv('preTreatment/results/CSV/tracerData.csv')
with pd.ExcelWriter('preTreatment/results/Excel/tracerData.xlsx',
                    engine="openpyxl", mode='w') as writer:
    for df_name, df in tracerDataExport.items():
        df.to_excel(writer, sheet_name=df_name, index=False)
        
del file, now, today
