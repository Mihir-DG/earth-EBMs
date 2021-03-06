# earth-EBMs
A hierarchial set of energy balance models parameterized for the Earth system using the Rapid Radiative Transfer Model for GCMs (RRTM-G) as implemented in climt using Python. Convection is modeled in the RCE setup as a secondary adjustive mechanism that is activated in regions of radiative instability.

#### Models:

1) 0D Radiative Equilibrium   
2) 1D Radiative Equilibrium (RE)
3) 1D Radiative-Convective Equilibrium (RCE)

#### 0-D Model Initial Conditions:
- Planetary Albedo: 0.29
- Emissivity Coefficient: 0.619 +/- 0.000425

#### 1-D Model Initial Conditions:
- Surface Type: Aquaplanet
- Zenith angle: 75 deg.
- Surface Direct SW Albedo: 0.3
- Surface Diffuse SW Albedo: 0.259 (0.3 sin(60))
- Surface Direct Near-Infrared Albedo: 0.45
- Ocean Mixed Layer Depth: 40 m
- Solar variation: None; Uniform flux of 1367.6
- Error margin in energy budget: 5 W/m^2.
- RE Energetics
  - Surface temperature: 250 K
  - Air Temperature: Isothermal; 230 K.
- RCE Energetics
  - Surface Temperature: 275 K
  - Air Temperature: Isothermal; 250 K  
