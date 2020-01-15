import matplotlib.pyplot as plt
import numpy as np
from simulation_config import *

# figure numbers
i_gene_plot = 2
i_bar_plot = 0
i_fish_plot = 1

def initialize_plot():
    plt.figure(num=i_bar_plot, figsize=(5, 5))
    plt.ylabel('Frequency')
    plt.xlabel('Effort')


    plt.figure(num=i_fish_plot, figsize=(5, 5))
    plt.ylabel('Stock size')
    plt.xlabel('time')

    plt.figure(num=i_gene_plot, figsize=(5, 5))
    plt.ylabel('b')
    plt.xlabel('a')

def plot_histogram(population, population_counter, generation, stock):
    # make list of efforts  
    effort_in_pop = []
    score = []
    for i, fisher in enumerate(population):
        effort_in_pop.append(fisher.effort)
        score.append(i)

    # plot histogram
    fig = plt.figure(i_bar_plot)
    fig.clf()
    ax = fig.gca()
    ax.bar(score, effort_in_pop, color='b')
    ax.set_title(f'Time {generation+1} nof species {len(population)}')
    ax.set_xlabel('player')
    ax.set_ylabel('effort')
    # ax.set_xticks(effort_in_pop)
    ax.set_xlim([0, max(max(score), 20)])
    ax.set_ylim([0, 5])
    plt.draw()

    # time plot over fish stock size
    fig = plt.figure(i_fish_plot)
    fig.clf()
    ax = fig.gca()
    ax.plot(stock.X_history, color='b')
    ax.set_title(f'Fish stock size: {stock.X_history[-1]}')
    ax.set_xlabel('time')
    ax.set_ylabel('stock size')
    ax.set_ylim(0, CARRYING_CAP)
    plt.draw()

    # scatterplot of genes in population
    a_vec = [f.gene[0] for f in population]
    b_vec = [f.gene[1] for f in population]
    
    fig = plt.figure(i_gene_plot)
    fig.clf()
    ax = fig.gca()
    ax.scatter(a_vec, b_vec)
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_title('Gene config')
    ax.set_xlim([-3,3])
    ax.set_ylim([-3,3])
    plt.grid(True)
    plt.draw()

    plt.pause(1e-5)

def close_all_figure_windows():
    # for ii in range(3):
    #     fig = plt.figure(2)
    plt.close('all')