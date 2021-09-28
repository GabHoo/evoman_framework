import numpy as np
import random

class Chrom(object):

    def __init__(self, genome,r_mut):
        self.genome = genome
        self.r_mut=r_mut
        #after run attributes:
        self.fitness = None
        self.p_life=None
        self.e_life=None
        self.time=None
        

    def __iter__(self):
        return Iterator([self.genome, self.fitness])

    def __str__(self):
        return(str(self.genome))

    """def __str__(self):
        return str("Chrom fitness: " + str(self.fitness))"""

    def copy(self):
        return self
    
    def get_size(self):
        return len(self.genome)

    def mutate (self,r_mut):
        for i in range(self.get_size()):
            if random.random() < r_mut:
                self.genome[i] = random.uniform(-1, 1)	

                
class Population(object):
        
    def __init__(self, size=0, chrom_size=0 ,dom_l=0 ,dom_u=0):
        self.chrom_list=[]
        if size is not 0:
            for _ in range(size):
                genome = np.random.uniform(dom_l, dom_u, chrom_size)
                r_mut=np.random.randint(0,1)
                self.chrom_list.append(Chrom(genome,r_mut))

    def __iter__(self):
        return Iterator(self.chrom_list)
    
    
    def show_f(self):
        for chrom in self.chrom_list:
            print(str(chrom.fitness))

    def get_size(self):
        return len(self.chrom_list)

    def add_chroms(self,chrom):
        if isinstance(chrom, list):
            self.chrom_list.extend(chrom)
        else:
            self.chrom_list.append(chrom)
       
    def sort_by_fitness(self):
        self.chrom_list.sort(key = lambda x: x.fitness, reverse=True)

    def get_best_fitness(self):
        newlist = sorted(self.chrom_list, key=lambda x: x.fitness, reverse=True)
        return newlist.pop(0).fitness
    
    def get_fitness_mean(self):
        return np.mean(np.array([c.fitness for c in self.chrom_list]))
    
    def get_fitness_STD(self):
        return np.std(np.array([c.fitness for c in self.chrom_list]))

    def mutation(self, r_mut):
        for chrom in self.chrom_list:
            #if prob of a chrom to not mutate at all
            chrom.mutate(r_mut)
    def check_equal(self,pop):
        result = True
        if self.get_size() == pop.get_size():
            for i in range (self.get_size()):
                if self.chrom_list[i] != pop.chrom_list[i]:
                    result=False
        else:
            result=False
        return result


            
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