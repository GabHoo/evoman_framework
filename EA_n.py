"""1. Imports"""
import sys
import os
import random
import numpy as np
from Chrom_N import Population
from Chrom_N import Chrom_N
import argparse
import csv
import math

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller

parser = argparse.ArgumentParser()
parser.add_argument("-o","--output_file_folder", help="Add the name of the Experiment", required=True, dest="experiment_name")
parser.add_argument("-e","--enemy", help="Add the enemy list separated by dash", required=True, dest="enemy")
args=parser.parse_args()


"""2. Setting up the enviroment"""
headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


#en = [int(i) for i in args.enemy.split("-")] #OMG IM SUCH A PYTHON SLUT

experiment_name = 'EA_n/'+'enemy_'+ args.enemy+'/'+args.experiment_name
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

n_hidden_neurons = 10

# initializes simulation in individual evolution mode, for single static enemy.
env = Environment(experiment_name=experiment_name,
                  enemies=[int(args.enemy)],
                  #multiplemode="yes",
                  playermode="ai",
                  player_controller=player_controller(n_hidden_neurons),
                  enemymode="static",
                  level=2,
                  speed="fastest",
                  randomini="yes",
                  logs="off")

# default environment fitness is assumed for experiment
env.state_to_log() 

"""3. Hyperparameters"""
#chrom parameters
chrom_size = (env.get_num_sensors() + 1) * n_hidden_neurons + (n_hidden_neurons + 1) * 5
dom_u = 1  # upper limit for a gene
dom_l = -1  # lower limit for a gene
step_max = 1 #max number mutation_step variable can assume

T = 1/math.sqrt(2*math.sqrt(chrom_size))
T_prim= 1/math.sqrt(2*chrom_size) 

pop_size = 4  # quantity of the population - number of chromosomes in our population, not changing during the experiment.
n_offspring = pop_size*2 # this might be a big number 

#Stop criteria:
n_iter = 2 # number of iterations we want to run the experiment for (set high for checking the fitness as a stop criterion)
#min_fit = 85 # minimal fitness after achieving which we will stop the experiment (set high for running n iterations)


"""4. Implementing functions"""

#simulates a play in the game with given chrom
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

def old_crossover (p1, p2):  
    new_genome = np.empty(chrom_size)
    new_mut_step=((p1.mut_step + p2.mut_step) / 2)
    for i in range(chrom_size):
        new_genome[i] = (p1.genome[i] + p2.genome[i])/ 2 #mean value of his parents values of the very gene   
    
    return Chrom_N(new_genome, new_mut_step*np.random.normal(0,T))



def new_crossover (p1, p2):  
    threshold = 0.001 #Minimum Value for the mut_step
    j = 0.1 #mutation parameter 
    k = 0.001 #crossover type parameter
    bias = np.random.normal(0, 1, 1)
    new_genome = np.empty(chrom_size)
    new_mut_steps = np.empty(chrom_size)

    for i in range(chrom_size):
        rand_n =  random.uniform (0,1) 
        if rand_n < k:
            new_genome[i] = random.uniform(-1,1)     
        else:
            rand_n2 =  random.uniform (0.5 - j, 0.5 +j) 
            new_genome[i] = (rand_n2*p1.genome[i] + (1-rand_n2)*p2.genome[i])   
            pre_mut_step = ((p1.mut_step[i] + p2.mut_step[i]) / 2)

            #s1’ (new, mutated s1) = s1_old * e ^ (T’ * BIAS + T * N(0,1))
            new_mut_steps[i] = pre_mut_step * math.exp(T_prim * bias + T * np.random.normal(0,T))

            if new_mut_steps[i] < threshold:
                new_mut_steps[i] = threshold

    return Chrom_N(new_genome, new_mut_steps, bias)

'''
    def discrite_crossover(p1, p2):
    threshold = 0.001 #Minimum Value for the mut_step

    #creating genome
    new_genome = np.empty(chrom_size)
    for i in range(chrom_size):
        rand_n =  random.uniform (0,1)
        if rand_n < 0.5:
            new_genome[i] = p1.genome[i]
        else:
            new_genome[i] = p2.genome[i]
    #calculating mut_step
    new_mut_step = ((p1.mut_step + p2.mut_step) / 2)* math.exp(np.random.normal(0,T))
    if new_mut_step < threshold:
        new_mut_step = threshold

    return Chrom(new_genome, new_mut_step)
'''

def reproduction(parents):
    offspring = Population()
    while offspring.get_size() < n_offspring:
        p1 = parents.chrom_list[random.randint(0,parents.get_size()-1)]
        p2 = parents.chrom_list[random.randint(0,parents.get_size()-1)]
        c = new_crossover(p1, p2)
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
        #selecting the best half
        new_gen = deterministic_selection(new_gen)   

        print( '\n GENERATION '+ str(count)+' Best: ' + str(round(new_gen.chrom_list[0].fitness,6))+' enemy_life: ' +str(round(pop.chrom_list[0].e_life,6))+' Mean: '+str(round(new_gen.get_fitness_mean(),6))+' Standard Deviation '+str(round(pop.get_fitness_STD(),6)))
        
        if new_gen.get_best_fitness() > global_best.fitness:
                global_best = new_gen.chrom_list[0]
                #imrovment += 1
        
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

    np.save(experiment_name+'/best_genome',global_best.genome)

   
    
   
    
main()