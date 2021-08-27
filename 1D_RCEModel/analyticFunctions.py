import os
import numpy as np

def surf_airBdry_tempDiff(state):
  	return (state['surface_temperature'] - state['air_temperature'])[0][0][0]

def radiating_pressure(state,diagnostics,diff_acceptable):
	upFlux = np.array(diagnostics['upwelling_longwave_flux_in_air']).flatten()
	int_level = 0
	for i in range(1,29):
		if abs(upFlux[i]-upFlux[i-1]) < diff_acceptable:
			int_level = i
			break
		else:
			int_level = 29
	return (np.array(state['air_pressure_on_interface_levels']).flatten())[int_level],int_level

"""def radiating_pressure(state,diff_acceptable):
	upFlux = np.array(state['upwelling_longwave_flux_in_air']).flatten()
	int_level = 0
	for i in range(1,29):
		if abs(upFlux[i]-upFlux[i-1]) < diff_acceptable:
			int_level = i
			break
		else:
			int_level = 29
	return (np.array(state['air_pressure_on_interface_levels']).flatten())[int_level],int_level"""

def cleaningUp():
	CSVs = 'output_runModel'
	graphs = 'graphs'
	foldersMain = [CSVs, graphs]
	for item in foldersMain:
		for file in os.listdir(item):
			os.remove(os.path.join(item,file))
	return 0.