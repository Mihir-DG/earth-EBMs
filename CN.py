from netCDF4 import Dataset
import numpy as np
from matplotlib import pyplot as plt

latitudes = np.linspace(-np.pi/2, np.pi/2, 73)

olr = Dataset("olr.mon.mean.nc","r",format="NETCDF4")
print(olr.variables['olr'])
olr = np.array(olr.variables['olr'])
olr = np.array(olr[-7-12*30:-7], dtype=np.float64)

olr = np.mean(olr.mean(axis=0),axis=1)
olr = np.average(olr, weights=np.cos(latitudes))
print(olr)


upFlux = Dataset("ulwrf.sfc.mon.mean.nc","r",format="NETCDF4")
upFlux = np.array(upFlux.variables['ulwrf'])
upFlux = np.array(upFlux[-7-12*30:-7],dtype=np.float64)
print(upFlux.shape)
print(upFlux.mean())


"""
surfT = Dataset("tmp.0-10cm.mon.mean.nc","r",format="NETCDF4")
print(surfT.variables)
surfT = np.array(surfT.variables['tmp'])
# Downloaded June 2021 --> Ignoring '21 data.
surfT = np.array(surfT[-7-12*30:-7], dtype=np.float64)
newSurfT = np.empty(surfT.shape)
validIndexes = np.argwhere(surfT==-9.969209968386869e+36)
sumT,count = 0,0
for valid in validIndexes:
	sumT += surfT[valid]
	print(surfT[valid].shape)
	count += 1
print(sumT/count)


#plt.plot(surfT)
#plt.show()
#3009526
"""