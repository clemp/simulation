
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
    """Utility function for `True` value for any idea in the problem space.
    If the idea `v` is included in the set of representative ideas `S` then
    the already assigned utility is returned.

    Otherwise the utility is interpolated as a weighted average of the utility
    values from the set of representative ideas.

    Args:
        v (tuple): idea to calculate utility of
        S (dict): {idea: utility value} dict for each idea in the representative

    Returns:
        float: True utility value Ut of idea `v` in range [0, 1]
    """
    # if the idea is in the set of representative ideas then
    # return the associated utility value
    if v in S.keys():
        return S[v]
    else:
        ut = sum([S[vi] * pow(hamming_distance(vi, v), -2) for vi in S.keys()]) / sum([pow(hamming_distance(vi, v), -2) for vi in S.keys()])
    return ut

def Um(v: tuple, S: dict, beta: float) -> float:
    """Utility function for `Master` value for any idea in the problem space.
    
    Master utility function simulates group-level bias by adding random perturbations 
    to the output of True utility algorithm. 

    Each bit of the idea `v` is flipped with probability 0.25 * beta, and then a random number
    in [-beta, beta] is added to the utility value output of the `True` utility function.

    Larger values of `beta` represent lack of understanding about the problem, while `beta` = 0 
    represents a perfect understanding of the problem.

    Args:
        v (tuple): idea to calculate utility of
        S (dict): 
        beta (float): bias parameter in [0, 1] that flips each bit in the idea with probability 0.25 * beta

    Returns:
        float: Master utility value Um of idea `v` in range [-1, 1]
    """

    # First randomly flip bits of the idea
    nv = tuple([abs(bit - 1) if random.random() > 0.25 * beta else bit for bit in v ])
    
    # Add random number to idea with flipped bits
    um = Ut(nv, S) + random.uniform(-1*beta, beta)
    return um
    
def Uj(v: tuple, S: dict, beta: float, xi: float) -> float:
    """Utility function for `Agent` value for any idea in the idea space.

    Args:
        v (tuple): idea to calculate utility of
        S (dict): {idea: utility value} dict for each idea in the representative
        beta (float): Master utility bias parameter in [0, 1] that flips each bit in the idea with probability 0.25 * beta
        xi (float): parameter that determines variations of utility functions among agents

    Returns:
        float: Agent utility value Uj of idea `v` in range [max(Um(v) - xi, 0), min(Um(v) + xi, 1)]
    """
    um = Um(v, S, beta)

    # Add random perturbation to utility function
    uj = um + xi

    # Logic to keep Uj(v) within range
    if uj < 0:
        uj = 0
    elif uj > 1:
        uj = 1
    
    return uj

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
    xi = 4 # parameter to set amount of heterogeneity among agents
    
    # Fill each agent with `n_init_ideas` number of random ideas
    for agent in agents:
        ideas = random.choices(problem_space, k = n_init_ideas)
        agent_xi = random.uniform(-1, 1) * xi # randomize xi for each agent
        perspective = [ideas, agent_xi]
        [agent.append(perspective) for idea in ideas]

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

    Um((0,1,1,0), representative_ideas, .5)
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
    

