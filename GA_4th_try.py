"""I've decided to re-write our GA from scratch,
in order to improve the clearness and clarity of the code and to eliminate errors.

The structure of this code is as follows:
1. Imports
2. Setting up the environment, in a way that allows to evaluate chromosomes by playing the game against static enemy
3. Hyperparameters
4. Implementing functions: Creating a population, Evaluation, Parent selection, Crossover,
Mutation, Offspring creation, Natural selection
5. The main() function, realising the algorithm

The algorithm structure goes as follows:
A. Create a random population (size X)
B. Choose a parent population out of it (size X)
C. Create an offspring population, using crossover and mutation (size X)
D. Perform natural selection on both parents and offspring populations combined (total size 2X),
until a population of size X prevails
E. Go to point B., repeat until stop.
"""

"""
There are some spots to be improved in this code:

- Some, if not each, of the functions could be optimised (I'm not good with lambda expression, for example, 
and didn't use them at all - stuff like that. I was trying to keep the computation as simple as possible tho)

- The selecion procedure, especially the natural selection, could use some more thought -
there are tons of different ways to approach this procedure, I arbitrarily chose one 
that I found logical and easy to implement. The algorithm can only benefit from a more advised approach. 

- I feel that the algorithm could benefit from object-oriented approach. Creating a class "chromosome" could help
with optimisation. For example, right now we calculate chromosome fitness both at parents selection and at natural selection.
With class "chromosome" we could store it as a parameter and just call it back. 
We could even evaluate a chromosome when creating it, or sth like that!
I feel like this is a solid idea, would love for somebody to try it, despite it being a lot of work and a major architecture change.
 
- I'm really not sure if using the dictionaries is a good call (in the seleciton functions)
I worry that they flatten the data in a way, not sure tho. Somebody smart can confirm/deny?
I'm suspicious, because of the log - in later generations, it seems like a lot less comparing is being done.
 
Feel free to upgrade the code.
Andy
"""





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
n_candidates_parents = 3  # number of candidates to be selected during the parents selection
n_candidates_natural = 5  # number of candidates to be selected during the natural selection
r_cross = 0.9  # crossover rate, the chance that children will be hybrids of their parents (else, they are copies of them)
r_mut = 10 / n_bits  # mutation rate, how likely is it for a gene to mutate
dom_u = 1  # upper limit for a gene
dom_l = -1  # lower limit for a gene

#Stop criteria:
n_iter = 10  # number of iterations we want to run the experiment for (set high for checking the fitness as a stop criterion)
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

# parent_selection(population) returns a new population of selected parents.
# New population size is equal to input population size.
# Parents are chosen semi-randomly: a number (n_candidates_best hyperparameter)
# of candidates is drawn and the best one of them becomes a part of parent population.
"""
This function might not be optimal. I had to change every chromosome into a bitstring and then back into np array,
since np.arrays are not hashable and as such cannot be keys in the dictionary.
An implementation without the dictionary might be nice.

Same goes for natural_selection, as it's basically a copy of parent_selection
"""
def parent_selection(population):
    parents = [] #creates an empty list, to store chosen chromosomes
    scores = dict()
    # for optimisation reasons, a dictionary of chromosome scores is created
    # (keys: chromosomes.tobytes(), values: fitnesses)
    # Once the chromosome is evaluated, it's score will be stored there, for easy and fast access.
    for n in range(n_pop): #iterating n_pop times, choosing one chromosome each time
        candidates = random.choices(population, k=n_candidates_parents) #choosing k candidates, at random
        candidates_scores = dict()  # ceating a new dictionary for keeping the candidates' scores
        for chromosome in candidates:
            if chromosome.tobytes() in scores:
                candidates_scores[chromosome.tobytes()] = scores[chromosome.tobytes()]
                #If it's been already tested, we take the stored value
            else:
                candidates_scores[chromosome.tobytes()] = evaluate(chromosome) #checking the fitness
                if candidates_scores[chromosome.tobytes()] > min_fit:
                    print("A good chromosome is: ", chromosome) #print for now, can be easily changed into breaking from the function and returning the chromosome
                    print("With a fitness of: ", candidates_scores[chromosome.tobytes()] )
                scores[chromosome.tobytes()] = candidates_scores[chromosome.tobytes()] #storing it for later
        winner = max(candidates_scores, key = candidates_scores.get) #the winner is the chromosome with the highest candidate score
        parents.append(np.fromstring(winner)) #we add a winner to our parents population
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

# create_offspring(parents) creates an offspring population (the same size as parents population),
# by performing crossover on pairs of parents and mutating the resulting chromosomes
def create_offspring(parents):
    offspring = [] #new list, for storing children
    for i in range(0, len(parents), 2):
        p1, p2 = parents[i], parents[i + 1]
        c1, c2 = crossover(p1, p2)
        mutate(c1)
        mutate(c2)
        offspring.append(c1)
        offspring.append(c2)
    return np.array(offspring)

# Natural selection, combining both parents and offspring populations,
# eliminating the worst until 1/2 of original quantity prevails
# the function is mostly a copy of parents_selection
def natural_selection(parents, offspring):
    initial_population = np.concatenate((parents, offspring), axis=0)
    random.shuffle(initial_population) #crucial, so we can choose only from the first half of shuffled population without loss of generality.
    desired_size = int(len(initial_population) / 2)
    scores = dict()
    survivors = []
    for n in range(desired_size):  # iterating desired_size times
        candidates = random.choices(initial_population, k=n_candidates_natural)  # choosing k candidates, at random
        candidates_scores = dict()  # ceating a new dictionary for keeping the candidates' scores
        for chromosome in candidates:
            if chromosome.tobytes() in scores:
                candidates_scores[chromosome.tobytes()] = scores[chromosome.tobytes()]
                # If it's been already tested, we take the stored value
            else:
                candidates_scores[chromosome.tobytes()] = evaluate(chromosome)  # checking the fitness
                scores[chromosome.tobytes()] = candidates_scores[chromosome.tobytes()]  # storing it for later
        winner = max(candidates_scores,
                     key=candidates_scores.get)  # the winner is the chromosome with the highest candidate score
        survivors.append(np.fromstring(winner))  # we add a winner to our surviviors population
        random.shuffle(survivors)
    return np.array(survivors)





def main():

    count = 0
    while count < n_iter:
        count+=1
        if count ==1:
            pop = create()
        else:
            pop = survivors
        print("Generation: ", count)
        parents = parent_selection(pop)
        offspring = create_offspring(parents)
        survivors = natural_selection(parents, offspring)


main()