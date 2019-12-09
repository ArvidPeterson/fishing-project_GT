class Fisherman:

    def __init__(self):
        self.effort = 0
        self.price_per_harvest = 500
        self.cost_per_effort = 300
        self.harvest = 0
        self.profit = 0

    def calculate_profit(self):
        self.profit = self.price_per_harvest*self.harvest - self.cost_per_effort*self.effort
