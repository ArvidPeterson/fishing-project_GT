import matplotlib.pyplot as plt

def initialize_plot():
    plt.figure(num=1, figsize=(5, 5))
    plt.ylabel('Frequency')
    plt.xlabel('Effort')

def plot_histogram(population, population_counter, generation):

    # make list of efforts
    effort_in_pop = []
    for fisher in population:
        effort_in_pop.append(fisher.effort)

    # plot histogram
    fig = plt.gcf()
    ax = plt.gca()
    ax.bar(effort_in_pop, population_counter, color='b')
    ax.set_title('Generation '+ str(generation+1))
    ax.set_xlim(0, 14)
    # ax.set_xticks(effort_in_pop)
    plt.draw()
    plt.pause(0.01)