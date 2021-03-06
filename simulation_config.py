# Define macros defining sikmulation, use to this 
# file have convenient way of setting hyperparameters
    
# Simulation loop
POPULATION_SIZE = 50
INIT_POP_FITNESS = 100
MAX_SIM_TIME = 1000
MUTATION_RATE = 1e-2
EFFORT_MAX = 14
EFFORT_MIN = 0
MUTATION_VARIANCE = 0.5
POPULATION_SCALING_FACTOR = 0.1

# fisherman class
PRICE_PER_HARVEST = 20
COST_PER_EFFORT =1


# fish stock
# INIT_STOCK_SIZE = 5e4
GROWTH_RATE = 1e-1
CARRYING_CAP = 5e4
CATCH_COEFF = 1e-2
