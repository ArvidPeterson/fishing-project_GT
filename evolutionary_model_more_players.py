from fisherman import *
from fish_stock import *
from simulation_of_fish import update_effort
from plot_functions import *

import numpy as np
import matplotlib.pyplot as plt
import warnings
import random
import sys
import copy

INIT_POP_NUMBER = 100

def evolutionary_dynamics(init_population_size, 
                        mutation_rate=1e-2, 
                        t_max=500, 
                        n_generations = 1000,
                        crossover=False):

    
    effort_max = 14.0
    effort_min = 0.0
    effort_resolution = 2
    step_size = (effort_max - effort_min) / init_population_size
    efforts = [step_size * ii for ii in range(init_population_size)]
    efforts = np.round(efforts, effort_resolution)
    base_effort = 1.0 / init_population_size
    
    genes = [[base_effort, np.round(np.random.randn(), effort_resolution)] for ii in range(init_population_size)]
    # init population
    population = [Fisherman(gene=genes[i]) for i in range(init_population_size)]
    population_fitness = {population[ii]:INIT_POP_NUMBER for ii in range(init_population_size)}# keeps track of the number
                                                                                    # of individuals of each genotype
    # init fish stock
    stock = FishStock(init_stock_size=5000)
    stock.X_history.append(stock.X)

    for t in range(n_generations):
        # check that population and counter is consistent
        if len(population) != len(population_fitness):
            import pdb; pdb.set_trace()
            raise Exception('population and population_fitness inconsistent')

        # update efforts depending on others effort at t-1
        update_effort(stock=stock, list_of_fishers=population)
        for fisher in population:
            population_fitness[fisher] += -1
        
        # update harvest for every fisher and change stock size
        stock.fish_stock_change(population)
        stock.X_history.append(stock.X)

        if stock.X < 1.0:
            print(f'Stock depleated at {t}')
            break
        
        # calculate profit
        profits = [fisher.calculate_profit() for fisher in population]
        population, population_fitness = calc_new_population(profits, population, population_fitness)
        if len(population) < 2:
            import pdb; pdb.set_trace()
            pass
        sys.stdout.write(f'\r generation: {t}\t nof species: {len(population)}')
        sys.stdout.flush()

        plot_histogram(population, population_fitness, t, stock)
    print('done')

def calc_new_population(profits, population, population_fitness, mutation_rate=1e-2):

    scaling_factor = 0.1
    

    extinct_fishers = []
    profits_mean = np.mean(profits)

    for i, fisher in enumerate(population):

        population_fitness[fisher] += int(scaling_factor*(fisher.profit - profits_mean))
        fisher.population_history.append(population_fitness[fisher])
        if population_fitness[fisher] < 1:
            del population_fitness[fisher]
            extinct_fishers.append(fisher)
    
    n_popped = 0
    for fisher in extinct_fishers:
        population.remove(fisher)

    if len(population) != len(population_fitness):
        import pdb; pdb.set_trace()
        raise Exception('population and population_fitness inconsistent')

    population, population_fitness = mutate_population(population, population_fitness)

    return population, population_fitness



def mutate_population(population, population_fitness, mutation_rate=1e-2):
    sigma = 0.5
    new_fishers = []
    for fisher in population:
        if random.random() < mutation_rate:
            new_fisher = copy.deepcopy(fisher)
            new_fisher.gene[0] += np.round(sigma * np.random.randn(), 2)
            # if random.random() < mutation_rate:
            new_fisher.gene[1] += np.round(sigma * np.random.randn(), 2)
            new_fishers.append(new_fisher)

    population += new_fishers
    for fisher in new_fishers:
        population_fitness[fisher] = INIT_POP_NUMBER
    return population, population_fitness

if __name__ == '__main__':
        population_size = 10
        initialize_plot()
        evolutionary_dynamics(population_size)
        plt.show()

