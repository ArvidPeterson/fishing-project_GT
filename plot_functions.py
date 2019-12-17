import matplotlib.pyplot as plt
import numpy as np

def initialize_plot():
    plt.figure(num=1, figsize=(5, 5))
    plt.ylabel('Frequency')
    plt.xlabel('Effort')

    plt.figure(num=2, figsize=(5, 5))
    plt.ylabel('Frequency')
    plt.xlabel('Effort')

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
    ax.set_title('Time '+ str(generation+1))
    ax.set_xlabel('score')
    ax.set_ylabel('effort')
    # ax.set_xticks(effort_in_pop)
    ax.set_xlim([0, max(max(score), 20)])
    plt.draw()

    fig = plt.figure(3)
    fig.clf()
    ax = fig.gca()
    ax.plot(stock, color='b')
    ax.set_title('Stock size at time ' + str(generation + 1))
    ax.set_xlabel('time')
    ax.set_ylabel('stock size')
    ax.set_ylim(0, 5000)
    plt.draw()

    plt.pause(0.01)
    max_effort = max(effort_in_pop)
    player_with_max_effort = np.argmax(effort_in_pop)

