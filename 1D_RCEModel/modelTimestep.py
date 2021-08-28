from sympl import (
    AdamsBashforth, get_constant)
from climt import (
    RRTMGLongwave, RRTMGShortwave,
    EmanuelConvection,
    SimplePhysics, DryConvectiveAdjustment,
    SlabSurface, get_grid,
    get_default_state)
import numpy as np
import csv
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import metpy.calc as calc
import os
from metpy.units import units

from stoppingCriteria_fn import *


def runningModel():
    # Initialize components
    sw = RRTMGShortwave()
    lw = RRTMGLongwave()
    surface = SlabSurface()
    convection = EmanuelConvection()
    boundary_layer = SimplePhysics()
    dryConvection = DryConvectiveAdjustment()

    # Set up model state.
    timestep = timedelta(minutes=100)
    grid = get_grid(nx=1, ny=1, nz=60)
    state = get_default_state([lw, sw, surface,
    boundary_layer, convection, dryConvection], grid_state=grid)
    albedo = 0.25
    # ------ HOLD CURRENT ALBEDO VALUES --> OUTPUTS PLANETARY ALBEDO ~ 0.3
    # ------ CURRENT BEST VALUE: surfT = 255, airT = 225 ==> final surfT = 278, olr = 280 - 18 = 262, albedo = 0.29
    # Importing atmospheric constituent data and updating state
    state['surface_temperature'][:] = 290
    state['air_temperature'][:] = 260
    state['zenith_angle'].values[:] = 76/90*np.pi/2
    state['surface_albedo_for_direct_near_infrared'].values[:] = albedo * 1.5
    state['ocean_mixed_layer_thickness'].values[:] = 1
    state['surface_albedo_for_direct_shortwave'][:] = albedo
    state['surface_albedo_for_diffuse_shortwave'][:] = np.sin((np.pi)/3) * albedo
    state['area_type'][:] = 'sea'
    tp_profiles = np.load('../thermodynamic_profiles.npz')
    mol_profiles = np.load('../molecule_profiles.npz')
    state['air_pressure'].values[:] = tp_profiles['air_pressure'][:, np.newaxis, np.newaxis]
    #state['air_temperature'].values = tp_profiles['air_temperature'][:, np.newaxis, np.newaxis]
    state['air_pressure_on_interface_levels'].values[:] = tp_profiles['interface_pressures'][:, np.newaxis, np.newaxis]
    state['specific_humidity'].values[:] = mol_profiles['specific_humidity'][:, np.newaxis, np.newaxis]*1e-3
    state['mole_fraction_of_carbon_dioxide_in_air'].values[:] = mol_profiles['carbon_dioxide'][:, np.newaxis, np.newaxis]
    state['mole_fraction_of_ozone_in_air'].values[:] = mol_profiles['ozone'][:, np.newaxis, np.newaxis]
    state.update()

    # Setting up clouds
    """p = state['air_pressure'][:]
    p_interface = state['air_pressure_on_interface_levels'][:]
    T = state['air_temperature'][:]
    R = get_constant('gas_constant_of_dry_air', 'J kg^-1 K^-1')
    g = get_constant('gravitational_acceleration', 'm s^-2')
    density = p / (R * T)
    dz = - np.diff(p_interface, axis=0) / (density * g)  # [m]
    z = np.cumsum(dz) * 10**-3  # [km]
    ice_density = 0.5 * 10**-3  # [kg m^-3]
    cloud_base = 10  # [km]
    cloud_top = 15  # [km]
    cloud_loc = np.where((z > cloud_base) & (z < cloud_top))
    area_fraction = 1
    mass_ice_array = area_fraction * ice_density * dz
    state['mass_content_of_cloud_ice_in_atmosphere_layer'][:] = mass_ice_array
    state['cloud_area_fraction_in_atmosphere_layer'][cloud_loc] = area_fraction
    state.update()"""

    time_stepper = AdamsBashforth([lw, sw, surface, convection])

    # Model variables
    diff_acceptable = 0.5
    airPressure_vertCoord = np.array(state['air_pressure_on_interface_levels']).flatten()
    time = datetime.datetime(2020,1,1,0,0,0) # In months (Add 1/168 for each timedelta jump)
    stop = False
    counter = 0
    errorMargin = 4
    #print(state['specific_humidity'][:])
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
        convectiveAdjustmentDiagnostics, new_state = dryConvection(state, timestep)
        state.update(new_state)
        state.update(convectiveAdjustmentDiagnostics)

        state['eastward_wind'][:] = 3
        state.update()

        # Updating appropriate quantities every month
        if counter % 42*4 == 0:
          print(counter)
          print(net_energy_level_in_column(state,diagnostics,diff_acceptable))
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
          print(np.array(state['upwelling_shortwave_flux_in_air'][:]).flatten()[-1])
          print("\n SW DOWN FLUX")
          print(np.array(state['downwelling_shortwave_flux_in_air'][:]).flatten()[-1])
        
        # Checking stopping criteria
        if (abs(net_energy_level_in_column(state,diagnostics,diff_acceptable)) < errorMargin):
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
    lwFluxNet = np.array(diagnostics['upwelling_longwave_flux_in_air'] - 
      diagnostics['downwelling_longwave_flux_in_air']).flatten()
    swFluxNet = np.array(diagnostics['upwelling_shortwave_flux_in_air'] - 
      diagnostics['downwelling_shortwave_flux_in_air']).flatten()
    sw_heatRate = np.array(diagnostics['air_temperature_tendency_from_shortwave']).flatten()
    lw_heatRate = np.array(diagnostics['air_temperature_tendency_from_longwave']).flatten()
    airTemperatureProf = (np.array(state['air_temperature'])).flatten()
    airPressure_vertCoord = np.array(state['air_pressure_on_interface_levels']).flatten()
    interface_airPressure_vertCoord = np.array(state['air_pressure']).flatten()
    olr = (np.array(diagnostics['upwelling_longwave_flux_in_air'][-1]).flatten())[0]
    convection_heatRate = np.array(diagnostics['air_temperature_tendency_from_convection']).flatten()

    return state, olr, timeTaken, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, convection_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord