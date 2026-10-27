import numpy as np

# Load wind data from a specified file
def load_wind_data(filename):
    wind_data = np.loadtxt(filename, skiprows=1)

    time = wind_data[:, 0]  # Time values, column 0 of wind_data
    wind_speed = wind_data[:, 1]  # Wind speed values, column 1 of wind_data

    return time, wind_speed

# Calculate CT based on mean wind speed
def calculate_CT(wind_speed, ct_data):
    mean_wind_speed = np.mean(wind_speed)

    ct_interpolated = np.interp(
        mean_wind_speed,
        ct_data[:, 0],  # Wind speed values, column 0 of ct_data
        ct_data[:, 1]   # CT values, column 1 of ct_data
    )

    return ct_interpolated

# Create mass, damping and stiffness matrices
def create_system_matrices(mb, mn, mh, mt, c1, c2, k1, k2):

    # Calculate total blade mass
    m1 = 3 * mb

    # Calculate total nacelle, hub and tower mass
    m2 = mn + mh + mt

    # Create mass matrix for the system
    M = np.array([[m1, 0],
                  [0, m2]])

    # Create damping matrix for the system
    C = np.array([[c1, -c1],
                  [-c1, c1 + c2]])

    # Create stiffness matrix for the system
    K = np.array([[k1, -k1],
                  [-k1, k1 + k2]])

    return M, C, K

def turbine_motion(t, y, M, C, K, wind_at_time, rho, CT, A):
    x1, x2, v1, v2 = y
    
    # Displacement vector
    x = np.array([x1, x2])

    # Velocity vector
    v = np.array([v1, v2])

    # Wind speed at current time
    u = wind_at_time(t)

    # Relative wind speed
    u_rel = u - v1

    # Calculate aerodynamic force on the blades
    F_aero = 0.5 * rho * A * CT * u_rel * abs(u_rel)

    # Matrix for aerodynamic force
    F = np.array([F_aero, 0])  # Assuming force acts only on the blades (x1 direction)

    # Net force calculation
    net_force = F - C @ v - K @ x    

    # Acceleration calculation
    a = np.linalg.solve(M, net_force)

    # Return derivatives
    return np.array([v1, v2, a[0], a[1]])