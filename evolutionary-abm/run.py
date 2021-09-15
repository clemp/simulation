
from itertools import repeat, product
from math import dist
import networkx as nx
import random


# 3.1 Model assumptions
# 3.1.1
# Model assumes that N agents are connected to a finite number of other agents 
# via links through which ideas are exchanged.

seed = 315
random.seed(seed)

def hamming_distance(a: tuple, b: tuple) -> int:
    if len(a) != len(b):
        raise Exception('a and b must be the same length')
    else:
        dist_counter = 0
        for n in range(len(a)):
            if a[n] != b[n]:
                dist_counter += 1
        return dist_counter

def Ut(v: tuple, S: dict) -> float:
    """Returns the utility value for any idea in the problem space.
    If the idea `v` is included in the set of representative ideas `S` then
    the already assigned utility is returned.

    Otherwise the utility is interpolated as a weighted average of the utility
    values from the set of representative ideas.

    Args:
        v (tuple): idea to calculate utility of
        S (dict): {idea: utility value} dict for each idea in the representative

    Returns:
        float: utility value of idea `v` in range [0, 1]
    """
    # if the idea is in the set of representative ideas then
    # return the associated utility value
    if v in S.keys():
        return S[v]
    else:
        ut = sum([S[vi] * pow(hamming_distance(vi, v), -2) for vi in S.keys()]) / sum([pow(hamming_distance(vi, v), -2) for vi in S.keys()])
    return ut


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
    # Problem space consists of all possible M-length bit ideas
    problem_space = list(product([0, 1], repeat=M))

    agents = [[] for agent in range(N)]

    # Initialize each agent with representative ideas
    n_init_ideas = 3 # each agent starts with this number of random ideas of length M

    # Fill each agent with `n_init_ideas` number of random ideas
    for agent in agents:
        ideas = random.choices(problem_space, k = n_init_ideas)
        [agent.append(idea) for idea in ideas]

    # Create set of n representative ideas
    n = 5
    
    # error handling
    if n > len(problem_space):
        print("cannot choose more representative ideas than those that exist in the problem space")
        pass
    elif n < 2:
        print("must have at least two representative ideas")
        pass

    # Create a set of `n` representative ideas
    # Denoted as `S` in the original paper
    # S = {v_i | i = 1...n}
    representative_ideas = {key : 0 for key in random.sample(problem_space, n)}
    # representative_ideas = list(random.sample(problem_space, n))

    # Assign true utility to all ideas in the problem space
    # first assign utility to representative ideas.    

    # select two random index to assign the 1 and 0 value to
    random_idx = random.sample(range(len(representative_ideas.items())), 2)
    for i, (key, value) in enumerate(representative_ideas.items()):
        # step 1: assign 0 and 1 to two of the representative ideas

        if i == random_idx[0]:
            representative_ideas[key] = 0
        elif i == random_idx[1]:
            representative_ideas[key] = 1
        else: # default values are 0 so we already have that assignment
            representative_ideas[key] = random.uniform(0, 1)

    # Create Ut: True utility values that are not known to agents
    true_utility_dict = {idea: Ut(idea, representative_ideas) for idea in problem_space}
    # then interpolate utility for remaining ideas in problem space that are
    # not in the representative ideas, using the Ut function
    # initialize a dictionary to hold the utility values for every idea in the problem space
    master_utility_dict = {key : 0 for key in problem_space}

    # Interpolate utility for the rest of the ideas in the problem space that 
    # were not included in the set of representative ideas
    # {k:v for k,v in E.items() if k not in P}

    ## Place an agent on each node of the network
    print(g)

def update():
    pass

def observe():
    pass

if __name__ == "__main__":
    initialize()
    

