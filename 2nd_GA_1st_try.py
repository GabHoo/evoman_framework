#OK so the idea behind it is not very far from Andy's one but idk.
#basically in every iteration the pop gets smaller (trough classi selection/tournament function) by a certain ammount that we can tune, so far it is the half.
#once you have ideally some of the best individuals you make the fuck like rabbits and mutate the child in order to restablish the initial numner 


#I also changed the function for crossover and now rather than having all the parents generating a child we choose them randomly in the population (?)
#with this method tho, results are slightly worse but I am not sure. Maybe some of you big brains can tell me why

#Maybe I should take care of the fact that the number of the pop cannot just be a random odd number but idk, so be carefull if you change n_pop

#I also in general notice some lack of diversity,  true is that I have been runnign with very low number of chromosoms but idk

"""1. Imports"""
import sys
import os
import random
import numpy as np

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller

"""2. Setting up the enviroment (lifted from optimization_specialist_demo.py)"""
headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

experiment_name = 'GA_4th_try'
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
env.state_to_log()  # checks environment state

"""3. Hyperparameters"""
n_bits = (env.get_num_sensors() + 1) * n_hidden_neurons + (n_hidden_neurons + 1) * 5
n_pop = 16  # quantity of the population - number of chromosomes in our population, not changing during the experiment.
#^ n_pop gotta be even, otherwise we'll get an error while trying to pair chromosomes for crossover!
n_candidates_parents = 5  # number of candidates to be selected during the parents selection

r_cross = 0.9  # crossover rate, the chance that children will be hybrids of their parents (else, they are copies of them)
r_mut = 10 / n_bits  # mutation rate, how likely is it for a gene to mutate
dom_u = 1  # upper limit for a gene
dom_l = -1  # lower limit for a gene

n_survivors = int(n_pop/2) #first wave o survivors, those who get be parents. VERY UGLY CAST TO INT but its fine as long as we assume n_pop is even

#Stop criteria:
n_iter = 5  # number of iterations we want to run the experiment for (set high for checking the fitness as a stop criterion)
min_fit = 95 # minimal fitness after achieving which we will stop the experiment (set high for running n iterations)


"""4. Implementing functions"""

#create() creates a new population. Size of the population and length of a chromosome controlled by hyperparameters
def create():
    population = np.random.uniform(dom_l, dom_u, (n_pop, n_bits))
    #creates a uniformly distributed (from dom_l to dom_u) population in size n_pop x n_bits
    return population

# lifted from optimization_specialist_demo.py, evaluate(chromosome) runs the simulation
# with a given chromosome as a seed (bias, input) for the player controller; returns fitness of the run.
def evaluate(chromosome):
    f,p,e,t = env.play(pcont=chromosome)
    return f

# evaluation
def evaluate_pop(x):
    return np.array(list(map(lambda y: evaluate(y), x)))



#selection returns a reduced populetion, we can tune how many in the hyperparameters

def selection(population):
    parents = []
    for n in range(n_survivors):
        candidates = random.choices(population, k=n_candidates_parents)
        f_candidates = evaluate_pop(candidates)
        winner = np.argmax(f_candidates)
        print("\n", "first lucky survivor has a respectable fitness of: " , max(f_candidates), "\n")
        parents.append(candidates[winner])
    random.shuffle(parents)
    return np.array(parents)
    
#crossover(p1, p2) returns two chromosomes, both of which are children of p1 and p2
def crossover (p1, p2):
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # print("c1", c1, "c2", c2)
    # check for recombination
    if random.random() < r_cross:
        # select crossover point that is not on the end of the string
        pt = random.randint(1, len(p1) - 2)
        # perform crossover
        c1 = np.concatenate((p1[:pt], p2[pt:]), axis=None)
        c2 = np.concatenate((p2[:pt], p1[pt:]), axis=None)
    return [c1, c2]

#mutate mutates the chromosome, adding random numbers to randomly selected genes.
#note that this function doesn't return anything, but rather changes the chromosome itself.
def mutate (chromosome):
    for i in chromosome:
        # check for a mutation
        if random.random() < r_mut:
            # add random number to the gene
            i += np.random.normal(0, 1)
            # then check if it's not over limits
            if i > dom_u:
                i = 1
            if i < dom_l:
                i = -1

# create_offspring(survivors) creates an offspring population sufficient to restablish the original number of individual
# by performing crossover on pairs of parents and mutating the resulting chromosomes
"""def create_offspring(survivors):
    offspring = [] #new list, for storing children
    for i in range(0,(n_pop-n_survivors), 2):
        p1, p2 = survivors[i], survivors[i + 1]
        c1, c2 = crossover(p1, p2)
        mutate(c1)
        mutate(c2)
        offspring.append(c1)
        offspring.append(c2)
    return np.array(offspring)
"""
def create_offspring(survivors):
    offspring = [] #new list, for storing children
    for i in range(0,int(((n_pop-n_survivors)/2)), 2): #n_pop-n_survivors is the number of offsprings that we need to create in order to restablish a full population
        p1 = survivors[np.random.randint(0,len(survivors))]
        p2 = survivors[np.random.randint(0,len(survivors))]
        c1, c2 = crossover(p1, p2)
        mutate(c1)
        mutate(c2)
        offspring.append(c1)
        offspring.append(c2)
    return np.array(offspring)






def main():

    count = 0
    while count < n_iter:
        count+=1
        if count ==1:
            pop = create()
        else:
            pop = new_gen
        print("Generation: ", count)

        print("\n", "running the game for selecting parents","\n")
        survivors = selection(pop)

        print("now we mateee :)")
        offspring = create_offspring(survivors)

        new_gen = np.vstack((survivors,offspring))


main()