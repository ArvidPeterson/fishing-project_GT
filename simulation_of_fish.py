from fisherman import *
from fish_stock import *
import numpy as np
import matplotlib.pyplot as plt


def stable_solution(list_of_fishers, fish_stock):
    # Calculate stable solution:
    # This means what player i would have to choose for effort Ei
    # to obtain sustainable solution if player j choose effort Ej
    stable_effort_all_players = []
    for i, fisher in enumerate(list_of_fishers):
        if i == len(list_of_fishers)-1:
            effort_of_other_player = list_of_fishers[0].effort
        else:
            effort_of_other_player = list_of_fishers[i+1].effort

        b = fisher.cost_per_effort/(fisher.price_per_harvest*fish_stock.catch_coeff*fish_stock.carrying_cap)
        stable_effort = (fish_stock.growth_rate/(2*fish_stock.catch_coeff))*(1-b)-0.5*effort_of_other_player

        #nash_equilibrium = fish_stock.growth_rate/(3*fish_stock.catch_coeff)*(1-b)
        #print("Nash equilibrium: ", nash_equilibrium)
        stable_effort_all_players.append(stable_effort)

    return stable_effort_all_players

# TODO: maybe change this to a class?
def go_fishing(nbr_players, max_time, effort_of_round=[], list_of_fishers=[]):
    # Assume same effort for all players

    # list_of_fishers = []
    # for i in range(nbr_players):
    #     list_of_fishers.append(Fisherman())
    #     list_of_fishers[i].effort = effort_of_round[i]

    if len(list_of_fishers) < 1:
        list_of_fishers = [Fisherman(effort=effort_of_round[i]) for i in range(nbr_players)]

    fish_stock = FishStock()
    fish_stock.X = 50

    harvest_array = np.zeros([max_time, nbr_players])
    fish_stock_array = np.zeros([max_time])
    total_profit = np.zeros([nbr_players])

    # Calculate stable solution:
    #stable_effort_all = stable_solution(list_of_fishers, fish_stock)
    #print("Stable effort: ", stable_effort_all)

    for t in range(max_time):
        fish_stock_array[t] = fish_stock.X
        fish_stock.fish_stock_change(list_of_fishers)

        for i, fisher in enumerate(list_of_fishers):
            harvest_array[t, i] = fisher.harvest
            fisher.calculate_profit()
            total_profit[i] += fisher.profit

        if fish_stock.X < 1e-10:
            #print("Fish stock depleted at iteration ", t)
            break

    return total_profit, fish_stock_array, harvest_array


def main():

    nbr_players = 2

    # Todo: Set reasonable maximal time and maximal effort
    max_time = 500
    max_effort = 15

    effort_sweep = np.linspace(0, max_effort, num=100)

    profit = np.zeros([len(effort_sweep), len(effort_sweep)])
    fish_stock = np.zeros([max_time, len(effort_sweep), len(effort_sweep)])
    harvest = np.zeros([max_time, len(effort_sweep), len(effort_sweep)])
    for i, i_effort in enumerate(effort_sweep):
        print("Player 1 with effort ", round(i_effort, 2), "against all player 2 efforts.")
        for j, j_effort in enumerate(effort_sweep):
            effort_of_round = [i_effort, j_effort]
            ij_profit, round_fish_stock, ij_harvest = go_fishing(nbr_players, max_time, effort_of_round)

            profit[j, i] = ij_profit[0]
            fish_stock[:, i, j] = round_fish_stock
            harvest[:, i, j] += ij_harvest[:, 0]

    #import pdb; pdb.set_trace()
    fig, ax = plt.subplots(1, 1)
    contour_plot = ax.contourf(effort_sweep, effort_sweep, profit)
    fig.colorbar(contour_plot)
    ax.set_xlabel('Fishing effort player 1')
    ax.set_ylabel('Fishing effort player 2')
    ax.set_title('Profit for player 1')
    plt.show()

if __name__ == '__main__':
    main()