from fisherman import *
from fish_stock import *
from simulation_of_fish import go_fishing

import numpy as np
import matplotlib.pyplot as plt

def evolutionary_dynamics(init_population_size, 
                        mutation_rate=1e-2, 
                        t_max=500, 
                        n_generations = 20, 
                        crossover=False):
    
    E_max = 14.0
    E_min = 0.0
    effort_resolution = 2
    step_size = (E_max - E_min) / init_population_size
    efforts = [step_size * ii for ii in range(init_population_size)]
    efforts = np.round(efforts, effort_resolution)
    
    population = [Fisherman(effort=efforts[i]) for i in range(init_population_size)]
    population_counter = [1 for ii in range(init_population_size)]# keeps track of the number
                                                             # of individuals of each genotype
    for t in range(n_generations):
        #population size can vary in time as new genes emerge
        population_size = len(population) # not equal to the number of individuals more like n_species 
        profits = np.zeros((population_size, population_size))
        for fisher in population: # squeeze effort into interval [E_min, E_max]
            if fisher.effort > E_max:
                fisher.effort = E_max
            elif fisher.effort < 0.0:
                fisher.effort = 0.0

        # all vs all tournament
        for ii in range(population_size):
            for jj in range(ii, population_size):
                total_profit, fish_stock_array, harvest_array = go_fishing(2, max_time=t_max, list_of_fishers=[population[ii], population[jj]])
                profits[ii, jj] = total_profit[0]
        population = calc_new_population(profits, population, population_counter)
    # import pdb; pdb.set_trace()
    print('done')

def calc_new_population(profits, population, population_counter):
    # return array of proportions of the new
    # np.dstack(np.unravel_index(np.argsort(profits.ravel()), profits.shape))
    import pdb; pdb.set_trace()
    n_individuals = sum(population_counter)
    scores = [sum(profits[:, ii] * population_counter[ii] / n_individuals) for ii in range(len(profits[0,:]))]
    pass

def mutate_population(population):
    pass



if __name__ == '__main__':
        population_size = 5
        evolutionary_dynamics(population_size)