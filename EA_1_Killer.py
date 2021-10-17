"""1. Imports"""
import sys
import os
import random
import numpy as np
from Chrom import Population
from Chrom import Chrom
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


en = [int(i) for i in args.enemy.split("-")] #OMG IM SUCH A PYTHON SLUT

experiment_name = 'EA_1/'+'enemy_'+args.enemy+'/'+args.experiment_name
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

n_hidden_neurons = 10

# initializes simulation in individual evolution mode, for single static enemy.
env = Environment(experiment_name=experiment_name,
                  enemies=en,
                  multiplemode="yes",
                  playermode="ai",
                  player_controller = player_controller(n_hidden_neurons),
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

T = 1/(chrom_size**0.5) 

pop_size = 20  # quantity of the population - number of chromosomes in our population, not changing during the experiment.
n_offspring = pop_size*2 # this might be a big number 

#Stop criteria:
n_iter = 10 # number of iterations we want to run the experiment for (set high for checking the fitness as a stop criterion)
#min_fit = 85 # minimal fitness after achieving which we will stop the experiment (set high for running n iterations)

champs = Population()
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

def crossover (p1, p2):  
    threshold = 0.001 #Minimum Value for the mut_step
    j = 0.3 #mutation parameter 
    k = 0.2 #crossover type parameter
    
    #creating genome
    new_genome = np.empty(chrom_size)
    for i in range(chrom_size):
        rand_n =  random.uniform (0,1) 
        if rand_n < k:
            new_genome[i] = random.uniform (-1,1)     
        else:
            rand_n2 =  random.uniform (0.5 - j, 0.5 +j) 
            new_genome[i] = (rand_n2*p1.genome[i] + (1-rand_n2)*p2.genome[i])   
    
    #calculating mut_step
    new_mut_step = ((p1.mut_step + p2.mut_step) / 2)* math.exp(np.random.normal(0,T))
    if new_mut_step < threshold:
        new_mut_step = threshold

    return Chrom(new_genome, new_mut_step*np.random.normal(0,T))

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
    while offspring.get_size() < parents.get_size()*2:
        p1 = parents.chrom_list[random.randint(0,parents.get_size()-1)]
        p2 = parents.chrom_list[random.randint(0,parents.get_size()-1)]

        c = crossover(p1, p2)
        
        offspring.add_chroms(c)
    offspring.mutation()
    return offspring
    

def deterministic_selection(pop):
    pop.chrom_list = pop.chrom_list[:pop_size]
    return pop

'''
We can do smth like this, tell me if you agree
'''

'''
IDEA

function that iniside a population,
will look at similar familys of fitness,
and will eliminate some of those chroms

To avoid having so many similar fitnesses


'''
# kills the worst genomes, and replace with new best/random solutions
def doomsday(pop,fit_pop):

    worst = int(pop_size/4)  # a quarter of the population
    order = np.argsort(fit_pop)
    orderasc = order[0:worst]

    for o in orderasc:
        for j in range(0,chrom_size):
            pro = np.random.uniform(0,1)
            if np.random.uniform(0,1)  <= pro:
                pop[o][j] = np.random.uniform(dom_l, dom_u) # random dna, uniform dist.
            else:
                pop[o][j] = pop[order[-1:]][0][j] # dna from best

        fit_pop[o]=evaluate([pop[o]])

    return pop,fit_pop
'''  
'''
def retest_specials(pop, last_best_fitness):
    print("RETEST")
    
    real_ones = pop.get_specials(last_best_fitness)
    print("RETEST ENDED")
    return real_ones


    return real_ones

def main():
    
    #improvment = -1 #we set this to -1 bc the first imrpovment will for sure take place (line 206)
    count = 0
    pop = Population(pop_size,chrom_size,dom_l,dom_u)
    testing_pop(pop)
    pop.sort_by_fitness()
    global_best = pop.chrom_list[0]    

    print("Specials of 1st Pop: ")
    specials = pop.get_specials(30, 200)
    specials.sort_by_fitness()


    print( '\n GENERATION '+str(count)+' Best_Fitness: '+str(round(pop.chrom_list[0].fitness,6))+' enemy life: '+str(round(pop.chrom_list[0].e_life,6))+' Mean: '+str(round(pop.get_fitness_mean(),6))+' Standard Deviation '+str(round(pop.get_fitness_STD(),6)))
    if specials.get_size() != 0:
        print( '\n GENERATION '+str(count)+' Best Special: '+str(round(specials.chrom_list[0].fitness,6))+' enemy life: '+str(round(specials.chrom_list[0].e_life,6))+' Mean: '+str(round(specials.get_fitness_mean(),6))+' Standard Deviation '+str(round(specials.get_fitness_STD(),6)))

    archive=[]    
    for c in pop.chrom_list:
            archive += [[c.fitness,c.p_life,c.e_life,c.time,count]] #APPENDS THE LINE AS A LIST TO THE LIST OF LINES
    
    while count < n_iter:
        count+=1
        best_f = pop.get_best_fitness()
        longest_t = pop.get_longest_time()
        print("\nGeneration: ", count)
        #evolution process:

        offspring = reproduction(pop)
        testing_pop(offspring)
        offspring.sort_by_fitness()

        #add any new special  chroms
        print(f"Seaching for Specials in Gen : {count}")
        specials.add_chroms(offspring.get_specials(best_f, longest_t).chrom_list)

        #mix and mutate the genome of these special chroms
        offspring_specials = reproduction(specials)
        testing_pop(offspring_specials)

        #add this resultant offsprings to the main special pop
        specials.chrom_list.extend(offspring_specials.chrom_list)
        specials.sort_by_fitness()
        if specials.get_size()>25:
            specials.chrom_list=specials.chrom_list[:25]
        #retest again the special pop, to make sure they are special and to find any CHAMP
        testing_pop(specials)
        print("RE-TEST: ")
        real_specials = specials.get_specials(best_f, longest_t)

        new_gen = Population()
        new_gen.chrom_list= offspring.chrom_list+ real_specials.chrom_list #ALGORITHM  : KIDS+(PARENTS + KIDS )real killers
        new_gen.sort_by_fitness()
        #selecting the best half
        new_gen = deterministic_selection(new_gen)
        
        best_f=new_gen.get_best_fitness()
        longest_t=new_gen.get_longest_time()
        '''

        Mix plus/comma selection IDEA

        instead of having just one type,
        we would start with one type and
        than if there are no more improvments
        we change to the other one. 

        also we could start using the lack of improvments
        to stop our algorithm, instead of a number of iterations

        '''
         
        print( '\n GENERATION '+ str(count)+' Parents Best : '+str(round(pop.chrom_list[0].fitness,6))+' enemy life: '+str(round(pop.chrom_list[0].e_life,6))+' player life: '+str(round(pop.chrom_list[0].p_life,6))+' Mean: '+str(round(pop.get_fitness_mean(),6))+' Standard Deviation '+str(round(pop.get_fitness_STD(),6)))
        if real_specials.get_size() !=0:
            print( '\n GENERATION '+ str(count)+' Specials Best : '+str(round(real_specials.chrom_list[0].fitness,6))+' enemy life: '+str(round(real_specials.chrom_list[0].e_life,6))+' player life: '+str(round(real_specials.chrom_list[0].p_life,6))+' Mean: '+str(round(real_specials.get_fitness_mean(),6))+' Standard Deviation '+str(round(real_specials.get_fitness_STD(),6)))
        print( '\n GENERATION '+ str(count)+' Offspring Best : '+str(round(offspring.chrom_list[0].fitness,6))+' enemy life: '+str(round(offspring.chrom_list[0].e_life,6))+' player life: '+str(round(offspring.chrom_list[0].p_life,6))+' Mean: '+str(round(offspring.get_fitness_mean(),6))+' Standard Deviation '+str(round(offspring.get_fitness_STD(),6)))
        print( '\n GENERATION '+ str(count)+' New Gen Best : ' + str(round(new_gen.chrom_list[0].fitness,6))+' enemy_life: ' +str(round(new_gen.chrom_list[0].e_life,6))+' player life: '+str(round(new_gen.chrom_list[0].p_life,6))+' Mean: '+str(round(new_gen.get_fitness_mean(),6))+' Standard Deviation '+str(round(new_gen.get_fitness_STD(),6)))

        if new_gen.get_best_fitness() > global_best.fitness:
                global_best = new_gen.chrom_list[0]

        pop = new_gen
        
        for c in pop.chrom_list:
            archive += [[c.fitness,c.p_life,c.e_life,c.time,count]]

    file_best  = open(experiment_name+'/best.txt','w')
    file_best.write("The following best individual has scored a fitness of: "+str(round(global_best.fitness,6))+" enemy life ="+str(round(global_best.e_life,6)) + "\n"+repr(global_best.genome))
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

    if champs.get_size()!=0:
        print("CHamps:")
        for chrom in champs:
            print("chrom.fitness",chrom.fitness, "chrom.e_life", chrom.e_life, "chrom.p_life", chrom.p_life)
    
    
   
    
main()