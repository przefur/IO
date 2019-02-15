# IO

Project for 2018/2019 IO classes

## Getting Started

These instructions will get You a copy of the project up and running on Your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
First of all, You need a Python installed, ideally 3.6+
On top of Python You need to download additional packages mentioned below.
```

### Installing

A step by step series of examples that tell you how to get a development env running

Python Installation

```
Pretty Straightforward, download and install version of Your choice from [Python](https://www.python.org/downloads/)
```

Python Packages Installation

```
To get things running You need deap and scoop packages.
To get those, simply run a pip commands:
pip install deap
pip install scoop
```


## Running the tests

To run the tests, You need a valid connection to Zeus/Prometheus

### Connecting to Zeus

You would like to get started around here: 

```
ZEUS - https://docs.cyfronet.pl/display/PLGDoc
```

### After You get an account up and running with resources

Use a FTP client to send Your scripts to your catalogue on Zeus & create an environment

```
Hint: 
plgrid/tools/python-intel/3.6.5
Add pip packages with '--user' option
```

## Parallelization
Parallelization was achieved using mpi4py library. Each process is assigned its own island. In the scope of each iteration an evolution algotrithm is run (DEAP) and best result is propagated to other processes. Currently two different topologies are supported:
- circle topology with RTT propagation
![alt text](https://github.com/przefur/IO/blob/master/images/circle_top.png)
- star topology
![alt text](https://github.com/przefur/IO/blob/master/images/star_top.png)

In case of error on one of the processes the failover can be done with following procedure:
```
try:
  <communication operation to process X>
except:
  <change the address from process X to Y, repeat communication operation>
```

Currently the process is not supporting the failover opeartion due to switch to communication functions that don't support it. Change was done to improve the performance of the system.

Each process goes through following states when running:
![alt text](https://github.com/przefur/IO/blob/master/images/phases.png)

First the initial values are innitiated and variables required by the program are setup. The execution command should look like that:
```
python main.py <population of each island> <number of iterations> <topology type> [<RTT for circle topology] [<density for star topology>]
```
Afterwards the single iteration of evolution algorithm is run and the results are send to the processes next to the source. Afterwards all communications are resolved and part of the old population is overwritten by newcomers. That process is repeated until the number of iterations stated in the command line is reached.
### Results
After running main.py on Zeus node with 48 processors following results were found for small amount of iterations:

![alt text](https://github.com/przefur/IO/blob/master/images/speedup.png)

![alt text](https://github.com/przefur/IO/blob/master/images/efficiency.png)

There're some visible improvements for small amount of iterations. Sadly for higher amount (above 100) due to unexplained desynchronizations between different nodes the execution times become much higher with higher number of processes bringing the speedup down.


## Experiment

At this point You are most likely ready to develop extensions and new features to the code, enjoy!
Please note that running a batch job with as low as 1000 islands and 300 individuals per islands, can take exceptionally long time to process.

## Useful links:

[DEAP](https://deap.readthedocs.io/en/master/)

[ZEUS](https://docs.cyfronet.pl/display/PLGDoc)

[MPI4PY](https://mpi4py.readthedocs.io/en/stable/)
