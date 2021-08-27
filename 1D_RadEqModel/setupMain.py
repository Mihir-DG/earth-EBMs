import numpy as np

def net_energy_level_in_column(state,diagnostics,diff_acceptable):
	# Used to calculate balance b/w energy entry and departure
	# to identify equilibrium  from atmosphere
	lw_up_ntat_OUT = (np.array(diagnostics['upwelling_longwave_flux_in_air']).flatten())[-1]
	lw_up_surf_IN = (np.array(diagnostics['upwelling_longwave_flux_in_air']).flatten())[0]
	lw_down_ntat_IN = (np.array(diagnostics['downwelling_longwave_flux_in_air']).flatten())[-1]
	lw_down_surf_OUT = (np.array(diagnostics['downwelling_longwave_flux_in_air']).flatten())[0]
	otherSurfFluxes_IN = (np.array(state['surface_upward_latent_heat_flux'] + state['surface_upward_sensible_heat_flux']).flatten())[0]
	sw_up_ntat_OUT = (np.array(diagnostics['upwelling_shortwave_flux_in_air']).flatten())[-1]
	sw_up_surf_IN = (np.array(diagnostics['upwelling_shortwave_flux_in_air']).flatten())[0]
	sw_down_ntat_IN = (np.array(diagnostics['downwelling_shortwave_flux_in_air']).flatten())[-1]
	sw_down_surf_OUT = (np.array(diagnostics['downwelling_shortwave_flux_in_air']).flatten())[0]
	fluxesIn = [lw_up_surf_IN,lw_down_ntat_IN,otherSurfFluxes_IN,sw_up_surf_IN,sw_down_ntat_IN]#,sw_up_surf_reflected_IN]
	fluxesOut = [lw_up_ntat_OUT,lw_down_surf_OUT,sw_up_ntat_OUT,sw_down_surf_OUT]
	netEn = sum(fluxesIn) - sum(fluxesOut)
	return netEn,fluxesIn,fluxesOut
