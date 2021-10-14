import os
import sys
import numpy as np
import time

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller
import csv

headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


'''
This file will, with each enemy, run 10 times both GAs on the setted up environment
Then the "champion" of each run will be load to 'champs' list
Finally the five best fitnesses of the 10 champions wil be saved in best_5_f.csv, for each run
'''

def main():
    start_time = time. time()
    
    enemy_list=[1,2,3]
    n_hidden_neurons=10


    '''Setting up environment for each enemy'''
    env = Environment(enemies=[1,2,3,4,5,6,7,8],
                playermode="ai",
                multiplemode="yes",
                player_controller=player_controller(n_hidden_neurons),
                enemymode="static",
                level=2,
                speed="fastest",
                randomini="yes",
                logs="off")
    #Algorithm Iteration
    #for n in range(1,3):
    n="n"
    champs=[]
    #Run Iteration
    for i in range(1,11):
        os.system(f"python ./EA_n.py -o Run_{i} -e 1-2-3")
        champ = np.load(f'EA_n/enemy_'+"1-2-3"+'/Run_'+str(i)+'/best_genome.npy')
        champs.append(champ)
        
    for j,c  in enumerate(champs):
        best_5_f=[]
        print(f"EA_n, Running the best of run ",str(j+1)+" 5 times")
        for z in range(0,5):
            f,p,e,t=env.play(pcont=c)
            best_5_f.append(f)

        '''Storing 5 best fitnesses in best_5_f.csv file'''
        with open(f'EA_n/enemy_'+"1-2-3"+'/Run_'+str(j+1)+'/best_5_f.csv','w') as f:
            writer = csv.writer(f)
            writer.writerow(best_5_f)
                    
    print("--- %s seconds ---" % (time. time() - start_time))
          
main()