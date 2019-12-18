class FishStock:

    def __init__(self, init_stock_size=0):

        # Todo: Set reasonable parameter values
        self.carrying_cap = 5000
        self.growth_rate = 0.1
        self.catch_coeff = 0.01
        self.X = init_stock_size
        self.X_history = []

    def fish_stock_change_update_fisher_harvest(self, list_of_fishers):
        sum_of_harvest = 0
        for fisher in list_of_fishers:  # Update harvest for every fisher
            fisher.harvest = self.catch_coeff * fisher.effort * self.X
            sum_of_harvest += fisher.harvest

        stock_change = self.logistic_growth() - sum_of_harvest
        self.X += stock_change

        if self.X < 0:  # Fish stock cannot be negative
            self.X = 0

    def logistic_growth(self):
        return self.growth_rate*self.X*(1 - self.X / self.carrying_cap)