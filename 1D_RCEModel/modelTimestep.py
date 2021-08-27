from sympl import (
    AdamsBashforth, PlotFunctionMonitor)
from climt import (
    RRTMGLongwave, RRTMGShortwave,
    EmanuelConvection,
    SimplePhysics, DryConvectiveAdjustment,
    SlabSurface, get_grid,
    get_default_state)
import datetime
import numpy as np
import csv
import sympl
from datetime import timedelta
import matplotlib.pyplot as plt
import metpy.calc as calc
import os
from metpy.units import units

from stoppingCriteria_fn import *
from analyticFunctions import *
from fluxDivergence_fns import *

def runningModel():
  # Initialize components
  sw = RRTMGShortwave()
  lw = RRTMGLongwave()
  surface = SlabSurface()
  #convectionScheme = EmanuelConvection()
  boundary_layer = SimplePhysics(
      use_external_surface_specific_humidity=True)
  convection_lapseRateAdjustment = DryConvectiveAdjustment()
  time_stepper = AdamsBashforth([lw, sw, surface])
  
  # Set up model state.
  timestep = timedelta(hours=1)
  grid = get_grid(nx=1, ny=1, nz=60)  
  state = get_default_state([lw, sw, surface,
    boundary_layer, convection_lapseRateAdjustment], grid_state=grid)
  albedo = 0.3
# ------ HOLD CURRENT ALBEDO VALUES --> OUTPUTS PLANETARY ALBEDO ~ 0.3
# ------ CURRENT BEST VALUE: surfT = 255, airT = 225 ==> final surfT = 278, olr = 280 - 18 = 262, albedo = 0.29
  # Importing atmospheric constituent data and updating state
  diagnostics, state = time_stepper(state,timestep)
  state['surface_temperature'][:] = 275
  #print(state['air_temperature'][:])
  state['air_temperature'][:] = 250
  state['zenith_angle'].values[:] = np.pi/3
  state['surface_albedo_for_direct_near_infrared'].values[:] = albedo * 1.5
  state['ocean_mixed_layer_thickness'].values[:] = 40.
  state['surface_albedo_for_direct_shortwave'][:] = albedo
  state['surface_albedo_for_diffuse_shortwave'][:] = np.cos((np.pi)/3) * albedo
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
  radPres = radiating_pressure(state,diagnostics,diff_acceptable)
  radHt = radPres[1]

  #Creates list for assorted 0d output vars.
  netEn = [(net_energy_level_in_column(state,diagnostics,diff_acceptable))[0]]
  bdry_tempDiff = [surf_airBdry_tempDiff(state)]
  olrs = [(np.array(diagnostics['upwelling_longwave_flux_in_air']).flatten())[-1]]
  surfT = [(np.array(state['surface_temperature']).flatten())[0]]
    
  counter = 0
  errorMargin = .1

  while stop == False:
    # Updating TendencyComponents
    diagnostics, state = time_stepper(state,timestep)
    state.update(diagnostics)
    counter += 1
    time = time + timestep

    # Updating boundary layer
    boundaryDiagnostics, new_state = boundary_layer(state, timestep)
    state.update(new_state)
    state.update(boundaryDiagnostics)

    #Updating convective adjustment
    convectiveAdjustmentDiagnostics, new_state = convection_lapseRateAdjustment(state, timestep)
    state.update(new_state)
    state.update(convectiveAdjustmentDiagnostics)

    state['eastward_wind'][:] = 5.
    state.update()

    # Updating appropriate quantities every month
    if counter % 42*4 == 0:
      netEn.append((net_energy_level_in_column(state,diagnostics,diff_acceptable))[0])
      bdry_tempDiff.append(surf_airBdry_tempDiff(state))
      olrs.append((np.array(diagnostics['upwelling_longwave_flux_in_air']).flatten())[-1])
      surfT.append((np.array(state['surface_temperature']).flatten())[0])
      print(counter)
      print(net_energy_level_in_column(state,diagnostics,diff_acceptable)[0])
      #print((net_energy_level_in_column(state,diagnostics,diff_acceptable))[0])
      #print(time - datetime.datetime(2020,1,1,0,0,0))
      #print("\n")
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
    if (abs(net_energy_level_in_column(state,diagnostics,diff_acceptable)[0]) < errorMargin and counter > 2500):
    #if len(netEn) > 4:
      #if abs(netEn[-1] - netEn[-2]) < errorMargin:
      stop = True
    
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

  return state, olr, timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord