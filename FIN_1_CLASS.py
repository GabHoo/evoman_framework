#ok so first attempt to create what could be our final algorithms. Logs system might be primitive but it is there. Just need to change the format.
#class chromosome is imported so that is fuking easy to sort a chromosome collection by fitness.

"""1. Imports"""
import sys
import os
import random
import numpy as np
from Chrom import Population
from Chrom import Chrom
import argparse
import csv

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller

parser = argparse.ArgumentParser()
parser.add_argument("-o","--output_file_folder", help="Add the name of the Experiment pls you cunt", required=True, dest="experiment_name")
args=parser.parse_args()


"""2. Setting up the enviroment (lifted from optimization_specialist_demo.py)"""
headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

experiment_name = 'FINAL_GA_1/'+args.experiment_name
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

n_hidden_neurons = 10

# initializes simulation in individual evolution mode, for single static enemy.
env = Environment(experiment_name=experiment_name,
                  enemies=[1],
                  playermode="ai",
                  player_controller=player_controller(n_hidden_neurons),
                  enemymode="static",
                  level=2,
                  speed="fastest",
                  randomini="yes",
                  logs="off")

# default environment fitness is assumed for experiment
env.state_to_log()  # checks environment state

"""3. Hyperparameters"""

chrom_size = (env.get_num_sensors() + 1) * n_hidden_neurons + (n_hidden_neurons + 1) * 5
pop_size = 50  # quantity of the population - number of chromosomes in our population, not changing during the experiment.
n_parents = pop_size # how many individuals will be selected for parenting
n_candidates_parents = 5  # number of candidates to be selected during the parents selection
n_offspring = 100 # this might be a big number 

r_cross = 0.9  # crossover rate, the chance that children will be hybrids of their parents (else, they are copies of them)
r_mut = 10 / chrom_size  # mutation rate, how likely is it for a gene to mutate
dom_u = 1  # upper limit for a gene
dom_l = -1  # lower limit for a gene

#Stop criteria:
n_iter = 15  # number of iterations we want to run the experiment for (set high for checking the fitness as a stop criterion)
min_fit = 85 # minimal fitness after achieving which we will stop the experiment (set high for running n iterations)


"""4. Implementing functions"""

# lifted from optimization_specialist_demo.py, evaluate(chromosome) runs the simulation
# with a given chromosome as a seed (bias, input) for the player controller; returns fitness of the run.
    
def evaluate(chromosome):
    f,p,e,t = env.play(pcont=chromosome.genome)
    chromosome.fitness=f 
    chromosome.p_life=p
    chromosome.e_life=e
    chromosome.time=t

#evaluate pop
def testing_pop(pop):
    for c in pop.chrom_list:
        evaluate(c)
    

"""Evolution fuctionss"""

#selection returns a reduced populetion, we can tune how many in the hyperparameters
def selection(pop):
    parents = []
    for n in range(n_parents):
        candidates = random.choices(pop.chrom_list, k=n_candidates_parents)
        candidates.sort(key = lambda x: x.fitness, reverse=True)
        winner = candidates[0]
        parents.append(winner)
    pop.chrom_list = parents

    
#crossover(p1, p2) returns c (one chromosome)
def crossover (p1, p2): #crossover only handles lists (genomes)
    new_genome = np.empty(chrom_size)
    for i in range(chrom_size):
        new_genome[i] = (p1[i] + p2[i])/ 2 #mean value of his parents values of the very gene   
    r_mut=((p1.r_mut + p2.r_mut) / 2)
    return new_genome,r_mut 


def reproduction(parents):

    offspring = Population(0,0)
    for j in range(int(n_offspring/(n_parents/2))): #based on how many offpring we want: 400? and the pop is 100? then it will iterate 8 times #hopefully they will not be the same bc of mutation
        for i in range(0, parents.get_size(), 2):
            p1, p2 = parents.chrom_list[i].genome, parents.chrom_list[i + 1].genome
            new_genome,new_r_mut = crossover(p1, p2)
            offspring.add_chroms(Chrom(new_genome,new_r_mut))
    #offspring.mutation(r_mut)

    return offspring
    


def deterministic_selection(pop):
    pop.chrom_list = pop.chrom_list[:pop_size]
    return pop

def main():
    improvment = -1 #we set this to -1 bc the first imrpovment will for sure take place (line 206)
    count = 0

    pop = Population(pop_size,chrom_size,dom_l,dom_u)
    testing_pop(pop)
    pop.sort_by_fitness()

    print("\nGeneration: ", count)
    #pop.show    

    #file_aux  = open(experiment_name+'/results.csv','w')
    #file_aux.write('\n\ngen best mean std')
    print( '\n GENERATION '+str(count)+' Best: '+str(round(pop.chrom_list[0].fitness,6))+' Mean: '+str(round(pop.get_fitness_mean(),6))+' Standard Deviation '+str(round(pop.get_fitness_STD(),6)))
    #file_aux.write('\n'+str(count)+' '+str(round(pop[0].fitness,6))+' '+str(round(pop.get_fitness_mean(),6))+' '+str(round(pop.get_fitness_STD(),6))   )
    
    while count < n_iter:
        count+=1
        
        print("\nGeneration: ", count)
        #evolution process:
        #Selecting the Chroms to reproduce
        selection(pop)
        #Perform crossover to get offsrping, and mutate it
        offspring = reproduction(pop)
        testing_pop(offspring)
        offspring.mutation(r_mut)
        #print("offspring: ")
        #offspring.show()

        new_gen = Population(0,0)
        new_gen.set_chrom_list(pop.chrom_list+offspring.chrom_list) #ALGORITHM 1 : PARENTS + KIDS
        new_gen.sort_by_fitness()
        #print("new_gen: ")
        #new_gen.show()


        print("POP best fitness: ", pop.get_best_fitness()) 
        print("NEWGEN best fitness: ", new_gen.get_best_fitness()) 
        #new_gen = deterministic_selection(new_gen)
        
        #best_C=new_gen.get_best_chrom()

        # saves results
   
        #file_aux.write('\n\ngen best mean std')
        print( '\n GENERATION '+str(count)+' Best: '+str(round(new_gen.chrom_list[0].fitness,6))+' Mean: '+str(round(new_gen.get_fitness_mean(),6))+' Standard Deviation '+str(round(pop.get_fitness_STD(),6)))
        #file_aux.write('\n'+str(count)+' '+str(round(new_gen[0].fitness,6))+' '+str(round(pop.get_fitness_mean(),6))+' '+str(round(pop.get_fitness_STD(),6))   )
        

        if new_gen.get_best_fitness() > pop.get_best_fitness():
                improvment += 1

        pop = new_gen
     
    #file_aux.close()
    #file_best  = open(experiment_name+'/best.txt','w')
    #file_best.write("The following best individual has scored a fitness of: "+str(global_best_f)+ "\n"+str(global_best_individual))



#print the best and its fitness in another file

    
main()