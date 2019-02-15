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

## Way forward/simple improvements
```
First things You should look at is probably parallelization, as it would drastically lower the time needed to process the tasks.
```

## Experiment

At this point You are most likely ready to develop extensions and new features to the code, enjoy!
Please note that running a batch job with as low as 1000 islands and 300 individuals per islands, can take exceptionally long time to process.

## Useful links:

[DEAP](https://deap.readthedocs.io/en/master/)

[ZEUS](https://docs.cyfronet.pl/display/PLGDoc)

[MPI4PY](https://mpi4py.readthedocs.io/en/stable/)
