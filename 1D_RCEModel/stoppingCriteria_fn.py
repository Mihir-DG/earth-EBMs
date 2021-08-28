import numpy as np

def net_energy_level_in_column(state,diagnostics,diff_acceptable):
	sw_upFlux = np.array(diagnostics['upwelling_shortwave_flux_in_air']).flatten()[-1]
	sw_downFlux = np.array(diagnostics['downwelling_shortwave_flux_in_air']).flatten()[-1]
	lw_upFlux = np.array(diagnostics['upwelling_longwave_flux_in_air']).flatten()[-1]
	lw_downFlux = np.array(diagnostics['downwelling_longwave_flux_in_air']).flatten()[-1]
	return sw_downFlux - sw_upFlux + lw_downFlux - lw_upFlux