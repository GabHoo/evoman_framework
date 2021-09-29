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
from enviroment import Environment
from demo_controller import player_controller

parser = argparse.ArgumentParser()
parser.add_argument("-o","--output_file_folder", help="Add the name of the Experiment pls you cunt", required=True, dest="experiment_name")
parser.add_argument("-e","--enemy", help="Add the enemy", required=True, dest="enemy")
args=parser.parse_args()


"""2. Setting up the enviroment (lifted from optimization_specialist_demo.py)"""
headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

experiment_name = 'GA_1/'+args.experiment_name
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

n_hidden_neurons = 10

# initializes simulation in individual evolution mode, for single static enemy.
env = Environment(experiment_name=experiment_name,
                  enemies=[int(args.enemy)],
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
#chrom parameters
chrom_size = (env.get_num_sensors() + 1) * n_hidden_neurons + (n_hidden_neurons + 1) * 5
dom_u = 1  # upper limit for a gene
dom_l = -1  # lower limit for a gene
step_max = 1 #max number mutation_step variable can assume

T = 1/(chrom_size**0.5) 

pop_size = 100  # quantity of the population - number of chromosomes in our population, not changing during the experiment.
n_offspring = 400 # this might be a big number 

#Stop criteria:
n_iter = 15  # number of iterations we want to run the experiment for (set high for checking the fitness as a stop criterion)
#min_fit = 85 # minimal fitness after achieving which we will stop the experiment (set high for running n iterations)


"""4. Implementing functions"""

# lifted from optimization_specialist_demo.py, evaluate(chromosome) runs the simulation
# with a given chromosome as a seed (bias, input) for the player controller; returns fitness of the run.
    
def evaluate(chrom):
    f,p,e,t = env.play(pcont=chrom.genome)
    #eventually with coyuld implement shared fintess punishment
    chrom.fitness=f 
    chrom.p_life=p
    chrom.e_life=e
    chrom.time=t

#evaluate pop
def testing_pop(pop):
    for c in pop.chrom_list:
        evaluate(c)
    

"""Evolution fuctionss"""

def crossover (p1, p2): #crossover only handles lists 
    new_genome = np.empty(chrom_size)
    for i in range(chrom_size):
        new_genome[i] = (p1.genome[i] + p2.genome[i])/ 2 #mean value of his parents values of the very gene   
    new_mut_step=((p1.mut_step + p2.mut_step) / 2)
    return Chrom(new_genome, new_mut_step*T)


def reproduction(parents):
    offspring = Population()
    while offspring.get_size() < n_offspring:
        p1 = parents.chrom_list[random.randint(0,parents.get_size()-1)]
        p2 = parents.chrom_list[random.randint(0,parents.get_size()-1)]
        c = crossover(p1, p2)
        offspring.add_chroms(c)
    offspring.mutation()
    return offspring
    


def deterministic_selection(pop):
    pop.chrom_list = pop.chrom_list[:pop_size]
    return pop


def main():
    #improvment = -1 #we set this to -1 bc the first imrpovment will for sure take place (line 206)
    count = 0

    pop = Population(pop_size,chrom_size,dom_l,dom_u)
    testing_pop(pop)
    pop.sort_by_fitness()
    global_best=pop.chrom_list[0]

    print( '\n GENERATION '+str(count)+' Best: '+str(round(pop.chrom_list[0].fitness,6))+' enemy life: '+str(round(pop.chrom_list[0].e_life,6))+' Mean: '+str(round(pop.get_fitness_mean(),6))+' Standard Deviation '+str(round(pop.get_fitness_STD(),6)))
    
    archive=[]    
    for c in pop.chrom_list:
            archive += [[c.fitness,c.p_life,c.e_life,c.time,count]] #APPENDS THE LINE AS A LIST TO THE LIST OF LINES
    
    while count < n_iter:
        count+=1
        print("\nGeneration: ", count)
        #evolution process:
        #Perform crossover to get offsrping, and mutate it
        offspring = reproduction(pop)
        testing_pop(offspring)
        new_gen = Population()
        new_gen.chrom_list= pop.chrom_list+offspring.chrom_list #ALGORITHM 1 : PARENTS + KIDS
        new_gen.sort_by_fitness()
        new_gen = deterministic_selection(new_gen)   

        print( '\n GENERATION '+ str(count)+' Best: ' + str(round(new_gen.chrom_list[0].fitness,6))+' enemy_life: ' +str(round(pop.chrom_list[0].e_life,6))+' Mean: '+str(round(new_gen.get_fitness_mean(),6))+' Standard Deviation '+str(round(pop.get_fitness_STD(),6)))
        
        '''if new_gen.get_best_fitness() > global_best.fitness:
                global_best = new_gen.chrom_list[0]
                improvment += 1'''
        
        pop = new_gen
        
        for c in pop.chrom_list:
            archive += [[c.fitness,c.p_life,c.e_life,c.time,count]]

    file_best  = open(experiment_name+'/best.txt','w')
    file_best.write("The following best individual has scored a fitness of: "+str(round(global_best.fitness,6))+ "\n"+repr(global_best.genome))
    file_best.close

    header= ['Fitness','Player_Life','Enemy_Life', 'Time','Generataion']

    with open(experiment_name+'/Evolution_Archive.csv','w') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for c in archive:
        # write the data
            writer.writerow(c)
    
main()