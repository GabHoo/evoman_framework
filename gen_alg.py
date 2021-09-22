import numpy as np
import random
import sys, os
sys.path.insert(0, 'evoman')
from evoman.environment import Environment
from demo_controller import player_controller


#Environment Attributes
number_of_enemies = 2
n_hidden_neurons = 1

experiment_name = 'individual_demo'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

#so the UI doesn't start
headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

# initializing environment
env = Environment(experiment_name=experiment_name,
                  enemies=[number_of_enemies],
                  playermode="ai",
                  player_controller=player_controller(n_hidden_neurons),
                  enemymode="static",
                  level=2,
                  speed="fastest")

env.state_to_log() # checks environment state
print(env.checks_params())

#Chrom Attributes
chrom_len = (env.get_num_sensors()+1)*n_hidden_neurons + (n_hidden_neurons+1)*5

class Chrom():

    def __init__(self):
        self.genome = 0
        self.fitness= 0

    def __iter__(self):
        return (t for t in self)
       
    def create(self):
        self.genome = np.random.uniform(-1, 1, chrom_len)
        return [self.genome, self.fitness]
    def get_size(self):
        return len(self.genome)
    def set_fitness(self, fitness):
        self.fitness=fitness

population_registry = []

#create a population (list of chroms)
def generate_pop(population_number):
    chrom_list=[]
    for _ in range(population_number):
        chrom_list.append(Chrom().create())
    
    population_registry.append(chrom_list)

#simulation to get the fitness of each Chrom
def simulation(env,x):
    f,p,e,t = env.play(pcont=x)
    return f

# evaluation
def evaluate():
    for chrom in population_registry[len(population_registry)-1]:
        chrom[1]=simulation(env,chrom[0])


def single_point_crossover():
    current_pop = sorted(population_registry[len(population_registry)-1], key = lambda x: x[1], reverse=True)
    #get the 3 best chroms
    podio = current_pop[0:3]
    #get the 3 worst chroms
    losers = current_pop[-4:-1]

    #the 1º will cross info with the 3 worst ones
    #the 2º with the 2 worst ones
    #the 3º with the 3º worst

    #foreach Chrom
    #we select a random number of genes to change between genome.size/2 to genome.size
    #we save the changes in tuples (place of the gene, gene number)
    #them we will insert the genes from the best chrom, on the worst ones, in the same location
    #repeat this porcess to the rest of chromossomes 



    for best_chrom in podio:
        i=0
        childs=[]
        number_of_changing_genes=random.randint(5, 15)
        print("number_of_changing_genes", number_of_changing_genes)
        for gene in range(number_of_changing_genes):
            print("i: ",i)
            position = random.randint(0, 30)
            print("position :", position)
            print("worst loser ", losers[i])
            print("HEYYY",losers[i][0][position])

            losers[i][0][position]=0
            """best_chrom[position]"""
            print("worst loser ", losers[i])

        childs.append(losers[0]) 
        i+=1
         

            


    print(best_chrom[1])
    print("podio",podio[0][0][0])

    
    #IDEA: the best 3 parents stay, the rest "dies"
    
def main():
    generate_pop(7)
    evaluate()
    single_point_crossover()


if __name__ == '__main__':
    main() 