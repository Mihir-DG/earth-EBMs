import csv
from matplotlib import pyplot as plt 
import numpy as np
import matplotlib.ticker as ticker

dataArr = []
with open('output_runModel/equilibrium.csv', 'r') as equilibriumFile:
	csvRead = csv.reader(equilibriumFile)
	for row in csvRead:
		dataArr.append(row)

dataArr =  [ele for ele in dataArr if ele != []] 
lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord = dataArr[0],dataArr[1],dataArr[2], dataArr[3], dataArr[4], dataArr[6], dataArr[7]
airPressure_vertCoord = [round((float(ele)/100),0) for ele in airPressure_vertCoord] # Conversion to mbar
interface_airPressure_vertCoord = [round((float(ele)/100),0) for ele in interface_airPressure_vertCoord]
timeTaken = ''.join(dataArr[5])

fig = plt.figure(figsize=(12,12))

# SHORTWAVE FLUX DIVERGENCE

swFluxNet = [round(float(ele),2) for ele in swFluxNet]
ax = fig.add_subplot(2,2,1)
ax.set_yscale('log')
ax.yaxis.set_major_locator(ticker.MultipleLocator(6))
ax.yaxis.set_ticks(np.linspace(1000,10,6))
ax.axes.invert_yaxis()
ax.set_ylim(1e3, 5.)
ax.set_xticks(np.linspace(-125,-245,7))
ax.plot(swFluxNet,airPressure_vertCoord,'-o')
ax.set_xlabel("A - Shortwave Flux Divergence (" + r'W/m$^2$' + ")")
ax.set_ylabel("Pressure (mbar)")
ax.grid()
ax.set_yticklabels(np.linspace(1000,10,6))

# LONGWAVE FLUX DIVERGENCE

lwFluxNet = [round(float(ele),2) for ele in lwFluxNet]
ax = fig.add_subplot(2,2,2)
ax.set_yscale('log')
ax.yaxis.set_major_locator(ticker.MultipleLocator(6))
ax.yaxis.set_ticks(np.linspace(1000,10,6))
ax.axes.invert_yaxis()
ax.set_ylim(1e3, 5.)
ax.set_xticks(np.linspace(125,245,7))
ax.plot(lwFluxNet,airPressure_vertCoord,'-o')
ax.set_xlabel("B - Longwave Flux Divergence ("+ r'W/m$^2$' + ")")
ax.set_ylabel("Pressure (mbar)")
ax.grid()
ax.set_yticklabels(np.linspace(1000,10,6))

# HEATING RATES

sw_heatRate = [round(float(ele),2) for ele in sw_heatRate]
lw_heatRate = [round(float(ele),2) for ele in lw_heatRate]
ax = fig.add_subplot(2,2,3)
ax.set_yscale('log')
ax.yaxis.set_major_locator(ticker.MultipleLocator(6))
ax.yaxis.set_ticks(np.linspace(1000,10,6))
ax.axes.invert_yaxis()
ax.set_ylim(1e3, 5.)
ax.set_xticks(np.linspace(-30,30,13))
ax.plot(sw_heatRate,interface_airPressure_vertCoord,'-o',color = "orange", label = "SW")
ax.plot(lw_heatRate,interface_airPressure_vertCoord,'-o', label = "LW")
ax.plot((np.array(sw_heatRate).flatten() + np.array(lw_heatRate).flatten()),
	interface_airPressure_vertCoord, '--', color='green', label = 'Net')
ax.set_xlabel("C - Heating Rates (K)")
ax.legend(loc='upper right')
ax.set_ylabel("Pressure (mbar)")
ax.grid()
ax.set_yticklabels(np.linspace(1000,10,6))

# AIR TEMPERATURE

airTemperatureProf = [round(float(ele),2) for ele in airTemperatureProf]
ax = fig.add_subplot(2,2,4)
ax.set_yscale('log')
ax.yaxis.set_major_locator(ticker.MultipleLocator(6))
ax.yaxis.set_ticks(np.linspace(1000,10,6))
ax.axes.invert_yaxis()
ax.set_ylim(1e3, 5.)
ax.set_xticks(np.linspace(200,305,6))
ax.plot(airTemperatureProf,interface_airPressure_vertCoord, '-o')
ax.set_xlabel("D - Air Temperature (K)")
ax.set_ylabel("Pressure (mbar)")
ax.grid()
ax.set_yticklabels(np.linspace(1000,10,6))

plt.savefig("../graphs/RadEq.png")