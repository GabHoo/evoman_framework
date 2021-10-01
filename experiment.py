import os
import sys
import numpy as np

sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller
import csv

headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

def main():
    enemy_list=[2,3,4]
    n_hidden_neurons=10

    for enemy in enemy_list:

        champs_1=[]

        for i in range(1,11):
            os.system(f"python ./GA_1.py -o Run_{i} -e {enemy}")
            champ = np.load('GA_1/enemy_'+str(enemy)+'/Run_'+str(i)+'/best_genome.npy')
            champs_1.append(champ)
           
        champs_2=[]

        for i in range(1,11):
            os.system(f"python ./GA_2.py -o Run_{i} -e {enemy}")
            champ = np.load('GA_2/enemy_'+str(enemy)+'/Run_'+str(i)+'/best_genome.npy')
            champs_2.append(champ)
     
        env = Environment(enemies=[enemy],
                    playermode="ai",
                    player_controller=player_controller(n_hidden_neurons),
                    enemymode="static",
                    level=2,
                    speed="fastest",
                    randomini="yes",
                    logs="off")


        for j,c  in enumerate(champs_1):
            best_5_f=[]
            print("GA_1, Running the best of run ",str(j+1)+" 5 times")
            for z in range(0,5):               
                f,p,e,t=env.play(pcont=c)
                best_5_f.append(f)
            with open('GA_1/enemy_'+str(enemy)+'/Run_'+str(j+1)+'/best_5_f.csv','w') as f:
                writer = csv.writer(f)
                writer.writerow(best_5_f)

        for j,c  in enumerate(champs_2):
            best_5_f=[]
            print("GA_2, Running the best of run ",str(j+1)+" 5 times")
            for z in range(0,5):
                f,p,e,t=env.play(pcont=c)
                best_5_f.append(f)
            with open('GA_2/enemy_'+str(enemy)+'/Run_'+str(j+1)+'/best_5_f.csv','w') as f:
                writer = csv.writer(f)
                writer.writerow(best_5_f)
        
                        
main()