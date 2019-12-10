class Fisherman():

    def __init__(self, effort=0):
        self.effort = effort
        self.price_per_harvest = 50
        self.cost_per_effort = 30
        self.harvest = 0
        self.profit = 0

    def calculate_profit(self):
        self.profit = self.price_per_harvest*self.harvest - self.cost_per_effort*self.effort
