from climt import (RRTMGLongwave, RRTMGShortwave,
	SlabSurface, SimplePhysics, 
	DryConvectiveAdjustment, get_default_state,
	get_grid, Frierson06LongwaveOpticalDepth)
from sympl import (AdamsBashforth, 
	initialize_numpy_arrays_with_properties)
import numpy as np
import datetime
import csv
from matplotlib import pyplot as plt

from setupMain import *

def runningModel():
	# Importing components
	rad_sw = RRTMGShortwave()
	rad_lw = RRTMGLongwave()
	surface = SlabSurface()
	time_stepper = AdamsBashforth([rad_sw, rad_lw, surface])
	
	# Setting up default state
	timestep = datetime.timedelta(hours = 4)
	grid = get_grid(nx=1, ny=1, nz=60)
	state = get_default_state([rad_lw,rad_sw,surface], grid_state = grid)
	albedo = 0.3

	# Setting up model constraints and importing atmospheric constituent data
	diagnostics, state = time_stepper(state,timestep)
	state['surface_temperature'][:] = 250
	state['air_temperature'][:] = 230
	state['zenith_angle'].values[:] = np.pi/3
	state['surface_albedo_for_direct_near_infrared'].values[:] = albedo * 1.5
	state['ocean_mixed_layer_thickness'].values[:] = 40.
	state['surface_albedo_for_direct_shortwave'][:] = albedo
	state['surface_albedo_for_diffuse_shortwave'][:] = np.sin((np.pi)/3) * albedo
	state['area_type'][:] = 'sea'
	tp_profiles = np.load('../thermodynamic_profiles.npz')
	mol_profiles = np.load('../molecule_profiles.npz')
	state['air_pressure'].values[:] = tp_profiles['air_pressure'][:, np.newaxis, np.newaxis]
	state['air_pressure_on_interface_levels'].values[:] = tp_profiles['interface_pressures'][:, np.newaxis, np.newaxis]
	state['specific_humidity'].values[:] = mol_profiles['specific_humidity'][:, np.newaxis, np.newaxis]*1e-3
	state['mole_fraction_of_carbon_dioxide_in_air'].values[:] = mol_profiles['carbon_dioxide'][:, np.newaxis, np.newaxis]
	state['mole_fraction_of_ozone_in_air'].values[:] = mol_profiles['ozone'][:, np.newaxis, np.newaxis]
	state.update()

	# Model variables
	diff_acceptable = 5.
	airPressure_vertCoord = np.array(state['air_pressure_on_interface_levels']).flatten()
	time = datetime.datetime(2020,1,1,0,0,0) # In months (Add 1/168 for each timedelta jump)
	stop = False

	counter = 0
	errorMargin = 0.5

	# Running to equilibrium
	while stop == False:
		diagnostics, state = time_stepper(state,timestep)
		state.update(diagnostics)
		counter += 1
		time = time + timestep

		if counter % 42*4 == 0:
			print(counter)
			print(net_energy_level_in_column(state,diagnostics,diff_acceptable)[0])
			
		if counter % 500 == 0:
			print("AIR TEMPERATURE")
			print(np.array(state['air_temperature'][:]).flatten())
			print("\n LW NET FLUX")
			print(np.array(state['upwelling_longwave_flux_in_air'][:] - state['downwelling_longwave_flux_in_air'][:]).flatten())
			print("\n SW NET FLUX")
			print(np.array(state['upwelling_shortwave_flux_in_air'][:] - state['downwelling_shortwave_flux_in_air'][:]).flatten())
			print("\n SURFACE TEMPERATURE")
			print(state['surface_temperature'])
			print("\n SURFACE FLUXES")
			print((np.array(state['surface_upward_latent_heat_flux'] + state['surface_upward_sensible_heat_flux']).flatten())[0])
			print("\n SW UP FLUX")
			print(np.array(state['upwelling_shortwave_flux_in_air'][:]).flatten())
			
		# Checking stopping criteria
		if (abs(net_energy_level_in_column(state,diagnostics,diff_acceptable)[0]) < errorMargin and counter > 1500):
			stop = True
	
	# Calculating output quantities
	timeTaken = time - datetime.datetime(2020,1,1,0,0,0)
	lwFluxNet, lwFluxUp, lwFluxDown = netFlux(state)
	swFluxNet = np.array(diagnostics['upwelling_shortwave_flux_in_air'] - 
		diagnostics['downwelling_shortwave_flux_in_air']).flatten()
	sw_heatRate = np.array(diagnostics['air_temperature_tendency_from_shortwave']).flatten()
	lw_heatRate = np.array(diagnostics['air_temperature_tendency_from_longwave']).flatten()
	airTemperatureProf = (np.array(state['air_temperature'])).flatten()
	airPressure_vertCoord = np.array(state['air_pressure_on_interface_levels']).flatten()
	interface_airPressure_vertCoord = np.array(state['air_pressure']).flatten()
	olr = (np.array(diagnostics['upwelling_longwave_flux_in_air'][-1]).flatten())[0]

	print("AIR TEMPERATURE")
	print(np.array(state['air_temperature'][:]).flatten())
	print("\n LW NET FLUX")
	print(np.array(state['upwelling_longwave_flux_in_air'][:] - state['downwelling_longwave_flux_in_air'][:]).flatten())
	print("\n SW NET FLUX")
	print(np.array(state['upwelling_shortwave_flux_in_air'][:] - state['downwelling_shortwave_flux_in_air'][:]).flatten())
	print("\n SURFACE TEMPERATURE")
	print(state['surface_temperature'])
	print("\n SURFACE FLUXES")
	print((np.array(state['surface_upward_latent_heat_flux'] + state['surface_upward_sensible_heat_flux']).flatten())[0])
	print("\n SW UP FLUX")
	print(np.array(state['upwelling_shortwave_flux_in_air'][:]).flatten())

	return state, olr, timeTaken, olrs, netEn, surfT, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord

def output_to_csv(timeTaken, olrs, netEn, surfT, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord):
	
	with open('output_runModel/equilibrium.csv', mode='w') as equilibriumCSV:
		equilibriumWriter = csv.writer(equilibriumCSV)
		equilibriumWriter.writerow(lwFluxNet)
		equilibriumWriter.writerow(swFluxNet)
		equilibriumWriter.writerow(sw_heatRate)
		equilibriumWriter.writerow(lw_heatRate)
		equilibriumWriter.writerow(airTemperatureProf)
		equilibriumWriter.writerow(str(timeTaken))
		equilibriumWriter.writerow(interface_airPressure_vertCoord)
		equilibriumWriter.writerow(airPressure_vertCoord)
	
	return 0.

def main():
	state, olr, timeTaken, olrs, netEn, surfT, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord = runningModel()
	output_to_csv(timeTaken, olrs , netEn, surfT, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord)
	print(swFluxNet)
	print(olr)
	print(state['surface_temperature'])

if __name__ == "__main__":
	main()
