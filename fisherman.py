class Fisherman():

    def __init__(self, gene = [0.0, 0.0]):
        self.gene = gene
        self.effort = self.gene[0]
        self.price_per_harvest = 5
        self.cost_per_effort = 10
        self.harvest = 0
        self.profit = 0
        self.population_history = []
        self.profit_history = []
        self.gene_history = []

    def calculate_profit(self):
        
        self.profit = self.price_per_harvest*self.harvest - self.cost_per_effort*self.effort
        self.profit_history.append(self.profit)
        self.gene_history.append(self.gene)
        return self.profit
    
    def update_effort(self, E_bar, n_players=None):

        if n_players:
            E_bar = (E_bar*n_players - self.effort)/(n_players - 1)
            
        self.effort = max(self.gene[0] + self.gene[1]*E_bar, 0)
        self.effort = min(10.0, self.effort)


