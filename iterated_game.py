import numpy as np
import matplotlib.pyplot as plt
import random
import pickle

from simulation_config import *
from fisherman import Fisherman
from fish_stock import FishStock 
from evolutionary_model_more_players import evolutionary_dynamics, calc_new_population

def iterated_game():
    n_simulations = 100
    n_iterations = 100
    depl_time = np.zeros(n_iterations)
    pop_at_iter = []
    effort_resolution = 2
    depletion_time = np.zeros([n_iterations, n_simulations])
    mean_total_profit = np.zeros([n_iterations, n_simulations])
    mean_effort = np.zeros([n_iterations, n_simulations])

    # init a first population of fishers
    population = init_population()
    #population_fitness = {population[ii]:INIT_POP_FITNESS for ii in range(POPULATION_SIZE)}# keeps track of the number
                                                                                # of individuals of each genotype
    for i_sim in range(n_simulations):
        population = init_population()
        for i_itr in range(n_iterations):
            population, population_fitness, stock, d_time = evolutionary_dynamics(population=population)
            profits = [fisher.calculate_and_set_profit() for fisher in population]
            population, population_fitness = calc_new_population(profits, 
                    population, 
                    population_fitness, 
                    stock = stock, 
                    effort_resolution=effort_resolution)
            depletion_time[i_itr, i_sim] = d_time
            mean_total_profit[i_itr, i_sim] = np.mean([sum(population[ii].profit_history) for ii in range(POPULATION_SIZE)])
            mean_effort[i_itr, i_sim] = np.mean([population[ii].effort for ii in range(POPULATION_SIZE)])
            if d_time == 0:
                break
        print(f'simulation: {i_sim}\n')
        pickle.dump(depletion_time, open('depletion_time.pkl', 'wb'))
        pickle.dump(mean_total_profit, open('mean_total_profit.pkl', 'wb'))
        pickle.dump(mean_effort, open('mean_effort.pkl', 'wb'))
        # population = init_population()
        # depl_time[i_itr] = d_time

def init_population():
    effort_max = EFFORT_MAX
    effort_min = EFFORT_MIN
    effort_resolution = 2
    step_size = (effort_max - effort_min) / POPULATION_SIZE
    # efforts = [step_size * ii for ii in range(POPULATION_SIZE)]
    # efforts = np.round(efforts, effort_resolution)
    # base_effort = 1.0 / POPULATION_SIZE
    
    genes = [[(np.random.rand() - 0.5) * 6, (np.random.rand() - 0.5) * 6] for ii in range(POPULATION_SIZE)]
    population = [Fisherman(gene=genes[i]) for i in range(POPULATION_SIZE)]
    return population
    

if __name__ == '__main__':

    iterated_game()

    