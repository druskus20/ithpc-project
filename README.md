# Flock Simulation

pedrobg@kth.se

## Structure:

```
flock_simulation_types.py       # Common type aliases and constants 

flock_simulation_original.py    # Original implementation of flock simulation
flock_simulation.py             # Refactored implementation of flock_simulation_original.py
flock_simulation_C.py           # Cython-optimized flock simulation
flock_simulation_parallel.py    # Parallelized flock simulation
```

## Pre-requisites

```
pip install -r requirements.txt
```

Compile Cython
```
./compile_cython.sh
```

Run tests:
```
pytest test.py
```

## Run

The entry point to the project is the Jupiter notebook `Flock Simulation.ipynb`. It contains the main code in a way that should be reproducible and easy to understand.

An record of the results obtained in my tests is provided in `results.csv`

## Documentation

The documentation for the modules can be found in the form of doc comments in the code. The code is also structured in a way that should be self-explanatory, and some additional clarifications are provided as inline comments.

The notebook `Flock Simulation.ipynb` also contains explanations and visualizations of results.

It is also recommended to read the report `report/report.pdf` for a more detailed explanation of the project.


> This is the public version of the repository where the code has been cleaned up and any private parts have been removed. It should work by itself, if additional explanations, intermediate steps, data from previous executions and tests is required, contact pedrobg@kth.se.
