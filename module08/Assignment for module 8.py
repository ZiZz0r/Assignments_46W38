import numpy as np
import matplotlib.pyplot as plt


class GeneralWindTurbine:
    """General wind turbine model."""

    def __init__(self, rotor_diameter, hub_height,
                 rated_power, v_in, v_rated, v_out,
                 name=None):

        # Store the turbine characteristics here
        self.rotor_diameter = rotor_diameter
        self.hub_height = hub_height
        self.rated_power = rated_power
        self.v_in = v_in
        self.v_rated = v_rated
        self.v_out = v_out
        self.name = name
    def get_power(self, v):
        """Calculate the power output of the wind turbine for a given wind speed.

        Parameters
        ----------
        v : float or array-like
            Wind speed in m/s.

        Returns
        -------
        float or array-like
            Power output in kW.
        """
        v = np.asarray(v, dtype=float)
        power = np.zeros_like(v)

        # Below cut-in wind speed, power is zero
        power[v < self.v_in] = 0

        # Between cut-in and rated wind speed, power increases cubically
        mask = (v >= self.v_in) & (v < self.v_rated)
        power[mask] = self.rated_power * (v[mask] / self.v_rated)**3
        # Between rated and cut-out wind speed, power is constant at rated power
        mask = (v >= self.v_rated) & (v < self.v_out)
        power[mask] = self.rated_power

        # Above cut-out wind speed, power is zero
        power[v >= self.v_out] = 0

        return power


class WindTurbine(GeneralWindTurbine):
    """Wind turbine using measured power curve data."""

    def __init__(self, rotor_diameter, hub_height,
                 rated_power, v_in, v_rated, v_out,
                 power_curve_data, name=None):

        super().__init__(
            rotor_diameter, hub_height, rated_power,
            v_in, v_rated, v_out, name
        )

        self.power_curve_data = np.asarray(
            power_curve_data, dtype=float
        )
    def get_power(self, v):
        """Calculate power by interpolating the turbine power curve."""

        wind_speeds = self.power_curve_data[:, 0]
        power_values = self.power_curve_data[:, 1]
        return np.interp(v, wind_speeds, power_values)

# Example power curve: wind speed [m/s], power [kW]
test_curve = np.array([
    [0, 0],
    [4, 0],
    [6, 600],
    [8, 1800],
    [12, 8000],
    [20, 8000],
    [25, 0]
])

# Create an object of the child class
turbine2 = WindTurbine(
    rotor_diameter=164,
    hub_height=110,
    rated_power=8000,
    v_in=4,
    v_rated=12,
    v_out=25,
    power_curve_data=test_curve,
    name="Interpolated Turbine"
)
wind_speeds = np.array([0, 4, 8, 12, 20, 25])

print(turbine2.get_power(wind_speeds))
