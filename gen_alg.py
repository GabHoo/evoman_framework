import numpy as np
import sys, os
sys.path.insert(0, 'evoman')
from evoman.environment import Environment
from demo_controller import player_controller


#Environment Attributes
number_of_enemies = 2
n_hidden_neurons = 3

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
chrom_len = n_bits = (env.get_num_sensors()+1)*n_hidden_neurons + (n_hidden_neurons+1)*5

#creates a chrom (numpyarray) with "chrom_len" size 
def create_chrom():
    chrom = np.random.uniform(-1, 1, chrom_len)
    return chrom

#create a population (list of chroms)
def generate_pop(chrom_list_len):
    chrom_list=[]
    for _ in range(chrom_list_len):
        chrom = create_chrom()
        chrom_list.append(chrom)
    return chrom_list

#simulation to get the fitness of each Chrom
def simulation(env,x):
    f,p,e,t = env.play(pcont=x)
    return f

# evaluation
def evaluate(x):
    return np.array(list(map(lambda y: simulation(env,y), x)))

def main():
    first_genaration = generate_pop(1)
    #print(first_genaration)
    #print("-----------------------")
    #print(simulation(env,first_genaration[0]))
    print("-----------------------")
    print(evaluate(first_genaration))


if __name__ == '__main__':
    
    main() 