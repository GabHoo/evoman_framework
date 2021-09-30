import os
import sys
import subprocess
import numpy as np
sys.path.insert(0, 'evoman')
from enviroment import Environment
from demo_controller import player_controller
import csv

headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

def main():
    enemy_list=[1,2,5,7,8]
    bests_GA_1=[]
    bests_GA_2=[]
    n_hidden_neurons=10

    for enemy in enemy_list:
        env = Environment(experiment_name='champ_runs',
                  enemies=[enemy],
                  playermode="ai",
                  player_controller=player_controller(n_hidden_neurons),
                  enemymode="static",
                  level=2,
                  speed="fastest",
                  randomini="yes",
                  logs="off")
        
        for i in range(1,11):
            os.system(f"python ./GA_1.py -o Run_{i} -e {enemy}")
            champ = np.load('GA_1/enemy_'+str(enemy)+'/Run_'+str(i)+'/best_genome.npy')
            best_5_f=[]
            for j in range(0,5):
                f,p,e,t=env.play(pcont=champ)
                best_5_f.append(f)
            with open('GA_1/enemy_'+str(enemy)+'/Run_'+str(i)+'/best_5_f.csv','w') as f:
                writer = csv.writer(f)
                writer.writerow(best_5_f)
                        

        
        for i in range(1,11):
            os.system(f"python ./GA_2.py -o Run_{i} -e {enemy}")
            champ = np.load('GA_2/enemy_'+str(enemy)+'/Run_'+str(i)+'/best_genome.npy')
            best_5_f=[]
            for j in range(0,5):
                f,p,e,t=env.play(pcont=champ)
                best_5_f.append(f)
            with open('GA_2/enemy_'+str(enemy)+'/Run_'+str(i)+'/best_5_f.csv','w') as f:
                writer = csv.writer(f)
                writer.writerow(best_5_f)
                        
            
    

main()

