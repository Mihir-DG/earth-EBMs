import sympl
from matplotlib import pyplot as plt
import numpy as np
import climt

radiation1 = climt.GrayLongwaveRadiation()
grid = climt.get_grid(nx=None,ny=None,nz=0)

state = climt.get_default_state([radiation1],grid_state=grid)

surfT = np.array(state['surface_temperature']).flatten()[0]
sigma = 5.68*10**-8
upFlux = sigma * surfT**4
albedo = 0.29

# Albedo vs emissivity
x = np.linspace(0,1,100)
y = 1-((4*upFlux)/1367.6)*x
plt.ylabel('Albedo')
plt.xlabel('Epsilon (Emissivity)')
plt.plot(x,y)
plt.savefig("epsilonValbedo.png")

# Temperature vs emissivity
fig = plt.figure()
x = np.linspace(0.01,1,100) #Emissivity
t = (1367.6*(1-albedo)/(4 * sigma * x))**0.25
plt.xlabel("Epsilon (Emissivity)")
plt.ylabel("Temperature (K)")
plt.plot(x,t)
plt.savefig("tempVemissivity.png")

#Temperature vs albedo
fig = plt.figure()
x = np.linspace(0,1,100)
t = ((1367.6*(1-x))/(4*sigma*0.5244))**0.25
plt.xlabel("Albedo")
plt.ylabel("Temperature (K)")
plt.plot(x,t)
plt.savefig("tempValbedo.png")