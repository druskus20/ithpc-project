import numpy as np
from time import time_ns
from flock_simulation_types import SimulationParameters, ExtraParameters, SEED
from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from concurrent.futures import ThreadPoolExecutor

"""
Create Your Own Active Matter Simulation (With Python)
Philip Mocz (2021) Princeton Univeristy, @PMocz
Pedro Burgos (2024) KTH University

Simulate Viscek model for flocking birds

"""

def animate(name: str, sim_parameters: SimulationParameters, positions: np.ndarray, velocities: np.ndarray) -> None:
    """
    Create an animation of the flock simulation.

    Parameters:
        name (str): The name of the output animation file.
        sim_parameters (SimulationParameters): Simulation parameters.
        positions (np.ndarray): Positions of the birds.
        velocities (np.ndarray): Velocities of the birds.

    Returns:
        None
    """
    plt.clf()
    plt.close()
    fig = plt.figure(figsize=(4,4), dpi=600)
    ax = plt.gca()
    ax.clear()

    (v0, eta, L, R, dt, Nt, N) = sim_parameters
    x: np.ndarray = positions[0,:,0]
    y: np.ndarray = positions[0,:,1]
    vx: np.ndarray = velocities[0,:,0]
    vy: np.ndarray = velocities[0,:,1]

    quiver = ax.quiver(x,y,vx,vy)

    def step_function(frame: int, positions: np.ndarray, velocities: np.ndarray) -> None:
        """
        Update the animation for each frame.

        Parameters:
            frame (int): Current frame number.
            positions (np.ndarray): Positions of the birds.
            velocities (np.ndarray): Velocities of the birds.

        Returns:
            None
        """
        x: np.ndarray = positions[frame,:,0]
        y: np.ndarray = positions[frame,:,1]
        vx: np.ndarray = velocities[frame,:,0]
        vy: np.ndarray = velocities[frame,:,1]
        quiver.set_offsets(np.column_stack([x, y]))
        quiver.set_UVC(vx, vy)

    ani = FuncAnimation(
        fig, 
        step_function,
        fargs=(positions, velocities),
        frames=Nt,
        interval=1, 
        blit=False, 
        repeat=False, 
    )  

    ani.save(f"{name}.mp4", fps=60, writer='ffmpeg')
    


def simulate(sim_parameters: SimulationParameters) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Simulate the flock behavior.

    Parameters:
        sim_parameters (SimulationParameters): Simulation parameters.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: Positions, velocities, and step times.
    """
    ## Init ##
    np.random.seed(SEED)

    (v0, eta, L, R, dt, Nt, N) = sim_parameters

    x: np.ndarray = np.random.rand(N,1)*L
    y: np.ndarray = np.random.rand(N,1)*L
    
    # bird velocities
    theta: np.ndarray = 2 * np.pi * np.random.rand(N,1)
    vx: np.ndarray = v0 * np.cos(theta)
    vy: np.ndarray = v0 * np.sin(theta)
    
    positions = []
    positions.append(np.column_stack([x, y]))
    velocities = []
    velocities.append(np.column_stack([vx, vy]))
    step_times = []


    ## Run the simuation ##
    extra_parameters: ExtraParameters = (x, y, vx, vy, theta)
   
    for i in range(Nt):
        time: int = time_ns()
        extra_parameters, ps, vs = step(i, sim_parameters, extra_parameters)
        step_times.append(time_ns() - time)
        positions.append(ps)
        velocities.append(vs)


    
    return np.asarray(positions), np.asarray(velocities), np.asarray(step_times)


def step(frame: int, sim_parameters: SimulationParameters, extra_parameters: ExtraParameters) -> Tuple[ExtraParameters, np.ndarray, np.ndarray]:
    """
    Perform a single step in the simulation, using parallel computation.

    Parameters:
        frame (int): Current frame number.
        sim_parameters (SimulationParameters): Simulation parameters.
        extra_parameters (ExtraParameters): Extra parameters for the simulation.

    Returns:
        Tuple[ExtraParameters, np.ndarray, np.ndarray]: Updated extra parameters, positions, and velocities.
    """
    # Simulation parameters
    (v0, eta, L, R, dt, Nt, N) = sim_parameters
    (x, y, vx, vy, theta) = extra_parameters

    # move
    x += vx*dt
    y += vy*dt
    
    # apply periodic BCs
    x = x % L
    y = y % L
    

    ## parallel: ##

    # find mean angle of neighbors within R
    mean_theta: np.ndarray = theta

    def bird(b):
        neighbors = (x - x[b]) ** 2 + (y - y[b]) ** 2 < R**2
        sx: float = np.sum(np.cos(theta[neighbors]))
        sy: float = np.sum(np.sin(theta[neighbors]))
        return np.arctan2(sy, sx)

    with ThreadPoolExecutor(max_workers=8) as executor:
        mean_theta = np.array(list(executor.map(bird, range(N))))
        
    mean_theta = mean_theta.reshape(x.shape)
    # add random perturbations
    theta = mean_theta + eta*(np.random.rand(N,1)-0.5)
    
    # update velocities
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)
    
    # Store updated positions and velocities
    positions: np.ndarray = np.column_stack([x, y])
    velocities: np.ndarray = np.column_stack([vx, vy])

    return (x, y, vx, vy, theta), positions, velocities

