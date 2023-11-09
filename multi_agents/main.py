from . import *

NUM_AGENTS = 4
NUM_COMMUNITIES = 2

def main():
    society = Society("economy")

    # First create communities
    for _ in range(NUM_COMMUNITIES):
        society.add_community()


    # Create agents
    for i in range(NUM_AGENTS):
        society.add_agent(None, i % 2)
    
    # Create chatgroups
    for i in range(NUM_COMMUNITIES):
        society.add_chatgroup(f"chatgroup_{i}", "community", i)
    
    # For each pair of agents from rival communities, create a private chatgroup
    for agent0 in society.communities[0]:
        for agent1 in society.communities[1]:
            tmp_cg = society.add_chatgroup(f"chatgroup_{agent0}_{agent1}", "private")
            tmp_cg.add_agents(agent0, agent1)

    # Start chatting
    for _ in range(10):
        society.chat() # TODO: chat() function