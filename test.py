import pytest
from flock_simulation import simulate, step
import numpy as np

# Seed is taken from the flock_simulation_types.py file

v0 = 1.0          
eta = 0.5        
R = 1           
dt = 0.2       
L = 10        
Nt = 10
N = 10

sim_parameters = (v0, eta, L, R, dt, Nt, N)

expected_positions_step_10 = [[2.2891999,  1.33494762],
 [3.37933285, 0.1717447 ],
 [0.55203815, 7.67654308],
 [9.7810559 , 7.12464767],
 [6.00329694, 1.16827763],
 [8.16949674, 7.68293198],
 [7.81990414, 6.86436183],
 [7.39277316, 7.06298293],
 [0.29397963, 2.8620359 ],
 [2.14315113, 3.98728931]]
expected_velocities_step_10 = [[-0.35997506,  0.93296193],
 [-0.99657208, -0.08272902],
 [-0.5108848 , -0.85964918],
 [-0.31594041, -0.94877903],
 [-0.97160943,  0.23659059],
 [ 0.68987667,  0.72392692],
 [ 0.87904488,  0.47673903],
 [ 0.73145682,  0.68188777],
 [ 0.12501253, -0.99215516],
 [-0.99879694, -0.04903756]]


@pytest.mark.parametrize(
    "sim_parameters, expected_positions, expected_velocities",
    [
        (sim_parameters, expected_positions_step_10, expected_velocities_step_10),
    ]
)
def test_simulation(sim_parameters, expected_positions, expected_velocities):
    # Run simulation
    positions, velocities, _ = simulate(sim_parameters)
    
    # Compare positions and velocities with expected output
    assert np.allclose(positions[-1], expected_positions), "Positions do not match expected output"
    assert np.allclose(velocities[-1], expected_velocities), "Velocities do not match expected output"


x = np.array([[2.94665003],
              [5.30586756],
              [1.91520787],
              [0.67900358],
              [7.8698546 ],
              [6.56333522],
              [6.37520896],
              [5.75602894],
              [0.39062916],
              [3.57813604]])
y = np.array([[9.45683187],
              [0.6004468 ],
              [8.64042104],
              [8.77290526],
              [0.51193666],
              [6.52418615],
              [5.51751369],
              [5.97513253],
              [4.83528624],
              [2.82988161]])
vx = np.array([[-0.29539556],
               [-0.92624466],
               [-0.79417156],
               [ 0.24077448],
               [-0.87167933],
               [ 0.61833417],
               [ 0.58316683],
               [ 0.94036601],
               [-0.19948099],
               [-0.26276595]])
vy = np.array([[ 0.95537504],
               [-0.37692284],
               [ 0.60769362],
               [-0.97058109],
               [ 0.49007667],
               [ 0.7859153 ],
               [ 0.81235242],
               [ 0.34016433],
               [-0.9799017 ],
               [ 0.9648596 ]])
theta = np.array([[1.87066586],
                  [3.5280645 ],
                  [2.48843943],
                  [4.95555271],
                  [2.62941494],
                  [0.904175  ],
                  [0.94817473],
                  [0.34709164],
                  [4.51156075],
                  [1.83668411]])

extra_parameters = (x, y, vx, vy, theta)
expected_positions_step_0 = [[2.88757092, 9.64790688],
 [5.12061863, 0.52506223],
 [1.75637356, 8.76195976],
 [0.72715848, 8.57878904],
 [7.69551873, 0.60995199],
 [6.68700205, 6.68136921],
 [6.49184233, 5.67998417],
 [5.94410214, 6.0431654 ],
 [0.35073296, 4.6393059 ],
 [3.52558285, 3.02285353]]
expected_velocities_step_0 = [[-0.49200563,  0.87059202],
 [-0.96339316, -0.26809255],
 [-0.87946291,  0.47596743],
 [ 0.33413258, -0.94252608],
 [-0.79945306,  0.60072856],
 [ 0.658265,    0.75278628],
 [ 0.77102252,  0.63680788],
 [ 0.83539215,  0.5496544 ],
 [-0.36368753, -0.931521  ],
 [-0.22652457,  0.97400545]]



@pytest.mark.parametrize(
    "frame, sim_parameters, extra_parameters, expected_positions, expected_velocities",
    [
        (0, sim_parameters, extra_parameters, expected_positions_step_0, expected_velocities_step_0),
    ]
)
def test_step(frame, sim_parameters, extra_parameters, expected_positions, expected_velocities):
    # Run step function
    updated_extra_parameters, positions, velocities = step(frame, sim_parameters, extra_parameters)
    
    # Compare positions and velocities with expected output
    assert np.allclose(positions, expected_positions), "Positions do not match expected output"
    assert np.allclose(velocities, expected_velocities), "Velocities do not match expected output"

