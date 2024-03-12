import numpy as np
from flock_simulation_types import SimulationParameters, SEED
from time import time_ns

"""
Create Your Own Active Matter Simulation (With Python)
Philip Mocz (2021) Princeton Univeristy, @PMocz
Pedro Burgos (2024) KTH University

Simulate Viscek model for flocking birds

"""


def simulate(sim_parameters: SimulationParameters):
    """
    Simulate the Viscek model for flocking birds using Finite Volume simulation.

    Parameters:
        sim_parameters (SimulationParameters): Simulation parameters.

    Returns:
        None, None, np.ndarray: Since this function doesn't return positions or velocities, returns None for positions and velocities, and an array of step times.
    """
    # Initialize
    np.random.seed(SEED)      # set the random number generator seed

    (v0, eta, L, R, dt, Nt, N) = sim_parameters

    # bird positions
    x = np.random.rand(N,1)*L
    y = np.random.rand(N,1)*L
    
    # bird velocities
    theta = 2 * np.pi * np.random.rand(N,1)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)
    step_times = []

    # Simulation Main Loop
    for i in range(Nt):
        time = time_ns()
        # move
        x += vx*dt
        y += vy*dt
        
        # apply periodic BCs
        x = x % L
        y = y % L
        
        # find mean angle of neighbors within R
        mean_theta = theta
        for b in range(N):
            neighbors = (x-x[b])**2+(y-y[b])**2 < R**2
            sx = np.sum(np.cos(theta[neighbors]))
            sy = np.sum(np.sin(theta[neighbors]))
            mean_theta[b] = np.arctan2(sy, sx)
            
        # add random perturbations
        theta = mean_theta + eta*(np.random.rand(N,1)-0.5)
        
        # update velocities
        vx = v0 * np.cos(theta)
        vy = v0 * np.sin(theta)
        
        step_times.append(time_ns() - time)
        
        
    return None, None, np.asarray(step_times)

