#I'm messing around with the genetic algorithm as seen on: https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/
#gonna write and run it line by line, so I'll get the grip on it
import random

#hyperparameters
n_bits = 5
n_pop = 10
n_iter = 5
n_candidates = 3
r_cross = 0.9
r_mut = 1/n_bits #the usual, as it says in the tutorial.

#functions

#creating a faux evaluation function.
#In our case, it will be the result of the game (which includes both players life and time) of the agent steered by the neural network with wieghts defined by particular chromosome

def evaluate(chrom):
    #basically binary to dec, just to have something for now
    result = 0
    for i in range (len(chrom)):
        result += chrom[i] * 2**i
    return result

#tournament, getting the best chromosomes from the population
def tournament (pop):
    #we choose n_candidates of candidates
    candidates = random.sample(pop, n_candidates)
    #we find the strongest of candidates
    winner = candidates[0]
    top = evaluate(candidates[0])
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

# mutation, flipping some of the 1 into 0 and vice versa
def mutation(bitstring):
	for i in range(len(bitstring)):
		# check for a mutation
		if random.random() < r_mut:
			# flip the bit
			bitstring[i] = 1 - bitstring[i]




#iteratating over generations, leaving 1 for now
count = 0
for gen in range (n_iter):
    count +=1
    #gonna create a population of twenty arrays consisting of five {0,1}s
    #the original code wont work for some reason, working around it
    #the orig:
    #pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]


    #note - that's for my use only, we should surely work on numpy/pandas, arrays and so on. I'm just terrible at it so I'm doing generic data structures.
    if count == 1:
        pop = []
        for i in range(n_pop):
            chrom = []
            for i in range(n_bits):
                chrom.append(random.randint(0,1))
            pop.append(chrom)
    else:
        pop = children


    #Since Ive got different data structure, I'll stick to the tutorial pretty loosely from now on:

    scores = [evaluate(c) for c in pop]
    #we've got a nice list of how good each chromosome in the population is performing

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
            # store for next generation
            children.append(c)

    print("Sum of scores of the parents",sum(scores))
    chi = 0
    for chrom in children:
        chi += evaluate(chrom)
    print("sum of scores of the children", chi)
    print("gain of generation ", count, chi-sum(scores))

