#This is my second try of creating a GA, this time it acctually plays the game to evaluate chromosomes
#There is some issu with the code: after running it for a while, I'm able to get the followiing error:
#File "C:/Users/Andrzej/PycharmProjects/EA_new_git/evoman_framework/GA_2nd_try.py", line 91, in crossover
#    c1 = p1[:pt] + p2[pt:]
#ValueError: operands could not be broadcast together with shapes (255,) (10,)

#I understand that there is something wrong with the data structures, so that the crossover was fed a chromosome and a population to cross.
#I can't find the mistake - could you help?





import sys
import os
import random
import numpy as np

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller


headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


experiment_name = 'GA_2nd_try'
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
n_bits = (env.get_num_sensors()+1)*n_hidden_neurons + (n_hidden_neurons+1)*5
n_pop = 100
n_iter = 5
n_candidates = 3
r_cross = 0.9
r_mut = 1/n_bits #the usual, as it says in the tutorial.
dom_u = 1 #upper limit for a gene
dom_l = -1 #lower limit for a gene

#functions
#creates an initial population - a numpy array of numpy arrays. Every one of this np arrays is a chromosome (or chorm for short)
def create():
    pop = np.random.uniform(dom_l, dom_u, (n_pop, n_bits))
    print(pop)
    return pop

#lifted from opt._spec._demo.py, run the simulation, returns fitness function
def evaluate(chrom):
    f,p,e,t = env.play(pcont=chrom)
    return f

#tournament, getting the best chromosomes from the population
def tournament (pop):
    #we choose n_candidates of candidates
    candidates = random.choices(pop, k=n_candidates)
    #we find the strongest of candidates
    winner = candidates[0]
    top = evaluate(winner)
    for chrom in candidates[1:]:
        if evaluate(chrom) > top:
            top = evaluate(chrom)
            winner = chrom
    return winner

#crossover, creating two children of two parents
def crossover(p1, p2):
	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	# check for recombination
	if random.random() < r_cross:
		# select crossover point that is not on the end of the string
		pt = random.randint(1, len(p1)-2)
		# perform crossover
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]

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
    #iteratating over generations
    count = 0
    for gen in range (n_iter):
        count +=1

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
        for n in range (n_pop):
            parents.append(tournament(pop))

        #now we will create a new generation
        children = list()
        for i in range(0, n_pop-1, 2):
            # get selected parents in pairs (no need to shuffle or introduce randomness, since the list is already de facto randomly shuffled
            p1, p2 = parents[i], parents[i + 1]
            # crossover and mutation
            for c in crossover(p1, p2):
                # mutation
                mutation(c)
                #check if not over 1 nor under -1
                for x in c:
                    limits(x)
                # store for next generation
                children.append(c)

       # print("Sum of scores of the parents",sum(scores))
       # chi = 0
       # for chrom in children:
       #     chi += evaluate(chrom)
       # print("sum of scores of the children", chi)
       # print("gain of generation ", count, chi-sum(scores))\

main()