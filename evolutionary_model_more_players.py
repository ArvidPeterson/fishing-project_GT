from fisherman import *
from fish_stock import *
from simulation_of_fish import update_effort
from plot_functions import *

import numpy as np
import matplotlib.pyplot as plt
import warnings
import random
import sys

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
    population_counter = {population[ii]:100 for ii in range(init_population_size)}# keeps track of the number
                                                                                    # of individuals of each genotype
    # init fish stock
    stock = FishStock(init_stock_size=5000)
    # plot_histogram(population, population_counter, 0)
    stock_size_array = np.zeros(n_generations)

    for t in range(n_generations):
        # check that population and counter is consistent
        if len(population) != len(population_counter):
            import pdb; pdb.set_trace()
            raise Exception('population and population_counter inconsistent')
        # population size can vary in time as new genes emerge
        population_size = len(population) # not equal to the number of individuals more like n_species 
        profits = np.zeros(population_size)

        
        # update efforts depending on others effort at t-1
        update_effort(stock=stock, list_of_fishers=population)
        
        # update harvest for every fisher and change stock size
        stock.fish_stock_change(population)
        if stock.X < 1.0:
            print(f'Stock depleated at {t}')
            break
        
        # calculate profit
        profits = [fisher.calculate_profit() for fisher in population]
        population, population_counter = calc_new_population(profits, population, population_counter)
        if len(population) < 2:
            import pdb; pdb.set_trace()
            pass
        sys.stdout.write(f'\r generation: {t}\t nof species: {len(population)}')
        sys.stdout.flush()
        stock_size_array[t] = stock.X
        # import pdb; pdb.set_trace()
        plot_histogram(population, population_counter, t, stock_size_array[0:t])
    print('done')

def calc_new_population(profits, population, population_counter, mutation_rate=1e-2):

    scaling_factor = 0.1
    

    extinct_fishers = []
    profits_mean = np.mean(profits)

    for i, fisher in enumerate(population):

        population_counter[fisher] += int(scaling_factor*(fisher.profit - profits_mean))
        fisher.population_history.append(population_counter[fisher])
        if population_counter[fisher] < 1:
            del population_counter[fisher]
            extinct_fishers.append(fisher)
    
    n_popped = 0
    for fisher in extinct_fishers:
        population.remove(fisher)

    if len(population) != len(population_counter):
        import pdb; pdb.set_trace()
        raise Exception('population and population_counter inconsistent')

    population = mutate_population(population)

    return population, population_counter



def mutate_population(population, mutation_rate=5e-2):
    sigma = 0.5
    for fisher in population:
        if random.random() < mutation_rate:
            fisher.gene[0] += np.round(sigma * np.random.randn(), 2)
        if random.random() < mutation_rate:
            fisher.gene[1] += np.round(sigma * np.random.randn(), 2)

    return population

if __name__ == '__main__':
        population_size = 10
        initialize_plot()
        evolutionary_dynamics(population_size)
        plt.show()

