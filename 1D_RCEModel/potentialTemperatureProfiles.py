import numpy as np
from matplotlib import pyplot as plt
import metpy.calc as calc
from metpy.units import units
import climt

def potentialTemperature_verticalProfile(state):
  potentialTemperatures = []
  for i in range(28):
    pressure = np.array(state['air_pressure_on_interface_levels']).flatten()[i]
    pressure  = units.Quantity(pressure,"pascal")
    temperature = np.array(state['air_temperature']).flatten()[i]
    temperature = units.Quantity(temperature,"kelvin")
    potentialTemperatures.append(calc.potential_temperature(pressure,temperature))
  potentialTemperatures = [i.magnitude for i in potentialTemperatures]
  
  # Graphing Theta.
  fig = plt.figure()
  plt.plot(np.array(state['air_pressure_on_interface_levels']).flatten()[:28],potentialTemperatures)
  plt.xlabel("Pressure (Pa)")
  plt.ylabel("Potential Temperature (K)")
  plt.gca().invert_xaxis()
  plt.savefig("graphs/potentialTemperatureProfile.png")
  plt.close()
  return potentialTemperatures
