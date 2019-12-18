import matplotlib.pyplot as plt
import numpy as np

def initialize_plot():
    plt.figure(num=1, figsize=(5, 5))
    plt.ylabel('Frequency')
    plt.xlabel('Effort')

    plt.figure(num=2, figsize=(5, 5))
    plt.ylabel('b')
    plt.xlabel('a')

    plt.figure(num=3, figsize=(5, 5))
    plt.ylabel('Stock size')
    plt.xlabel('time')

def plot_histogram(population, population_counter, generation, stock):

    # make list of efforts
    effort_in_pop = []
    score = []
    for i, fisher in enumerate(population):
        effort_in_pop.append(fisher.effort)
        score.append(i)

    # plot histogram
    fig = plt.figure(1)
    fig.clf()
    ax = fig.gca()
    ax.bar(score, effort_in_pop, color='b')
    ax.set_title(f'Time {generation+1} nof species {len(population)}')
    ax.set_xlabel('score')
    ax.set_ylabel('effort')
    # ax.set_xticks(effort_in_pop)
    ax.set_xlim([0, max(max(score), 20)])
    ax.set_ylim([0, 5])
    plt.draw()


    a_vec = [f.gene[0] for f in population]
    b_vec = [f.gene[1] for f in population]
    
    fig = plt.figure(2)
    fig.clf()
    ax = fig.gca()
    ax.scatter(a_vec, b_vec)
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_title('Gene config')
    ax.set_xlim([-3,3])
    ax.set_ylim([-3,3])
    plt.draw()


    fig = plt.figure(3)
    fig.clf()
    ax = fig.gca()
    ax.plot(stock.X_history, color='b')
    ax.set_title(f'Fish stock size')
    ax.set_xlabel('time')
    ax.set_ylabel('stock size')
    ax.set_ylim(0, 5000)
    plt.draw()

    plt.pause(0.01)

