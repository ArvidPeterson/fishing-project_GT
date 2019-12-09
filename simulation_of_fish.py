from fisherman import *
from fish_stock import *
import numpy as np

def main():

    nbrPlayers = 2
    list_of_fishers = []
    for i in range(nbrPlayers):
        list_of_fishers.append(Fisherman())

    fish_stock = FishStock()
    fish_stock.X = 10

    for t in range(10):
        fish_stock.fish_stock_change(list_of_fishers)
        print(fish_stock.X)


if __name__ == '__main__':
    main()