import numpy as np

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