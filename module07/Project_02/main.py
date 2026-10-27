
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from turbie_mod import turbine_motion

# Load turbine parameters from txt file
parameters = np.loadtxt("turbie_inputs/turbie_parameters.txt")
mb, mn, mh, mt, c1, c2, k1, k2, fb, ft, drb, drt, Dr, rho = parameters

# Calculate total blade mass
m1 = 3 * mb
print("Total blade mass:", m1, "kg")

# Calculate total nacelle, hub and tower mass
m2 = mn + mh + mt
print("Total nacelle, hub and tower mass:", m2, "kg")

# Create mass matrices for the system
M = np.array([[m1, 0],
              [0, m2]])

# Create damping matrices for the system
C = np.array([[c1, -c1],
              [-c1, c1 + c2]])

# Create stiffness matrices for the system
K = np.array([[k1, -k1],
              [-k1, k1 + k2]])

# Load CT data from txt file
ct_data = np.loadtxt("turbie_inputs/CT.txt", skiprows=1)

# Calculate swept area of the rotor
A = np.pi * (Dr / 2)**2
print("Swept area of rotor:", A, "m^2")

# Interpolate wind speed at a given time
def wind_at_time(t):
    return np.interp(t, time, wind_speed)

# Initial conditions
y0 = np.array([0, 0, 0, 0])  # Initial displacements and velocities for blades and nacelle

# Load wind data for different wind speeds
mean_blade_results = {}
mean_tower_results = {}
std_blade_results = {}
std_tower_results = {}

for ti in [0.05, 0.1, 0.15]:
    mean_blade_results[ti] = []
    mean_tower_results[ti] = []
    std_blade_results[ti] = []
    std_tower_results[ti] = []

    for speed in range(4, 26):
        filename = f"wind_files/wind_TI_{ti}/wind_{speed}_ms_TI_{ti}.txt"

        wind_data = np.loadtxt(filename, skiprows=1)

        time = wind_data[:, 0]  # Time values, column 0 of wind_data
        wind_speed = wind_data[:, 1]  # Wind speed values, column 1 of wind_data

        # Calculate mean wind speed
        mean_wind_speed = np.mean(wind_speed)

        # Interpolate CT values based on mean wind speed
        ct_interpolated = np.interp(
            mean_wind_speed,
            ct_data[:, 0],  # Wind speed values, column 0 of ct_data
            ct_data[:, 1]   # CT values, column 1 of ct_data
        )

        # Simulation time settings
        t_span = (time[0], time[-1])  # From the first (0) to the last time point (-1)
        t_eval = time  # Use the same time points as in the wind data

        # Solve the dynamic system
        solution = solve_ivp(
            turbine_motion,
            t_span,
            y0,
            t_eval=t_eval,
            args=(M, C, K, wind_at_time, rho, ct_interpolated, A)
        )

        # Run the simulation and check if it was successful
        if not solution.success:
            raise RuntimeError(f"Simulation failed at {speed} m/s: {solution.message}")

        # Get the displacements for the current wind speed
        x1 = solution.y[0]  # Blade displacement
        x2 = solution.y[1]  # Tower displacement

        # Calculate mean and standard deviation of displacements for the current wind speed and append to the results lists
        mean_blade_results[ti].append(np.mean(x1))
        mean_tower_results[ti].append(np.mean(x2))
        std_blade_results[ti].append(np.std(x1))
        std_tower_results[ti].append(np.std(x2))

        print(speed, "m/s - Simulation successful:", solution.success)

for ti in [0.05, 0.1, 0.15]:
    print("TI:", ti, "- Stored simulations:", len(mean_blade_results[ti]))

# Plot mean blade displacement for different turbulence intensities
plt.figure(figsize=(10, 5))

for ti in [0.05, 0.1, 0.15]:
    plt.plot(range(4, 26), mean_blade_results[ti], label=f"TI = {ti}")

plt.xlabel("Wind speed [m/s]")
plt.ylabel("Mean blade displacement [m]")
plt.title("Mean blade displacement vs. wind speed for different turbulence intensities")
plt.grid(True)
plt.legend()
plt.show()

# Plot mean tower displacement for different turbulence intensities
plt.figure(figsize=(10, 5))

for ti in [0.05, 0.1, 0.15]:
    plt.plot(range(4, 26), mean_tower_results[ti], label=f"TI = {ti}")

plt.xlabel("Wind speed [m/s]")
plt.ylabel("Mean tower displacement [m]")
plt.title("Mean tower displacement vs. wind speed for different turbulence intensities")
plt.grid(True)
plt.legend()
plt.show()


# Plot the standard deviation of blade displacement for different turbulence intensities
plt.figure(figsize=(10, 5))

for ti in [0.05, 0.1, 0.15]:
    plt.plot(range(4, 26), std_blade_results[ti], label=f"TI = {ti}")

plt.xlabel("Wind speed [m/s]")
plt.ylabel("Standard deviation of blade displacement [m]")
plt.title("Standard deviation of blade displacement vs. wind speed for different turbulence intensities")
plt.grid(True)
plt.legend()
plt.show()

# Plot the standard deviation of tower displacement for different turbulence intensities
plt.figure(figsize=(10, 5))

for ti in [0.05, 0.1, 0.15]:
    plt.plot(range(4, 26), std_tower_results[ti], label=f"TI = {ti}")

plt.xlabel("Wind speed [m/s]")
plt.ylabel("Standard deviation of tower displacement [m]")
plt.title("Standard deviation of tower displacement vs. wind speed for different turbulence intensities")
plt.grid(True)
plt.legend()
plt.show()
