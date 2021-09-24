import numpy as np
import random

class Chrom(object):

    def __init__(self, genome):
        self.genome = genome
        self.fitness = 0

    def __iter__(self):
        return Iterator([self.genome, self.fitness])

    def __str__(self):
        return "Chrom Fitness: %s" % (self.fitness)
    
    def copy(self):
        return self
    
    def get_size(self):
        return len(self.genome)

    def mutate (self,r_mut):
        for i in range(self.get_size()):
            if random.random() < r_mut:
                self.genome[i] = random.uniform(-1, 1)	

                
class Population(object):
        
    def __init__(self, size, chrom_size):
        self.chrom_list=[]
        if size is not 0:
            for _ in range(size):
                genome = np.random.uniform(-1, 1, chrom_size)
                self.chrom_list.append(Chrom(genome))

    def __iter__(self):
        return Iterator(self.chrom_list)

    def show(self):
        for chrom in self.chrom_list:
            print(str(chrom.fitness))

    def getsize(self):
        return len(self.chrom_list)
    
    def add_chroms(self,chrom):
        if isinstance(chrom, list):
            self.chrom_list.extend(chrom)
        else:
            self.chrom_list.append(chrom)


    def sort_by_fitness(self):
        self.chrom_list.sort(key = lambda x: x.fitness, reverse=True)

    def get_bests_chrom(self ):
        newlist = sorted(self.chrom_list, key=lambda x: x.fitness, reverse=True)
        return newlist.pop(0)

    def mutation(self, r_mut):
        for chrom in self.chrom_list:
            #if prob of a chrom to not mutate at all
            chrom.mutate(r_mut)

            
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