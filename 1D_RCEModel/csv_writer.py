import csv
import numpy as np

def output_to_csv(timeTaken, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, convection_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord):
	print("ABC")
	with open('output_runModel/equilibrium.csv', mode='w') as equilibriumCSV:
		equilibriumWriter = csv.writer(equilibriumCSV)
		equilibriumWriter.writerow(lwFluxNet)
		equilibriumWriter.writerow(swFluxNet)
		equilibriumWriter.writerow(sw_heatRate)
		equilibriumWriter.writerow(lw_heatRate)
		equilibriumWriter.writerow(convection_heatRate)
		equilibriumWriter.writerow(airTemperatureProf)
		equilibriumWriter.writerow(str(timeTaken))
		equilibriumWriter.writerow(interface_airPressure_vertCoord)
		equilibriumWriter.writerow(airPressure_vertCoord)
	
	return 0.