#ok so first attempt to create what could be our final algorithms. Logs system might be primitive but it is there. Just need to change the format.
#class chromosome is imported so that is fuking easy to sort a chromosome collection by fitness.

"""1. Imports"""
import sys
import os
import random
import numpy as np
import Chrom 
import csv
import argparse

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
                  enemies=[5],
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
pop_size = 4  # quantity of the population - number of chromosomes in our population, not changing during the experiment.
n_parents = pop_size # how many individuals will be selected for parenting
n_candidates_parents = 5  # number of candidates to be selected during the parents selection
n_offspring = 8 # this might be a big number 

r_cross = 0.9  # crossover rate, the chance that children will be hybrids of their parents (else, they are copies of them)
r_mut = 10 / chrom_size  # mutation rate, how likely is it for a gene to mutate
dom_u = 1  # upper limit for a gene
dom_l = -1  # lower limit for a gene

#Stop criteria:
n_iter = 6  # number of iterations we want to run the experiment for (set high for checking the fitness as a stop criterion)
min_fit = 95 # minimal fitness after achieving which we will stop the experiment (set high for running n iterations)


"""4. Implementing functions"""

#create() creates a new population. Size of the population and length of a chromosome controlled by hyperparameters
def create(size_pop,chrom_size):
    chrom_list=[]
    if size_pop!= 0:
        for _ in range(size_pop):
            chrom_list.append(Chrom.Chrom(chrom_size,dom_l,dom_u))
    return chrom_list

# lifted from optimization_specialist_demo.py, evaluate(chromosome) runs the simulation
# with a given chromosome as a seed (bias, input) for the player controller; returns fitness of the run.
def evaluate(chromosome):
    f,p,e,t = env.play(pcont=chromosome.genome)
    chromosome.fitness=f 
    chromosome.p_life=p
    chromosome.e_life=e
    chromosome.time=t
    

        
#evaluate pop
def evaluate_pop(pop):
    for c in pop:
        evaluate(c)
    
        

#get list of fitness
def get_fitnesses(pop):
    fitnesses=[]
    return np.array([c.fitness for c in pop])


"""Evolution fuctionss"""

#selection returns a reduced populetion, we can tune how many in the hyperparameters
def selection(population):
    parents = []
    for n in range(n_parents):
        candidates = random.choices(population, k=n_candidates_parents)
        candidates.sort(key = lambda x: x.fitness, reverse=True)
        winner = candidates[0]
        parents.append(winner)
    return parents
    
#crossover(p1, p2) returns c (one chromosome)
def crossover (p1, p2):
    c=np.empty(chrom_size)
    for i in range(chrom_size):
        c[i] = (p1.genome[i] + p2.genome[i])/ 2 #mean value of his parents values of the very gene   
    r_mut=((p1.r_mut + p2.r_mut) / 2)
    return Chrom.Chrom(chrom_size,dom_l,dom_u,c,r_mut) # creating a chromosome with a genome already (check on Chrom.py constructor)

#mutate mutates the chromosome, 
def mutate (chromosome):
    """ for i in chromosome:
        # check for a mutation
        if random.random() < r_mut:
            # add random number to the gene
            i += np.random.normal(0, 1)
            # then check if it's not over limits
            if i > dom_u:
                i = 1
            if i < dom_l:
                i = -1"""
    return chromosome

def create_offspring(parents):
    offspring = [] #new list, for storing children
    for j in range(int(n_offspring/(n_parents/2))): #based on how many offpring we want: 400? and the pop is 100? then it will iterate 8 times #hopefully they will not be the same bc of mutation
        for i in range(0, len(parents), 2):
            p1, p2 = parents[i], parents[i + 1]
            c = crossover(p1, p2)
            mutate(c)
            offspring.append(c)
    return offspring




def deterministic_selection(pop):
    return pop[:pop_size]



def main():
    improvment = -1 #we set this to -1 bc the first imrpovment will for sure take place (line 206)
    count = 0

    pop = create(pop_size,chrom_size)

    evaluate_pop(pop)
    
    
    pop.sort(key = lambda x: x.fitness, reverse=True)
    
    fitnesses = get_fitnesses(pop) #only usefull for the stats
    
    global_best_f=pop[0].fitness
    global_best_individual=pop[0]

    mean = np.mean(fitnesses)
    std = np.std(fitnesses)
    

    print("\nGeneration: ", count)
    

    #file_aux  = open(experiment_name+'/results.csv','w')
    #file_aux.write('\n\ngen best mean std')
    print( '\n GENERATION '+str(count)+' Best: '+str(round(pop[0].fitness,6))+' Mean: '+str(round(mean,6))+' Standard Deviation '+str(round(std,6)))
    #file_aux.write('\n'+str(count)+' '+str(round(pop[0].fitness,6))+' '+str(round(mean,6))+' '+str(round(std,6))   )
    
    archive=[]
        
    for c in pop:
            archive += [[c.fitness,c.p_life,c.e_life,c.time,count]] #APPENDS THE LINE AS A LIST TO THE LIST OF LINES


    while count < n_iter:
        count+=1
        
        print("\nGeneration: ", count)

        #evolution process
        #print("\nrunning parent's selection..","\n")
        parents = selection(pop)

        print("creating offspring..")
        offspring = create_offspring(parents)
        
        evaluate_pop(offspring)


        new_gen = parents + offspring #ALGORITHM 1 : PARENTS + KIDS
        
        new_gen.sort(key = lambda x: x.fitness, reverse=True)
    
    
        new_gen = deterministic_selection(new_gen)
        
        best_C=new_gen[0]

        fitnesses = get_fitnesses(new_gen)
    
        mean = np.mean(fitnesses)
        std = np.std(fitnesses)


       
            


        # saves results

        #file_aux.write('\n\ngen best mean std')
        print('\n GENERATION '+str(count)+' Best: '+str(round(new_gen[0].fitness,6))+' Mean: '+str(round(mean,6))+' Standard Deviation '+str(round(std,6)))
        #file_aux.write('\n'+str(count)+' '+str(round(new_gen[0].fitness,6))+' '+str(round(mean,6))+' '+str(round(std,6))   )
        
        if(new_gen[0].fitness>global_best_f):
                global_best_f = new_gen[0].fitness
                global_best_individual=new_gen[0]
                improvment += 1

        pop = new_gen

        for c in pop:
            archive += [[c.fitness,c.p_life,c.e_life,c.time,count]]
     
    #file_aux.close()
    file_best  = open(experiment_name+'/best.txt','w')
    file_best.write("The following best individual has scored a fitness of: "+str(round(global_best_f,6))+ "\n"+repr(global_best_individual.genome))
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
