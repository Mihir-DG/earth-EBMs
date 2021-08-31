from matplotlib import pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

RCE = np.load("RCE_pT.npy")
RE = np.load("RE_pT.npy")
interface_airPressure_vertCoord = np.load("airP.npy")
interface_airPressure_vertCoord = [round((float(ele)/100),0) for ele in list(interface_airPressure_vertCoord)]
# Graphing Theta.
fig = plt.figure(figsize=(12,8),dpi=1000)

ax = fig.add_subplot(1,2,1)
ax.yaxis.set_major_locator(ticker.MultipleLocator(6))
ax.yaxis.set_ticks(np.linspace(1000,30,6))
ax.plot(RE[:45],interface_airPressure_vertCoord[:45],'-o', label="Model 3")
ax.set_yscale('log')
ax.set_ylabel("Pressure (hPa)")
ax.set_xlabel("Model 2 Potential Temperature (K)")
ax.axes.invert_yaxis()
ax.set_ylim(1e3, 30.)


ax = fig.add_subplot(1,2,2)
ax.yaxis.set_major_locator(ticker.MultipleLocator(6))
ax.yaxis.set_ticks(np.linspace(1000,30,6))
ax.plot(RCE[:45],interface_airPressure_vertCoord[:45],'-o',label="Model 2")
ax.set_yscale('log')
ax.set_ylabel("Pressure (hPa)")
ax.set_xlabel("Model 3 Potential Temperature (K)")
ax.axes.invert_yaxis()
ax.set_ylim(1e3, 30.)

plt.savefig("../graphs/pT.png")

