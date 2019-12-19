import numpy as np
import matplotlib.pyplot as plt
import random

from simulation_config import *
from fisherman import Fisherman
from fish_stock import FishStock 
from evolutionary_model_more_players import evolutionary_dynamics

def iterated_game():
    n_iterations = 1000
    depl_time = np.zeros(n_iterations)
    pop_at_iter = []

    # init a first population of fishers
    population = init_population()
    #population_fitness = {population[ii]:INIT_POP_FITNESS for ii in range(POPULATION_SIZE)}# keeps track of the number
                                                                                # of individuals of each genotype

    for i_itr in range(n_iterations):
        pop, pop_fitness, d_time = evolutionary_dynamics(population=population)
        population = init_population()
        depl_time[i_itr] = d_time

def init_population():
    effort_max = EFFORT_MAX
    effort_min = EFFORT_MIN
    effort_resolution = 2
    step_size = (effort_max - effort_min) / POPULATION_SIZE
    efforts = [step_size * ii for ii in range(POPULATION_SIZE)]
    efforts = np.round(efforts, effort_resolution)
    # base_effort = 1.0 / POPULATION_SIZE
    
    genes = [[(np.random.rand() - 0.5) * 6, (np.random.rand() - 0.5) * 6] for ii in range(POPULATION_SIZE)]
    population = [Fisherman(gene=genes[i]) for i in range(POPULATION_SIZE)]
    return population
    

if __name__ == '__main__':

    iterated_game()

    