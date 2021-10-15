import csv
import os
import pandas as pd
import numpy as np
path = "C:/Users/ASUS/Vs_workspace/VU/Evolutionary_Comp/evoman_framework"

def main():
    gather5BestForEachCross()
    results()
    print("End Test")
    

def results():
    folder_list=[]
    results_list=[]

    #Tests_folder = os.fsencode(path)
    #for folder in os.listdir(Tests_folder):
    #    foldername = os.fsdecode(folder)
    #    folder_list.append(foldername)
    with open(path + '/try3_EA_1/results.csv','r') as f:
        data = np.genfromtxt(f, delimiter=',')
        df = pd.DataFrame(data.flatten())  
        #print(foldername)
        print(df.describe())

def gather5BestForEachCross():


    #Tests_folder = os.fsencode(path)
    #for folder in os.listdir(Tests_folder):
        #foldername = os.fsdecode(folder)
    
    
    with open(path +'/try3_EA_1/results.csv','w') as final:
        writer = csv.writer(final)
        for i in range(1,6):
            with open(path +f'/try3_EA_1/enemy_1/Run_{i}/best_5_f.csv','r') as f:
                reader = csv.reader(f)
                header = []
                header = next(reader)
                header = sorted(header, key=float, reverse=True)

                writer.writerow(header)

main()