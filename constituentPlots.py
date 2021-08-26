from climt import (RRTMGLongwave, RRTMGShortwave,
	SlabSurface, SimplePhysics, 
	DryConvectiveAdjustment, get_default_state,
	get_grid, Frierson06LongwaveOpticalDepth)
from sympl import (AdamsBashforth, 
	initialize_numpy_arrays_with_properties)
import numpy as np
import datetime
import csv
from matplotlib import ticker as ticker
from matplotlib import pyplot as plt

rad_sw = RRTMGShortwave()
rad_lw = RRTMGLongwave()
surface = SlabSurface()

timestep = datetime.timedelta(hours=80)
grid = get_grid(nx=1, ny=1, nz=60)
state = get_default_state([rad_lw,rad_sw,surface], grid_state = grid)
time_stepper = AdamsBashforth([rad_sw, rad_lw, surface])

tp_profiles = np.load('thermodynamic_profiles.npz')
mol_profiles = np.load('molecule_profiles.npz')
state['air_pressure'].values[:] = tp_profiles['air_pressure'][:, np.newaxis, np.newaxis]
state['mole_fraction_of_carbon_dioxide_in_air'].values[:] = mol_profiles['carbon_dioxide'][:, np.newaxis, np.newaxis]
state['mole_fraction_of_ozone_in_air'].values[:] = mol_profiles['ozone'][:, np.newaxis, np.newaxis]
state.update()

specHumidity = list(state['specific_humidity'].values[:].flatten())
air_pressure = list(state['air_pressure'].values[:].flatten())
air_pressure = [ele * 1e-2 for ele in air_pressure]

co2 = list(state['mole_fraction_of_carbon_dioxide_in_air'].values[:].flatten())
o3 = list(state['mole_fraction_of_ozone_in_air'].values[:].flatten())

fig = plt.figure(figsize=(12,6),dpi=1000)

ax = fig.add_subplot(1,2,1)
ax.set_yscale('log')
ax.axes.invert_yaxis()
ax.plot(o3,air_pressure,'-o')
ax.set_xlabel("A - " + r'$O_3$' + " Distribution (Mole Fraction)")
ax.set_ylabel("Pressure (mbar)")
ax.grid()

ax = fig.add_subplot(1,2,2)
ax.set_yscale('log')
ax.axes.invert_yaxis()
ax.plot(co2,air_pressure,'-o')
ax.set_xlabel("B - " + r'$CO_2$' + " Distribution (Mole Fraction)")
ax.set_ylabel("Pressure (mbar)")
ax.grid()

plt.savefig("graphs/constituents")