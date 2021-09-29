import os


def main():
    enemy_list=[1,2,5,7,8]
    
    for enemy in enemy_list:
        best_ones=[]
        for i in range(0,10):
            best = os.system(f"python ./GA_1.py -o Run{i} -e {enemy}")
            best_ones.append(best)

        
        #for i in range(0,10):
        #   os.system(f"python ./GA_2.py -o Run{i} -e {enemy}")
            
    

main()

