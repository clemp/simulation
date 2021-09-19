import numpy as np
import random

# Roles
# Staff
#  - Staff members
# Core
#  - Core contributors
#  - Bounty contributors
# Casual
#  - Audience
#  - Token holders

# Assign global variables
global num_new_products, product_release_schedule

# Number of steps to simulate
N = 365 # imagine each step is one day in a year

# fixed token supply
num_tokens = 1000
pct_vault = 0.5
pct_market = 1 - pct_vault

num_tokens_vault = int(pct_vault * num_tokens)
num_tokens_market = int(num_tokens - num_tokens_vault)

# treasury parameters
# initial shares were exchanges for 1 crypto/social token
treasury_balance = num_tokens

# Number of different agents in each role
num_staff = 3

num_core_contributors = 6
num_bounty_contributors = 8

num_holders = 100

# Token distribution breakdown
# 80% of token supply held by staff and core contributors
# 20% of token supply held by token holders
# bounty contributors and audience have no tokens from the initial sale
pct_tokens_staff = 0.4
pct_tokens_core = 0.4
pct_tokens_bounty = 0.0
pct_tokens_holders = 0.2

class Agent:
    def __init__(self):
        self.tokens = 0
    
    def countTokens(self) -> int:
        """Return the number of tokens currenty in the agent's personal holdings

        Returns:
            [type]: [description]
        """
        return self.tokens

    def getTokens(self, amt: int) -> None:
        """append `amt` number of tokens to the agents holdings

        Args:
            amt (int): number of tokens to append to the agent's personal holdings
        """
        self.tokens += amt

# Set parameters for the simulation in the `initialize` function
def initialize():

    # First generate agents according to the rules    
    agents_staff = list()
    agents_core = list()
    agents_bounty = list()
    agents_holders = list()

    # Generate staff agents and give tokens according to parameters
    for i in range(num_staff):
        a = Agent()
        ntokens = int(pct_tokens_staff * pct_market * num_tokens) / num_staff
        a.getTokens(ntokens)
        agents_staff.append(a)

    # Generate core agents and give tokens according to parameters
    for i in range(num_core_contributors):
        a = Agent()
        ntokens = int(pct_tokens_core * pct_market * num_tokens) / num_core_contributors
        a.getTokens(ntokens)
        agents_core.append(a)

    # Generate bounty agents and give tokens according to parameters
    for i in range(num_bounty_contributors):
        a = Agent()
        ntokens = int(pct_tokens_bounty * pct_market * num_tokens) / num_bounty_contributors
        a.getTokens(ntokens)
        agents_bounty.append(a)
    
    # Generate holder agents and give tokens according to parameters
    for i in range(num_holders):
        a = Agent()
        ntokens = int(pct_tokens_holders * pct_market * num_tokens) / num_holders
        a.getTokens(ntokens)
        agents_holders.append(a)
        
    print("staff", sum([a.countTokens() for a in agents_staff]))
    print("core", sum([a.countTokens() for a in agents_core]))
    print("bounty", sum([a.countTokens() for a in agents_bounty]))
    print("holders", sum([a.countTokens() for a in agents_holders]))
    
    print("done loading agents")
    print("initialize token value", treasury_balance / num_tokens)

    # Assign a random number of new products/services to be released during the simulated year
    num_new_products = random.randint(4, 15)

    # Create a product release schedule: 1 indicates a product was released in that step
    product_release_schedule = np.random.binomial(1, num_new_products / N, size = N)

# Encode the interactions and dynamics that happen at each simulated step    
def update():
    pass

def observe():
    pass



if __name__ == "__main__":
    initialize()




