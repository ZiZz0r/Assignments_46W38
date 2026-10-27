import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Load turbine parameters from txt file
parameters = np.loadtxt("turbie_inputs/turbie_parameters.txt")
mb, mn, mh, mt, c1, c2, k1, k2, fb, ft, drb, drt, Dr, rho = parameters

# Calculate total blade mass
m1 = 3 * mb

print("Total blade mass:", m1, "kg")

#Calculate total nacelle, hub and tower mass
m2 = mn + mh + mt

print("Total nacelle, hub and tower mass:", m2, "kg")

#Create mass matrices for the system
M = np.array([[m1, 0], 
             [0, m2]])

#Create damping matrices for the system
C = np.array([[c1,-c1],
            [-c1, c1 + c2]])

#Create stiffness matrices for the system
K = np.array([[k1,-k1],
            [-k1, k1 + k2]])

# Load wind data
wind_data = np.loadtxt(
    "wind_files/wind_TI_0.1/wind_4_ms_TI_0.1.txt",
    skiprows=1
)

time = wind_data[:, 0]
wind_speed = wind_data[:, 1]

print("Time:", time[:5])
print("Wind speed:", wind_speed[:5])

# Plot wind speed over time
# plt.figure(figsize=(10, 5))
# plt.plot(time, wind_speed, label="Wind speed")

# plt.xlabel("Time [s]")
# plt.ylabel("Wind speed [m/s]")
# plt.title("Wind speed over time - 4 m/s, TI = 0.1")
# plt.grid(True)
# plt.legend()

# plt.show()

# Load CT data from txt file
ct_data = np.loadtxt("turbie_inputs/CT.txt", skiprows=1)

# Calculate mean wind speed
mean_wind_speed = np.mean(wind_speed)
print(mean_wind_speed)

# Interpolate CT values based on mean wind speed
ct_interpolated = np.interp(mean_wind_speed, 
                            ct_data[:, 0], # Wind speed values, column 0 of ct_data
                            ct_data[:, 1]) # CT values, column 1 of ct_data
print("Interpolated CT value:", ct_interpolated)

# Calculate swept area of the rotor
A = np.pi * (Dr/2)**2
print("Swept area of rotor:", A, "m^2")

# Interpolate wind speed at a given time
def wind_at_time(t):
    return np.interp(t, time, wind_speed)
