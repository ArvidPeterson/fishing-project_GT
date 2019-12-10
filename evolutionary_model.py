from fisherman import *
from fish_stock import *
from simulation_of_fish import go_fishing

import numpy as np
import matplotlib.pyplot as plt
import warnings
np.seterr(all='warn')

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
        population, population_size = calc_new_population(profits, population, population_counter)
    import pdb; pdb.set_trace()
    print('done')

def calc_new_population(profits, population, population_counter, mutation_rate=1e-2):
    # return array of proportions of the new
    # np.dstack(np.unravel_index(np.argsort(profits.ravel()), profits.shape))
    scaling_factor = 0.1
    n_individuals = sum(population_counter)
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            scores = [sum(profits[:, ii] * population_counter[ii] / n_individuals) for ii in range(len(profits[0,:]))]
            scores_bar = sum([scores[ii]*population_counter[ii] for ii in range(len(scores))]) / n_individuals
        except Warning as identifier:
            import pdb; pdb.set_trace()
            pass
    extinct_fishers = []
    
    # resize the population in proportion to fitness
    for idx, pop_size in enumerate(population_counter):
        # import pdb; pdb.set_trace()
            population_counter[idx] = pop_size*(1 + scaling_factor * (scores[idx] - scores_bar))
            population_counter[idx] = int(population_counter[idx])
            if population_counter[idx] < 1:
                extinct_fishers.append(idx)
    import pdb; pdb.set_trace()
    # remove fishermen versions where all are extinct
    n_popped = 0
    for idx in extinct_fishers:
        population_counter.pop(idx - n_popped)
        # pop_size.pop(idx)
        population.pop(idx - n_popped)
        n_popped += 1
        

    
    population = mutate_population(population, mutation_rate=1e-2)

    return population, population_counter



def mutate_population(population, mutation_rate=1e-2):
    # mutate population
    return population



if __name__ == '__main__':
        population_size = 20
        evolutionary_dynamics(population_size)