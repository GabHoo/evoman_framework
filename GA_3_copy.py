
import sys
import os
import random
import numpy as np
from Chrom import Chrom
from Chrom import Population

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller

headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

#I changed it to 3rd_try name
experiment_name = 'GA_3rd_try'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

n_hidden_neurons = 10

# initializes simulation in individual evolution mode, for single static enemy.
env = Environment(experiment_name=experiment_name,
                  enemies=[2],
                  playermode="ai",
                  player_controller=player_controller(n_hidden_neurons),
                  enemymode="static",
                  level=2,
                  speed="fastest")

# default environment fitness is assumed for experiment

env.state_to_log() # checks environment state





#hyperparameters
n_bits = (env.get_num_sensors()+1)*n_hidden_neurons + (n_hidden_neurons+1)*5 #whatsupp with this instruction
#^ it's lifted from the demo, I heard it was explained on the Q&A, still havent found it.
n_pop = 10
n_iter = 5
n_candidates = 3
r_cross = 0.9
r_mut = 1/n_bits #the usual, as it says in the tutorial.s
dom_u = 1 #upper limit for a gene
dom_l = -1 #lower limit for a gene

population_registry = []

#functions
def simulation(chrom):
    f,p,e,t = env.play(pcont=chrom)
    return f

def testing_pop(pop):
    for i in range (len(pop.chrom_list)):
        pop.chrom_list[i].fitness = simulation(pop.chrom_list[i].genome)

#crossover, creating two children of two parents
def crossover(genome1, genome2):
	# children are copies of parents by default
    c1, c2 = genome1.copy(), genome2.copy()
	# check for recombination
    if random.random() < r_cross:
		# select crossover point that is not on the end of the string
        pt = random.randint(1, len(genome1)-2)
		# perform crossover
        c1 = np.concatenate((genome1[:pt],genome2[pt:]),axis=None)
        c2 = np.concatenate((genome1[:pt],genome2[pt:]),axis=None)

    return Chrom(c1), Chrom(c2)


def evolution(pop):
    
    next_gen = Population(0,0)
    x = int(pop.getsize()/2)
    #we will cross over the best half, and discard the other
    for i in range(x): 
        c1, c2 = crossover(pop.chrom_list[i].genome, pop.chrom_list[i+1].genome)
        next_gen.add_chroms([c1, c2])
        next_gen.mutation(r_mut)
    testing_pop(next_gen)
    next_gen.sort_by_fitness()
    population_registry.append(testing_pop(pop))

    return next_gen









'''
IDEA:

like in Natural Selection
the chroms with best fitness have a much bigger change of reproduction
the chroms who don't even survive should be eliminated 
or if they don't reach a minimum fitness point
'''





def main():
    i=0
    pop = Population(n_pop, n_bits)
    testing_pop(pop)
    pop.sort_by_fitness()
    print("initial Pop")
    pop.show()

    population_registry.append(testing_pop(pop))
    while i<3:
        next_pop = evolution(pop)
        print("Pop :", i)
        next_pop.show()
        i+=1



main()