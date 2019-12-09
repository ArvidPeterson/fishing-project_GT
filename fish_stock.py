class FishStock:

    def __init__(self):

        self.carrying_cap = 1
        self.growth_rate = 1
        self.catch_coeff = 1
        self.X = 0

    def fish_stock_change(self, list_of_fishers):

        sum_of_harvest = 0
        for i_fisher in list_of_fishers:
            i_fisher.harvest = self.catch_coeff * i_fisher.effort * self.X
            sum_of_harvest += i_fisher.harvest

        dXdt = self.logistic_growth() - sum_of_harvest

        self.X += dXdt


    def logistic_growth(self):

        return self.growth_rate*self.X*(1 - self.X / self.carrying_cap)