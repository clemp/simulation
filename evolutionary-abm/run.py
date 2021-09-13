
import itertools
import networkx as nx
from itertools import permutations, repeat

# 3.1 Model assumptions
# 3.1.1
# Model assumes that N agents are connected to a finite number of other agents 
# via links through which ideas are exchanged.

seed = 315

def initialize():
    ## Set simulation parameters
    # Total number of steps to iterate the simulation.
    T = 30

    ## Create the group network
    # Define the number of agents
    N = 5

    # Create a Watts-Strogatz small-world graph
    g = nx.watts_strogatz_graph(N, 3, 0.2, seed)
    
    ## Create the problem space
    M = 4 # ideas are M-dimensional binary space
    problem_space = list(itertools.product([0, 1], repeat=M))

    ## Fill each agent with a set of initial ideas

    ## Place an agent on each node of the network
    print(g)

def update():
    pass

def observe():
    pass

if __name__ == "__main__":
    initialize()
    

