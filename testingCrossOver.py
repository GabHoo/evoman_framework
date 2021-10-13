import csv
import os
import pandas as pd

def main():
    test()
    print("End Test")
    
def test():

    path = "C:/Users/ASUS/Vs_workspace/VU/Evolutionary_Comp/evoman_framework/CrossOverTests"

    Tests_folder = os.fsencode(path)
    for folder in os.listdir(Tests_folder):
        foldername = os.fsdecode(folder)
        
        with open(path +f'/{foldername}/results.csv','w') as final:
            writer = csv.writer(final)
            for i in range(1,11):
                with open(path +f'/{foldername}/enemy_1/Run_{i}/best_5_f.csv','r') as f:
                    reader = csv.reader(f)
                    header = []
                    header = next(reader)
                    header = sorted(header, key=float, reverse=True)

                    writer.writerow(header)


            #data = {foldername: [{ f'{i}': header}]}
            #df = pd.DataFrame(data)  
            #print(df) 

main()