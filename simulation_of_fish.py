from fisherman import *
from fish_stock import *
import numpy as np
import matplotlib.pyplot as plt


def stable_solution(list_of_fishers, fish_stock):

    stable_effort_all_players = []
    for i, fisher in enumerate(list_of_fishers):
        if i == len(list_of_fishers)-1:
            effort_of_other_player = list_of_fishers[0].effort
        else:
            effort_of_other_player = list_of_fishers[i+1].effort

        b = fisher.cost_per_effort/(fisher.price_per_harvest*fish_stock.catch_coeff*fish_stock.carrying_cap)
        stable_effort = (fish_stock.growth_rate/(2*fish_stock.catch_coeff))*(1-b)-0.5*effort_of_other_player

        stable_effort_all_players.append(stable_effort)

    return stable_effort_all_players


def main():
    nbr_players = 2
    max_time = 10

    list_of_fishers = []
    for i in range(nbr_players):
        list_of_fishers.append(Fisherman())

    fish_stock = FishStock()
    fish_stock.X = 10

    effort_array = np.zeros([nbr_players, max_time])
    harvest_array = np.zeros([nbr_players, max_time])
    fish_stock_array = np.zeros([max_time])

    # Calculate stable solution
    stable_effort_all = stable_solution(list_of_fishers, fish_stock)
    print("Stable effort: ", stable_effort_all)

    for t in range(max_time):
        fish_stock_array[t] = fish_stock.X

        for i, fisher in enumerate(list_of_fishers):
            effort_array[i, t] = fisher.effort
            harvest_array[i, t] = fisher.harvest

        fish_stock.fish_stock_change(list_of_fishers)

    plt.plot(fish_stock_array)
    plt.show()

if __name__ == '__main__':
    main()