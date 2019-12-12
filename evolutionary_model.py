from fisherman import *
from fish_stock import *
from simulation_of_fish import go_fishing
from plot_functions import *

import numpy as np
import matplotlib.pyplot as plt
import warnings
from random import random
import sys

def evolutionary_dynamics(init_population_size, 
                        mutation_rate=1e-2, 
                        t_max=500, 
                        n_generations = 20, 
                        crossover=False):
    
    effort_max = 14.0
    effort_min = 0.0
    effort_resolution = 2
    step_size = (effort_max - effort_min) / init_population_size
    efforts = [step_size * ii for ii in range(init_population_size)]
    efforts = np.round(efforts, effort_resolution)
    
    population = [Fisherman(effort=efforts[i]) for i in range(init_population_size)]
    population_counter = [1000 for ii in range(init_population_size)]# keeps track of the number
                                                             # of individuals of each genotype
    plot_histogram(population, population_counter, 0)
    for t in range(n_generations):
        # check that population and counter is consistent
        if len(population) != len(population_counter):
            raise Exception('population and population_counter inconsistent')
        # population size can vary in time as new genes emerge
        population_size = len(population) # not equal to the number of individuals more like n_species 
        profits = np.zeros((population_size, population_size))
        for fisher in population: # squeeze effort into interval [effort_min, effort_max]
            if fisher.effort > effort_max:
                fisher.effort = effort_max
            elif fisher.effort < 0.0:
                fisher.effort = 0.0

        # all vs all tournament
        for ii in range(population_size):
            for jj in range(ii, population_size):
                total_profit, fish_stock_array, harvest_array = go_fishing(2, max_time=t_max, list_of_fishers=[population[ii], population[jj]])
                profits[ii, jj] = total_profit[0]
        
        population, population_counter = calc_new_population(profits, population, population_counter)
        if len(population) < 2:
            import pdb; pdb.set_trace()
            pass
        sys.stdout.write(f'\r generation: {t}\t nof species: {len(population)}')
        sys.stdout.flush()
        plot_histogram(population, population_counter, t)
    print('done')

def calc_new_population(profits, population, population_counter, mutation_rate=1e-2):
    # return array of proportions of the new
    # np.dstack(np.unravel_index(np.argsort(profits.ravel()), profits.shape))
    scaling_factor = 0.001
    n_individuals = sum(population_counter)
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            scores = [sum(profits[:, ii] * population_counter[ii] / n_individuals) for ii in range(len(profits[0,:]))]
            scores_bar = sum([scores[ii] * population_counter[ii] for ii in range(len(scores))]) / n_individuals
        except Warning as identifier:
            import pdb; pdb.set_trace()
            pass
    extinct_fishers = []
    
    # resize the population in proportion to fitness
    for idx, pop_size in enumerate(population_counter):
        # import pdb; pdb.set_trace()
        pop_update = scaling_factor * (scores[idx] - scores_bar)
        population_counter[idx] += pop_update
        population_counter[idx] = int(population_counter[idx])
        # import pdb; pdb.set_trace()
        if population_counter[idx] < 1:
            extinct_fishers.append(idx)
    #import pdb; pdb.set_trace()
    # remove fishermen versions where all are extinct
    n_popped = 0
    for idx in extinct_fishers:
        population_counter.pop(idx - n_popped)
        population.pop(idx - n_popped)
        n_popped += 1
          
    population, population_counter = mutate_population(population, population_counter)

    return population, population_counter



def mutate_population(population, population_counter, mutation_rate=5e-2):
    
    # create new mutated fishermen
    new_fishers = []
    for idx, fisher in enumerate(population):
        if random() < mutation_rate:
            mutated_fisher = Fisherman()
            mutated_fisher.effort = fisher.effort + np.random.normal()
            new_fishers.append(mutated_fisher)
    
    if len(new_fishers) > 0:
        # add new fishermen to population
        population += new_fishers
        population_counter += [1 for ii in new_fishers]

        # sort the population in ascending effort order
        # idx_effort_order = np.argsort([fisher.effort for fisher in population])
        # population = [population[ii] for ii in idx_effort_order]
        # population_counter = [population_counter[ii] for ii in idx_effort_order]

    return population, population_counter

if __name__ == '__main__':
        population_size = 100
        initialize_plot()
        evolutionary_dynamics(population_size)

