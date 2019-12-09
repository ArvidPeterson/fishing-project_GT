class FishStock:

    def __init__(self):

        # Todo: Set reasonable parameter values
        self.carrying_cap = 5000
        self.growth_rate = 0.1
        self.catch_coeff = 0.01
        self.X = 0

    def fish_stock_change(self, list_of_fishers):
        sum_of_harvest = 0
        for i_fisher in list_of_fishers:  # Update harvest for every fisher
            i_fisher.harvest = self.catch_coeff * i_fisher.effort * self.X
            sum_of_harvest += i_fisher.harvest

        stock_change = self.logistic_growth() - sum_of_harvest
        self.X += stock_change

        if self.X < 0:  # Fish stock cannot be negative
            self.X = 0

    def logistic_growth(self):
        return self.growth_rate*self.X*(1 - self.X / self.carrying_cap)