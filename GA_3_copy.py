
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
def evolution():
    pop0 = Population(n_pop, n_bits)
    population_registry.append(testing_pop(pop0))
    print("best fitness: ",pop0.get_best_chrom().get_fitness)
    pop0.sort_by_fitness()
    pop0.show()
    next_gen = Population(0,0)
    x=int(pop0.getsize()/2)
    print(x)
    #we will cross over the best half, and discard the other
    #for chrom1, chrom2 in enumerate(pop0.chrom_list):
    for i in range(x):
        kid1, kid2 = pop0.chrom_list[i].crossover(pop0.chrom_list[i+1], r_cross)
        next_gen.add_chrom(kid1)
        next_gen.add_chrom(kid2)
    print ("next gen: ", next_gen)
    testing_pop(next_gen)
    next_gen.sort_by_fitness()
    next_gen.show()






'''
IDEA:

like in Natural Selection
the chroms with best fitness have a much bigger change of reproduction
the chroms who don't even survive should be eliminated 
or if they don't reach a minimum fitness point
'''

def simulation(chrom):
    f,p,e,t = env.play(pcont=chrom.genome)
    return f

def testing_pop(pop):
    for chrom in pop.chrom_list:
        chrom.fitness = simulation(chrom)

#tournament, getting the best chromosomes from the population
def tournament (pop):
    #we choose n_candidates of candidates
    candidates = random.choices(pop, k=n_candidates)
    for chrom in pop:
        chrom.fitness=evaluate(chrom.genome)
    pop_classification=sorted(pop, key = lambda x: x[1], reverse=True)
    return pop_classification[0]

#crossover, creating two children of two parents

# mutation, adding a random number to some of the numbers in the chrom
def mutation(chrom):
	for i in range(len(chrom)):
		# check for a mutation
		if random.random() < r_mut:
			# flip the bit
			chrom+=np.random.normal(0, 1)

#we don't want any gene (a single number in a chromosome, that's how we call it?) to ba above 1 nor below -1, so we limit it
def limits(x):
    if x>dom_u:
        return dom_u
    elif x<dom_l:
        return dom_l
    else:
        return x

def main():
    evolution()


def main2():
    #iteratating over generations
    count = 0
    for gen in range (n_iter):
        count += 1
        print("GEN is : " , count)


        if count == 1:
            pop = create()
        else:
            pop = children

        #now we can do a tournament - we select k chromosomes at random and choose the best of them
        #we don't just choose the best - idk exacly why, but probly to mimic evolutionary mechanics
        #^ now I get it, we do it so we can preform the tournament n_pop times, without getting the same parent always

        #I'm kinda shady on the details, but I think now we need to pick n_pop parents - so that our generation isn't getting smaller
        #this way, we might pick the same parent many times, I think. I don't think it's a problem, but I might understand it wrong.
        
        parents = []
        
        #parents = pop #line not to make it run forever
        """print("++++++++++++")"""
        for n in range (n_pop):
            parents.append(tournament(pop))
        """print("++++++++++++++")"""
        #now we will create a new generation
        children = []
        for i in range(0, n_pop, 2):
            # get selected parents in pairs (no need to shuffle or introduce randomness, since the list is already de facto randomly shuffled            p1 = parents[i]
            p1, p2 = parents[i], parents[i + 1]
            # crossover and mutation
            
            for c in crossover(p1, p2):
                # mutation
                mutation(c)
                #check if not over 1 nor under -1
                for x in c:
                    limits(x)
                # store for next generation
                #^Basicly I changed it to append array(c) to the children list
                children.append(np.array(c))
        #and then I transformed the list into a big ass array (same shape as pop) to keep the iterations going        
        children = np.stack(children, axis = 0)


main()