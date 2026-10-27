
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from turbie_mod import turbine_motion, load_wind_data, calculate_CT, create_system_matrices
from pathlib import Path


# Load turbine parameters from txt file
parameters = np.loadtxt("turbie_inputs/turbie_parameters.txt")
mb, mn, mh, mt, c1, c2, k1, k2, fb, ft, drb, drt, Dr, rho = parameters

# Create mass, damping and stiffness matrices for the system
M, C, K = create_system_matrices(mb, mn, mh, mt, c1, c2, k1, k2)

print("Mass matrix:\n", M)
print("Damping matrix:\n", C)
print("Stiffness matrix:\n", K)

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

        # Define filename for the current wind speed and TI
        filename = f"wind_files/wind_TI_{ti}/wind_{speed}_ms_TI_{ti}.txt"

        # Load wind data from the Turbie module
        time, wind_speed = load_wind_data(filename)

        # Interpolate CT values based on mean wind speed
        ct_interpolated = calculate_CT(wind_speed, ct_data)

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
            raise RuntimeError(
                f"Simulation failed at {speed} m/s, TI = {ti}: {solution.message}"
            )

        # Get the displacements for the current wind speed
        x1 = solution.y[0]  # Blade displacement
        x2 = solution.y[1]  # Tower displacement

        # Get the velocities for the current wind speed
        v1 = solution.y[2]  # Blade velocity
        v2 = solution.y[3]  # Tower velocity

        # Save simulation time series to a text file
        output_folder = Path(f"outputs/TI_{ti}")
        output_folder.mkdir(parents=True, exist_ok=True)

        # Combine simulation results into five columns
        output_data = np.column_stack((
            solution.t,  # Time values
            x1,          # Blade displacement
            x2,          # Tower displacement
            v1,          # Blade velocity
            v2           # Tower velocity
        ))

        # Define filename for the current simulation
        output_filename = output_folder / f"simulation_{speed}_ms_TI_{ti}.txt"

        # Save the simulation results
        np.savetxt(
            output_filename,
            output_data,
            header="Time[s] Blade_displacement[m] Tower_displacement[m] Blade_velocity[m/s] Tower_velocity[m/s]",
            fmt="%.6f"
        )

        # Calculate mean and standard deviation of displacements for the current wind speed and append to the results lists
        mean_blade_results[ti].append(np.mean(x1))
        mean_tower_results[ti].append(np.mean(x2))
        std_blade_results[ti].append(np.std(x1))
        std_tower_results[ti].append(np.std(x2))

        print(speed, "m/s - TI:", ti, "- Simulation successful:", solution.success)


# Save mean and standard deviation results to a text file for each TI
for ti in [0.05, 0.1, 0.15]:

    # Check the number of stored simulations
    print("TI:", ti, "- Stored simulations:", len(mean_blade_results[ti]))

    # Create output folder for the current TI
    output_folder = Path(f"outputs/TI_{ti}")
    output_folder.mkdir(parents=True, exist_ok=True)

    # Combine wind speeds and statistics into five columns
    statistics_data = np.column_stack((
        range(4, 26),           # Wind speeds from 4 to 25 m/s
        mean_blade_results[ti], # Mean blade displacement
        mean_tower_results[ti], # Mean tower displacement
        std_blade_results[ti],  # Standard deviation of blade displacement
        std_tower_results[ti]   # Standard deviation of tower displacement
    ))

    # Define filename for the current TI
    statistics_filename = output_folder / f"statistics_TI_{ti}.txt"

    # Save statistics to text file
    np.savetxt(
        statistics_filename,
        statistics_data,
        header="Wind_speed[m/s] Mean_blade[m] Mean_tower[m] Std_blade[m] Std_tower[m]",
        fmt=["%d", "%.6f", "%.6f", "%.6f", "%.6f"]
    )

    print("Statistics saved to:", statistics_filename)



# Plot mean blade displacement for different turbulence intensities
plt.figure(figsize=(10, 5))

for ti in [0.05, 0.1, 0.15]:
    plt.plot(range(4, 26), mean_blade_results[ti], label=f"TI = {ti}")

plt.xlabel("Wind speed [m/s]")
plt.ylabel("Mean blade displacement [m]")
plt.title("Mean blade displacement vs. wind speed for different turbulence intensities")
plt.grid(True)
plt.legend()

# Save mean blade displacement figure
plt.savefig("outputs/mean_blade_displacement.png", dpi=300, bbox_inches="tight")
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

# Save mean tower displacement figure
plt.savefig("outputs/mean_tower_displacement.png", dpi=300, bbox_inches="tight")
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

# Save standard deviation of blade displacement figure
plt.savefig("outputs/std_blade_displacement.png", dpi=300, bbox_inches="tight")
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

# Save standard deviation of tower displacement figure
plt.savefig("outputs/std_tower_displacement.png", dpi=300, bbox_inches="tight")
plt.show()


# Check static equilibrium at 4 m/s
u = 4
CT = np.interp(u, ct_data[:, 0], ct_data[:, 1])

F_aero = 0.5 * rho * A * CT * u**2
F_static = np.array([F_aero, 0])

x_static = np.linalg.solve(K, F_static)

print("Static blade displacement:", x_static[0], "m")
print("Static tower displacement:", x_static[1], "m")


# Plot wind speed and displacements over time for one wind scenario
selected_speed = 10
selected_ti = 0.1

# Load original wind data
wind_filename = f"wind_files/wind_TI_{selected_ti}/wind_{selected_speed}_ms_TI_{selected_ti}.txt"
time, wind_speed = load_wind_data(wind_filename)

# Load saved simulation results
simulation_filename = f"outputs/TI_{selected_ti}/simulation_{selected_speed}_ms_TI_{selected_ti}.txt"
simulation_data = np.loadtxt(simulation_filename, skiprows=1)

simulation_time = simulation_data[:, 0]  # Time values
blade_displacement = simulation_data[:, 1]  # Blade displacement
tower_displacement = simulation_data[:, 2]  # Tower displacement

# Create a figure with two graphs
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

# Plot wind speed over time
ax1.plot(time, wind_speed, label="Wind speed")
ax1.set_ylabel("Wind speed [m/s]")
ax1.legend()
ax1.grid(True)

# Plot blade and tower displacements over time
ax2.plot(simulation_time, blade_displacement, label="Blades")
ax2.plot(simulation_time, tower_displacement, label="Tower")
ax2.set_xlabel("Time [s]")
ax2.set_ylabel("Displacement [m]")
ax2.legend()
ax2.grid(True)

fig.suptitle("Wind and turbine response over time (10 m/s, TI = 0.1)")
plt.tight_layout()

# Save time series figure
plt.savefig("outputs/turbie_timeseries_10ms_TI_0.1.png", dpi=300, bbox_inches="tight")

plt.show()