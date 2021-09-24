import numpy as np
import random

class Chrom(object):

    def __init__(self,size,dom_l,dom_u,genome=np.array([]),r_mut=None):

        if genome.size==0: # standard initial creation
            self.genome = np.random.uniform(dom_l, dom_u, size)
            self.fitness = 0
            self.r_mut = np.random.randint(0,1)
        else:     #after crossover creation
            self.genome=genome
            self.r_mut=r_mut


    def __iter__(self):
        return Iterator([self.genome, self.fitness])

    def __str__(self):
        return("Chrom fitness", self.fitness)
    
    def copy(self):
        return self

    def set_fitness(self, fitness):
        self.fitness=fitness
    
    def get_fitness(self):
        return self.fitness
    
    def get_size(self):
        return len(self.genome)

    def get_mutation_rate(self):
        return self.r_mut
    
    def set_mutation_rate(self, mutation_rate):
        self.r_mut=mutation_rate
    
        
    def crossover(self, chrom2, r_cross):
	# children are copies of parents by default
        c1, c2 = self.copy(), chrom2.copy()
        #print("c1", c1, "c2", c2)
        # check for recombination
        if random.random() < r_cross:
            #print("p1", p1, "p2", p2)
            # select crossover point that is not on the end of the string
            pt = random.randint(1, self.get_size()-2)
            
            # perform crossover
        c1 = np.concatenate((self.genome[:pt],chrom2.genome[pt:]),axis=None)
        c2 = np.concatenate((chrom2.genome[:pt],self.genome[pt:]),axis=None)
        return c1, c2
    def mutation (self,r_mut):
        self.genome

class Population(object):
        
    def __init__(self, size, chrom_size):
        self.chrom_list=[]
        if size is not 0:
            for _ in range(size):
                self.chrom_list.append(Chrom(chrom_size))

    def __init__(self, size, chrom_size):
        self.chrom_list=[]
        for _ in range(size):
            self.chrom_list.append(Chrom(chrom_size))

    def __iter__(self):
        return Iterator(self.chrom_list)

    def show(self):
        for chrom in self.chrom_list:
            print(str(chrom.fitness))

    def getsize(self):
        return len(self.chrom_list)
    
    def add_chrom(self,chrom):
        self.chrom_list.append(chrom)

    def sort_by_fitness(self):
        self.chrom_list.sort(key = lambda x: x.fitness, reverse=True)

    def get_best_chrom(self):
        newlist = sorted(self.chrom_list, key=lambda x: x.fitness, reverse=True)
        return newlist.pop(0)
            
class Iterator(object):
   def __init__(self, data_sequence):
       self.idx = 0
       self.data = data_sequence

   def __iter__(self):
       return self

   def __next__(self):
       self.idx += 1
       try:
           return self.data[self.idx-1]
       except IndexError:
           self.idx = 0
           raise StopIteration  # Done iterating.