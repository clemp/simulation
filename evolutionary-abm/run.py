
from itertools import repeat, product
import networkx as nx
import random


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
    agents = [[] for agent in range(N)]

    # Initialize each agent with representative ideas
    n_init_ideas = 3 # each agent starts with this number of random ideas of length M

    # Fill each agent with `n_init_ideas` number of random ideas
    for agent in agents:
        for i in range(n_init_ideas): # for each initial idea
            idea = tuple()
            for j in range(M): # create a random idea of length M
                idea += (random.randint(0,1),)
            agent.append(idea)

    ## Create the problem space and assign utility values 
    # Problem space consists of all possible M-length bit ideas
    problem_space = list(product([0, 1], repeat=M))

    # Create set of n representative ideas
    n = 5
    
    # error handling
    if n > len(problem_space):
        print("cannot choose more representative ideas than those that exist in the problem space")
        pass
    elif n < 2:
        print("must have at least two representative ideas")
        pass

    representative_ideas = {key : 0 for key in random.sample(problem_space, n)}


    # Assign master utility value to ideas
    for i, (key, value) in enumerate(representative_ideas.items()):
        # step 1: assign 0 and 1 to two of the representative ideas
        if i == 0:
            representative_ideas[key] = 1
        elif i > 1: # default values are 0 so we already have that assignment
            representative_ideas[key] = random.uniform(0, 1)

    # initialize a dictionary to hold the utility values for every idea in the problem space
    master_utility_dict = {key : 0 for key in problem_space}

    ## Place an agent on each node of the network
    print(g)

def update():
    pass

def observe():
    pass

if __name__ == "__main__":
    initialize()
    

