import numpy as np
import random
import math
import sys
import os

from Chrom_N import Chrom_N
sys.path.insert(0, 'evoman')
from evoman.environment import Environment
from demo_controller import player_controller

n_hidden_neurons = 10
headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
# initializes simulation in individual evolution mode, for single static enemy.
env = Environment(experiment_name="experiment_name",
                  enemies=[1],
                  multiplemode="yes",
                  playermode="ai",
                  player_controller=player_controller(n_hidden_neurons),
                  enemymode="static",
                  level=2,
                  speed="fastest",
                  randomini="yes",
                  logs="off")
chrom_size = (env.get_num_sensors() + 1) * n_hidden_neurons + (n_hidden_neurons + 1) * 5

 

def main():
    p1 = Chrom_N(np.random.uniform(-1, 1, chrom_size),np.random.uniform(0, 1, chrom_size),np.random.normal(0, 1, 1))
    p2 = Chrom_N(np.random.uniform(-1, 1, chrom_size),np.random.uniform(0, 1, chrom_size),np.random.normal(0, 1, 1))
    print("PARENT 1")
    print("p1.genome",p1.genome)
    print("p1.mut_step",p1.mut_step)

    print("PARENT 2")
    print("p2.genome",p2.genome)
    print("p2.mut_step",p2.mut_step)
    kid = crossover(p1,p2)

    print("kid")
    print("kid.genome",kid.genome)
    print("kid.mut_step",kid.mut_step)

    Mutated_kid = kid.mutate()

    print("Mutated_kid")
    print("Mutated_kid.genome",Mutated_kid.genome)
    print("Mutated_kid.mut_step",Mutated_kid.mut_step)

def crossover (p1, p2):  

    threshold = 0.01 #Minimum Value for the mut_step

    T = 1/math.sqrt(2*math.sqrt(chrom_size))
    T_prim= 1/math.sqrt(2*chrom_size) 

    j = 0.3 #mutation parameter 

    k = 0.2 #crossover type parameter

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

main()