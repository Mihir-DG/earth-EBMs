from sympl import (
    AdamsBashforth, PlotFunctionMonitor)
from climt import (
    Frierson06LongwaveOpticalDepth, GrayLongwaveRadiation,
    SimplePhysics, DryConvectiveAdjustment, SlabSurface,
    get_default_state)
import climt
import datetime
import math
import numpy as np
import sympl
from datetime import timedelta
import matplotlib.pyplot as plt
import metpy.calc as calc
import os
from metpy.units import units

# Importing functions from local pys.
from stoppingCriteria_fn import net_energy_level_in_column
from modelTimestep import runningModel
from csv_writer import output_to_csv
from equilibriumProfiles import eqProfs

def cleaningUp():
	CSVs = 'output_runModel'
	graphs = 'graphs'
	foldersMain = [CSVs, graphs]
	for item in foldersMain:
		for file in os.listdir(item):
			os.remove(os.path.join(item,file))
	return 0.

def main():
	cleaningUp()
	state, olr, timeTaken, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, convection_heatRate, airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord = runningModel()
	output_to_csv(timeTaken, lwFluxNet, swFluxNet, sw_heatRate, lw_heatRate, convection_heatRate,
		airTemperatureProf, interface_airPressure_vertCoord, airPressure_vertCoord)
	eqProfs()

	
if __name__ == "__main__":
	main()
