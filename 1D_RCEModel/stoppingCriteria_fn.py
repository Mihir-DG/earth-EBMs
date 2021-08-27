from analyticFunctions import radiating_pressure
import numpy as np

def net_energy_level_in_column(state,diagnostics,diff_acceptable):
	radPres = radiating_pressure(state,diagnostics,diff_acceptable)
	radHt = -1
	sb_const = 5.67e-08
	lw_up_ntat_OUT = (np.array(diagnostics['upwelling_longwave_flux_in_air']).flatten())[radHt]
	lw_up_surf_IN = (np.array(diagnostics['upwelling_longwave_flux_in_air']).flatten())[0]
	lw_down_ntat_IN = (np.array(diagnostics['downwelling_longwave_flux_in_air']).flatten())[radHt]
	lw_down_surf_OUT = (np.array(diagnostics['downwelling_longwave_flux_in_air']).flatten())[0]
	otherSurfFluxes_IN = (np.array(state['surface_upward_latent_heat_flux'] + state['surface_upward_sensible_heat_flux']).flatten())[0]
	sw_up_ntat_OUT = (np.array(diagnostics['upwelling_shortwave_flux_in_air']).flatten())[radHt]
	sw_up_surf_IN = (np.array(diagnostics['upwelling_shortwave_flux_in_air']).flatten())[0]
	sw_down_ntat_IN = (np.array(diagnostics['downwelling_shortwave_flux_in_air']).flatten())[radHt]
	sw_down_surf_OUT = (np.array(diagnostics['downwelling_shortwave_flux_in_air']).flatten())[0]
	fluxesIn = [lw_up_surf_IN,lw_down_ntat_IN,otherSurfFluxes_IN,sw_up_surf_IN,sw_down_ntat_IN]#,sw_up_surf_reflected_IN]
	fluxesOut = [lw_up_ntat_OUT,lw_down_surf_OUT,sw_up_ntat_OUT,sw_down_surf_OUT]
	netEn = sum(fluxesIn) - sum(fluxesOut)
	return netEn,fluxesIn,fluxesOut

"""
def net_energy_level_in_column(state,diff_acceptable):
	radPres = radiating_pressure(state,diff_acceptable)
	radHt = radPres[1]
	sb_const = 5.67e-08
	lw_up_ntat_OUT = (np.array(state['upwelling_longwave_flux_in_air']).flatten())[radHt]
	lw_up_surf_IN = sb_const * (((np.array(state['surface_temperature']).flatten())[0])**4)
	lw_down_ntat_IN = (np.array(state['downwelling_longwave_flux_in_air']).flatten())[radHt]
	lw_down_surf_OUT = (np.array(state['downwelling_longwave_flux_in_air']).flatten())[0]
	otherSurfFluxes_IN = (np.array(state['surface_upward_latent_heat_flux'] + state['surface_upward_sensible_heat_flux']).flatten())[0]
	sw_up_ntat_OUT = (np.array(state['upwelling_shortwave_flux_in_air']).flatten())[radHt]
	sw_up_surf_IN = (np.array(state['upwelling_shortwave_flux_in_air']).flatten())[0]
	sw_down_ntat_IN = (np.array(state['downwelling_shortwave_flux_in_air']).flatten())[radHt]
	sw_down_surf_OUT = (np.array(state['downwelling_shortwave_flux_in_air']).flatten())[0]
	#sw_up_surf_reflected_IN = albedo * (np.array(state['downwelling_shortwave_flux_in_air']).flatten())[0]
	fluxesIn = [lw_up_surf_IN,lw_down_ntat_IN,otherSurfFluxes_IN,sw_up_surf_IN,sw_down_ntat_IN]#,sw_up_surf_reflected_IN]
	fluxesOut = [lw_up_ntat_OUT,lw_down_surf_OUT,sw_up_ntat_OUT,sw_down_surf_OUT]
	netEn = sum(fluxesIn) - sum(fluxesOut)
	return netEn,fluxesIn,fluxesOut
"""

#sw_up_surf_reflected_IN removed b/c gray shortwave not considered
# i.e. any reflected shortwave (upwelling) leaves the atmosphere, hence, net zero impact.

# Will require consideration if gray shortwave component introduced and added to model setup
