---
title: |
    Introduction to High Performance Computing \
    Active Matter Time Optimization \
    Expected Grade C
author:
- |
    \textbf{https://github.com/druskus20/ithpc-project} \
    Pedro Burgos Gonzalo \
    pedrobg@kth.se 
date: "15-03-2024"
documentclass: article 
classoption: titlepage
geometry: "left=4cm, right=4cm, top=4cm, bottom=4cm"
---




# Introduction

The study of active matter systems, such as bird flocks, or bacterial colonies,
is of significant interest  due to their complex collective behaviors and
potential applications in various scientific fields such as ecology or
medicine. These systems consist of numerous individual
agents interacting with each other and their environment, exhibiting emergent
behaviors that cannot be understood by
studying each agent in isolation. Instead, we can turn to computational
models to simulate and analyze the dynamics of these systems.

In this case I will focus on the simulation of bird flocks, through the use of 
the Viscek model (1995). This model is based on the assumption that each bird
in a flock adjusts its velocity to match the average velocity of its neighbors.
The Viscek model captures the essential features of bird flocks.

The starting point will be a baseline simulation code provided by Philip Mocz.
The goal of this project is to implement and benchmark various optimization
techniques it. Specifically I aim to enhance the *time* performance of the algorithm. 

Moreover, understanding the dynamics of bird flocks has implications beyond the
realm of biology. By studying flocking behavior, we can gain insights into
swarm intelligence, distributed computing, and decentralized control systems.
These concepts are relevant to a wide range of disciplines, from artificial
intelligence to urban planning. Therefore, by improving the efficiency of bird
flock simulations, we potentially advance our understanding of biological systems
but also contribute to the development of innovative solutions.

# Experimental Setup

All the tests shown in this reports were performed on a modern laptop with the
following specifications:

* Ubuntu Server 22.04.3 LTS
* Linux 5.15.0-92-generic x86_64
* AMD Ryzen 7 PRO 5850U, 8c 16t
* 16 GB Ram
* 512GB SSD

The code lies both in a local git repository and in a remote one, hosted on
GitHub. The code was developed and tested using Python 3.10.12.

The following versions of the main libraries were used:

* numpy==1.24.2
* Cython==3.0.8
* line-profiler==4.1.2

For each graph shown, the results are averaged out of 10 executions. The
standard deviation is also calculated in an aim to showcase any irregularity.

# Methodology

To commence, I initiated the project by refining the baseline simulation code
to enable efficient profiling and benchmarking. I also removed non essential
features like the real time animation - which I implemented in a separate code
- and added at a later stage.

I utilized CProfile and Line Profiler, to analyze the baseline simulation code.
These tools enabled a granular examination of the codebase, pinpointing
specific functions and lines of code contributing significantly to execution
time. This allowed me to confirm that the bottleneck of the code happens in the
inner loop of each step. 

![Inner loop of the simulation](./methodology/1.png){ width=350px }

Line profiler clearly shows that the bulk of time I spent here, and thus I
decided that this would be the entry point of my optimization efforts. 

![Line profiler results for the inner loop](./methodology/2.png){ width=\textwidth }

Next, I refactored the code to allow for easy modification and testing, as well
as increased clarity. I tried different alternatives, such as using a class to
hold global mutable state, or using matplotlib's `FuncAnimation` to animate the
simulation at each step. However I quickly discarded all of these ideas in
favor of simplification, as I quickly realized the performance impact of either
of them was too high. I also added type annotations to all the variables and
parameters, and avoided pass-by-copy variables when possible.

Furthermore, I converted most of the operations to use Numpy's vectorized
functions, as they are potentially faster than the equivalent for loops.

The end result was a simple, clear, and easy to understand code, that is easy
to modify and test. I also designed a Jupyter notebook to visualize and compare
benchmarking results. This platform facilitated the iterative analysis and
comparison of different code versions and optimization techniques. 

\begin{figure}[!htb]
\centering
\includegraphics[width=\textwidth]{./methodology/3.png}
\caption{Function to measure the simulation time}
\end{figure}


For testing, I utilized a parameter grid method, systematically exploring
various combinations to assess their impact on performance. During this
process, I identified two relevant parameters: Nt (number of steps) and N
(number of birds). Altering these parameters could potentially showcase problem
specific optimizations. I decided on a regular distribution for each of them,
based on my previous experience running the code on my hardware. 

I also calculated the average and standard deviation of 10 executions per
result. I measured both the total time it took to execute the simulation, and
the time per step.


\begin{figure}[!htb]
\centering
\includegraphics[width=\textwidth]{./methodology/4.png}
\caption{Parameter grid}
\end{figure}

The first optimization method that I tried was parallelization, I used the
multiprocessing module to parallelize the inner loop of the simulation with a
`ThreadPoolExecutor`. In this way, every step is executed sequentially, as it
depends on the previous one, but the birds calculate the next position in
parallel.

![Parallelization with ThreadPoolExecutor](./methodology/5.png){ width=400px }

The second optimization method that I tried was partial compilation to C.
Utilizing Cython, I was able to transpile different parts of the code to C. I
attempted to compile the entire program at first, as well as the entire step
function, however, it required a significant effort to gain performance
benefits this way, so I decided to focus my efforts even further. In
particular, I offloaded the mean theta calculation, to take advantage of libc's
arithmetic functions. 

I also modified the function to write directly into an array instead of
returning a new one, and I used the `cdef` keyword to declare the types of the
variables. Finally I used the `nogil` keyword to release the GIL, and the
`boundscheck` and `wraparound` keywords to disable bounds checking and negative
indexing.

![Cython compilation](./methodology/6.png){ width=\textwidth }

# Results

First of all, I was able to conclude that altering the parameter space did not
have a significant impact on performance. After increasing either N or Nt the
increase in execution time obtained was regular and uniform. Obviously, a
greater value of N, implies higher deviation since bigger arrays are employed,
but the average time was consistent. 

![Per-step time average and standard deviation when changing N](./results/1.png){ width=\textwidth }

![Cumulative average time per step when changing N](./results/2.png){ width=350px }

Both parameters, N and Nt were tested independently, and the results were
consistent in the total time taken. Increasing either of them resulted in a
proportional and uniform increase in the total time taken to execute the
simulation. 

![Average total time when changing N and Nt](./results/3.png){ width=\textwidth }

However, when comparing the different versions of the algorithms, the results
were clear. The Cython version performs much better than the original, by a
factor of 9.8x approximately. 

To understand the results, it is important to understand the terminology
employed in the graphs. There are 4 names assigned to each of the versions of
the algorithms:

* original: The baseline code provided by Philip Mocz, with the animation removed.
* basic: Basic refactor over the original, utilizing Numpy and restructuring the code.
* parallel: The parallelized version of the basic code using `ThreadPoolExecutor`.
* cython: The Cython compiled version of the basic code, with the `mean_theta` calculation offloaded to C.

![Average total time for the different optimizations](./results/4.png){ width=550px }

The parallel version is counterproductive, as the overhead of creating and
managing threads is too high, and this is reflected in the standard deviation
and the total time taken.

![Time per step and standard deviation for the different optimizations](./results/5.png){ width=\textwidth }

In Figure 11, we can see the high variability of the parallel version, compared
to the other versions. It is worth noting that utilizing a higher number of
workers, or switching to a `ProcessPoolExecutor` did not yield any significant
improvements. It is possible that in a different hardware, diverse results
could be obtained.

Note that I measured both the total execution time, as well as the cumulative
time per step, in order to identify if a bottleneck was present on the actual
algorithm, or the boilerplate code that facilitates the profiling and
benchmarking. However, I was able to verify that this, did not have a
significant impact  on the performance.

# Discussion and Conclusion

Evaluating the average time and the standard deviation across several executions of the simulation contributes to reduce the impact of outliers. 

We have concluded that, in this particular case, the original code was quite
efficient, as it was short and simple. The parallelization method did not yield
any significant performance improvements, since the overhead of creating and
managing threads was too high. 

The Cython compilation method did greatly improve the performance of the inner
loop by a **factor of ~9.8x** approximately, and we established that further C compilation is generally not worth the
effort in maintainability and complexity. Small improvements were achieved by
disabling the GIL and adding type annotations everywhere, however, the biggest
improvement was the use of libc's arithmetic functions. 

The main alternative technique left to explore is the use of GPU acceleration,
through Pytorch, Cupy or another library of a similar nature. This would allow
us to take advantage of the massive parallelism of the GPU to calculate the
next position of the birds and possibly obtain a significant performance
improvement. In my case, I decided to leave it out of the scope given that I
currently do not have access to a stable internet connection due to traveling,
or an Nvidia GPU.

The code and the notebook are available in a public repository at [Github](https://github.com/druskus20/ithpc-project)
