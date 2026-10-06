from typing import Optional
from utils.rng import RNG

def step_room(T: float, heater_on: int, T_out: float, R: float, C: float, P: float,
              dt: float, process_sigma: float = 0.0, rng: Optional[RNG] = None) -> float:
    ''' Simulate one time step of a simple RC room thermal model.
        T: Current room temperature (degrees Celsius).
        heater_on: Heater state (0=OFF, 1=ON).
        T_out: Outside temperature (degrees Celsius).
        R: Thermal resistance (degrees Celsius per Watt).
        C: Thermal capacitance (Joules per degrees Celsius).
        P: Heater power when ON (Watts).
        dt: Time step duration (seconds).
        process_sigma: Standard deviation of process noise (degrees Celsius).
        rng: Optional random number generator for noise.
        Returns the updated room temperature after time step dt.
    '''
    if R <= 0:
        raise ValueError("R must be positive")
    if C <= 0:
        raise ValueError("C must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if process_sigma < 0:
        raise ValueError("process_sigma must be non-negative")
    if process_sigma > 0 and rng is None:
        raise ValueError("rng is required when process_sigma is positive")

    dTdt = (T_out - T) / (R * C) + heater_on * P / C
    updated_temp = T + dt * dTdt
    if process_sigma > 0:
        updated_temp += rng.gauss(0.0, process_sigma)
    return updated_temp
