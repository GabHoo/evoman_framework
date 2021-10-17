import numpy as np
import sys
import os
sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller
import csv
import matplotlib.pyplot as plt

headless = True
if headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


n_hidden_neurons=10
'''Setting up environment for each enemy'''
env = Environment(enemies=[1,2,3],
        multiplemode="yes",
        playermode="ai",
        player_controller=player_controller(n_hidden_neurons),
        enemymode="static",
        level=2,
        speed="fastest",
        randomini="yes",
        logs="off")


champs=[] 
avarages=[]
for i in range(1,6):
        champ = np.load(f'antonio_comparison/EA_n+/enemy_2-4/Run_'+str(i)+'/best_genome.npy')
        champs.append(champ)
    
for j,c  in enumerate(champs):
        best_5_f=[]
        print(f"EA_n,, Running the best of run ",str(j+1)+" 5 times")
        for z in range(0,5):               
            f,p,e,t=env.play(pcont=c)
            best_5_f.append(f)

        avarages.append(sum(best_5_f)/len(best_5_f))


        """ '''Storing 5 best fitnesses in best_5_f.csv file'''
        with open(f'EA_1/enemy_1-2-3/Run_'+str(j+1)+'/best_5_f.csv','w') as f:
            writer = csv.writer(f)
            writer.writerow(best_5_f)"""

x=[1,2,3,4,5]
y=avarages
plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12)
 
# setting x and y axis range
plt.ylim(1,70)
plt.xlim(1,10)
 
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
 
# giving a title to my graph
plt.title('Some cool customizations!')
 
# function to show the plot

                    
plt.show(block=True)
plt.close('all')