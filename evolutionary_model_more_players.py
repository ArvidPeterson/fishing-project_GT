from fisherman import *
from fish_stock import *
from simulation_of_fish import update_effort
from plot_functions import *
from simulation_config import *

import numpy as np
import matplotlib.pyplot as plt
import warnings
import random
import sys
import copy



def evolutionary_dynamics(population_size, 
                        mutation_rate=MUTATION_RATE, 
                        #t_max=500, 
                        n_generations = MAX_SIM_TIME,
                        crossover=False):

    effort_max = EFFORT_MAX
    effort_min = EFFORT_MIN
    effort_resolution = 2
    step_size = (effort_max - effort_min) / population_size
    efforts = [step_size * ii for ii in range(population_size)]
    efforts = np.round(efforts, effort_resolution)
    base_effort = 1.0 / population_size
    
    genes = [[(np.random.rand() - 0.5) * 6, (np.random.rand() - 0.5) * 6] for ii in range(population_size)]
    # init population
    population = [Fisherman(gene=genes[i]) for i in range(population_size)]
    population_fitness = {population[ii]:INIT_POP_FITNESS for ii in range(population_size)}# keeps track of the number
                                                                                    # of individuals of each genotype
    # init fish stock
    stock = FishStock(init_stock_size=5000)
    stock.X_history.append(stock.X)

    # init 
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
        stock.fish_stock_change_update_fisher_harvest(population)
        stock.X_history.append(stock.X)

        if stock.X < 1.0:
            print(f'Stock depleated at {t}')
            break
        
        # calculate profit
        profits = [fisher.calculate_profit() for fisher in population]
        population, population_fitness = calc_new_population(profits, population, population_fitness, stock, effort_resolution)
        if len(population) < 2:
            import pdb; pdb.set_trace()
            pass
        sys.stdout.write(f'\r generation: {t}\t nof species: {len(population)}')
        sys.stdout.flush()

        # plot_histogram(population, population_fitness, t, stock)

    # summation_of_profit(population)
    print('done')
    return stock.X_history

def calc_new_population(profits, population, population_fitness, 
            stock, effort_resolution, mutation_rate=MUTATION_RATE):

    scaling_factor = POPULATION_SCALING_FACTOR
    sigma = MUTATION_VARIANCE

    nbr_players = len(population)
    profits_mean = np.mean(profits)

    for i, fisher in enumerate(population):
        # calculate steady state if all players played like fisher i
        steady_all_fisher_i = stock.carrying_cap*(1-(stock.catch_coeff/stock.growth_rate)*fisher.effort*nbr_players)
        population_fitness[fisher] += int(scaling_factor*(fisher.profit - profits_mean) +
                                          (0.0*min(steady_all_fisher_i, 0)))
        fisher.population_history.append(population_fitness[fisher])

    
    
    p = max(len(population)//10, 1)
    pop_fitness_list = [population_fitness[fisher] for fisher in population]
    mean_fitness = np.mean(pop_fitness_list)
    fitness_sort_idx = np.argsort(pop_fitness_list)
    
    for idx in range(p):
        good_fisher = copy.deepcopy(population[fitness_sort_idx[-(idx + 1)]])
        good_fisher.gene[0] += np.round(sigma * np.random.randn(), effort_resolution)
        good_fisher.gene[1] += np.round(sigma * np.random.randn(), effort_resolution)
        population_fitness[good_fisher] = population_fitness[population[idx]]

        shit_fisher = population[fitness_sort_idx[idx]]
        del population_fitness[shit_fisher]
        population.remove(shit_fisher)
        population.append(good_fisher)
    
    for idx in range(p, nbr_players - p):
        if np.random.random() < mutation_rate:
            population[idx].gene[0] += np.round(sigma * np.random.randn(), effort_resolution)
            population[idx].gene[1] += np.round(sigma * np.random.randn(), effort_resolution)

    if len(population) != len(population_fitness):
        import pdb; pdb.set_trace()
        raise Exception('population and population_fitness inconsistent')

    # population, population_fitness = mutate_population(population, population_fitness)

    return population, population_fitness



def mutate_population(population, population_fitness, mutation_rate=MUTATION_RATE):
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
        population_fitness[fisher] = INIT_POP_FITNESS
    return population, population_fitness


def summation_of_profit(population):

    mean_profit_all_fishers = np.zeros(len(population))
    plt.figure(num=4, figsize=(5, 5))
    plt.ylabel('b')
    plt.xlabel('a')

    for i, fisher in enumerate(population):
        if len(fisher.profit_history) > 500: # take away transient
            mean_profit_all_fishers[i] = sum(fisher.profit_history[-500:])/len(fisher.profit_history[-500:])
        else:
            mean_profit_all_fishers[i] = sum(fisher.profit_history) / len(fisher.profit_history)
        print(f'{i}: Gene \t {fisher.gene}, Mean profit: {mean_profit_all_fishers[i]}')

    mean_profit = np.mean(mean_profit_all_fishers)
    for fisher in population:
        plt.scatter(fisher.gene[0], fisher.gene[1], s=0.2*mean_profit_all_fishers[i], color='b', alpha=0.5)

    best_fisher = population[np.argmax(mean_profit_all_fishers)]
    # print(mean_profit_all_fishers)
    # import pdb; pdb.set_trace()

if __name__ == '__main__':
        
        initialize_plot()
        evolutionary_dynamics(POPULATION_SIZE)
        plt.show()

