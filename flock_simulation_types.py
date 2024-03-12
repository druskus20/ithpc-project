from typing import Tuple
import numpy as np

SimulationParameters = Tuple[float, float, float, float, float, float, float]
ExtraParameters = Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]

SEED = 17

"""
SimulationParameters: Type alias for the parameters of the simulation.
    This tuple contains:
    - v0 (float): Magnitude of bird velocities.
    - eta (float): Magnitude of random perturbations.
    - L (float): Size of the simulation domain.
    - R (float): Interaction radius for alignment.
    - dt (float): Time step size.
    - Nt (float): Number of time steps.
    - N (float): Number of birds.

ExtraParameters: Type alias for the extra parameters used in the simulation.
    This tuple contains numpy arrays representing:
    - x (np.ndarray): x-coordinates of bird positions.
    - y (np.ndarray): y-coordinates of bird positions.
    - vx (np.ndarray): x-components of bird velocities.
    - vy (np.ndarray): y-components of bird velocities.
    - theta (np.ndarray): Angles representing bird orientations.

SEED: Global seed value for random number genera
"""
