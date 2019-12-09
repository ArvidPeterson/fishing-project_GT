class Fisherman:

    def __init__(self):
        self.effort = 1
        self.price_per_harvest = 1
        self.cost_per_effort = 1
        self.harvest = 0
        self.profit = 0

    def calculate_profit(self):
        self.profit = self.price_per_harvest*self.harvest - self.cost_per_effort*self.effort