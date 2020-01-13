import numpy as np
import matplotlib.pyplot as plt
import random

from simulation_config import *
from fisherman import Fisherman
from fish_stock import FishStock 
from evolutionary_model_more_players import evolutionary_dynamics
import pickle

def iterated_game():
    n_iterations = 500
    pop_hist = np.zeros([MAX_SIM_TIME + 1,  n_iterations])
    pop_at_iter = []
    
    # init a first population of fishers
    population = init_population()
    #population_fitness = {population[ii]:INIT_POP_FITNESS for ii in range(POPULATION_SIZE)}# keeps track of the number
                                                                                # of individuals of each genotype

    for i_itr in range(n_iterations):
        X_hist = evolutionary_dynamics(population_size=POPULATION_SIZE)
        population = init_population()
        pop_hist[0:len(X_hist),i_itr] = X_hist
        print(f' it no: {i_itr} / {n_iterations}\n')
    
    import pdb; pdb.set_trace()
    pickle.dump(pop_hist, open('fish_stock_hist_penalty.pkl', 'wb'))
    print('done')

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

    