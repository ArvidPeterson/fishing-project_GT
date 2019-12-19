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


def update_effort(stock, list_of_fishers):

    nbr_fishers = len(list_of_fishers)
    total_effort = sum([fisher.effort for fisher in list_of_fishers])   
    # effort_bar = total_effort/nbr_fishers
    effort_bar = np.median([fisher.effort for fisher in list_of_fishers])
    
    # calculate effort for every player and calculate profit
    for fisher in list_of_fishers:
        # effort_bar_fisher = (effort_bar*nbr_fishers-fisher.effort)/(nbr_fishers-1)
        # fisher.effort = fisher.gene[0]+fisher.gene[1]*effort_bar_fisher
        fisher.update_effort(E_bar=effort_bar, n_players=len(list_of_fishers))


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
            # ij_profit, round_fish_stock, ij_harvest = update_effort(nbr_players, max_time, effort_of_round)

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
    # main func
    main()