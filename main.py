import sys
import math
import random
import numpy as np
from mpi4py import MPI

from deap import base
from deap import creator
from deap import tools


if len(sys.argv)>1:
    POP_SIZE = int(sys.argv[1])
    MAX_ITER = int(sys.argv[2])
    TOPOLOGY_TYPE = sys.argv[3]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
# ----------

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

neighbors = []
if TOPOLOGY_TYPE == "circle":
    RTT = int(sys.argv[4])
    neighbors.append((rank - 1) % size)
    neighbors.append((rank + 1) % size)
elif TOPOLOGY_TYPE == "star":
    DENSITY = int(sys.argv[4])
    if rank%(DENSITY+1) == 0:
        neighbors = [x for x in range(rank+1,(rank+DENSITY+1)%(size-1))]
    else:
        neighbors = [rank - (rank%(DENSITY+1))]

else:
    raise ValueError("Wrong topology type.")


evolution = ()
iteration = 0

random.seed(64)
# create an initial population of POP_SIZE individuals (where
# each individual is a list of integers)
pop = toolbox.population(n=POP_SIZE)
# CXPB  is the probability with which two individuals
#       are crossed
#
# MUTPB is the probability for mutating an individual
CXPB, MUTPB = 0.5, 0.2

#print("Start of evolution")

# Evaluate the entire population
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit

#print("  Evaluated %i individuals" % len(pop))

# Extracting all the fitnesses of
fits = [ind.fitness.values[0] for ind in pop]

# Variable keeping track of the number of generations
iteration = 0
start = 0
measurement_status = True
while iteration < MAX_ITER:
    #if iteration == 100:
    #    comm.Barrier()
    #    start = time.time()
    #if time.time()-start > 60 and measurement_status:
    #    iteration_passed = iteration - 100
    #    rootdata = comm.gather(iteration_passed,root=0)
    #    if rank == 0:
    #        print(rootdata)
    #    measurement_status = False
    if rank == 0:
        print(iteration)
    iteration = iteration + 1
    # Select the next generation individuals
    offspring = toolbox.select(pop, len(pop))
    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):

        # cross two individuals with probability CXPB
        if random.random() < CXPB:
            toolbox.mate(child1, child2)

            # fitness values of the children
            # must be recalculated later
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:

        # mutate an individual with probability MUTPB
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    
    pop[:] = offspring
    best_ind = tools.selBest(pop, 1)[0]
    migrating_ind = []
    
    # send data to initial receivers
    data_carrier = np.asarray(best_ind)
    if TOPOLOGY_TYPE == "circle":
        data_carrier = np.append(data_carrier,[rank,RTT])
        comm.Isend(data_carrier, neighbors[0])
        comm.Isend(data_carrier, neighbors[1])
        
        # start data exchange to solve all awaiting data transfers
        while comm.Probe():
            req = comm.Irecv(data_carrier, source = MPI.ANY_SOURCE,tag = MPI.ANY_TAG)
            re = req.Wait()
            data_list = data_carrier.tolist()
            data_list[-1]=data_list[-1]-1
            if data_list[-1] != 0:
                if data_list[-2] == neighbors[0]:
                    data_list[-2] = rank
                    data_carrier = np.asarray(data_list)
                    comm.Isend(data_carrier, neighbors[1])
                else:
                    data_list[-2] = rank
                    data_carrier = np.asarray(data_list)
                    comm.Isend(data_carrier, neighbors[1])
    
                migrating_ind.append(data_list[:-2])
        pop = pop[:len(pop)-len(migrating_ind)] + migrating_ind
    
    elif TOPOLOGY_TYPE == "star" or TOPOLOGY_TYPE == "torus3d":
        for receiver in neighbors:
            comm.Isend(data_carrier, receiver)
        while comm.Probe():
            req = comm.Irecv(data_carrier, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
            re = req.Wait()
            data_list = data_carrier.tolist()
            migrating_ind.append(data_list)
        pop = pop[:len(pop) - len(migrating_ind)] + migrating_ind