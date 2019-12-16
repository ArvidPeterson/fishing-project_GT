import matplotlib.pyplot as plt

def initialize_plot():
    plt.figure(num=1, figsize=(5, 5))
    plt.ylabel('Frequency')
    plt.xlabel('Effort')

def plot_histogram(population, population_counter, generation):

    # make list of efforts
    effort_in_pop = []
    score = []
    for i, fisher in enumerate(population):
        effort_in_pop.append(fisher.effort)
        score.append(i)


    # plot histogram
    fig = plt.gcf()
    fig.clf()
    ax = plt.gca()
    ax.bar(score, effort_in_pop, color='b')
    ax.set_title('Generation '+ str(generation+1))
    ax.set_xlim(0, 14)
    # ax.set_xticks(effort_in_pop)
    ax.set_xlim([0, max(max(score), 20)])
    plt.draw()
    plt.pause(0.01)