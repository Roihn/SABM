import numpy as np

# Decision Format Processing
def process_decision(agent, question_id, decision):
    agent.decision_reason[question_id] = decision
    try:
        # If decision in line 2 of the response
        if 'reject' in decision.split('\n')[1] or 'reject' in decision.split('\n')[0]:
            agent.decision[question_id] = 0
        elif 'accept' in decision.split('\n')[1] or 'accept' in decision.split('\n')[0]:
            agent.decision[question_id] = 1 
            
        # If decision at the beginning of the response
        elif 'reject' in decision.split(' ')[0]:
            agent.decision[question_id] = 0
        elif 'accept' in decision.split(' ')[0]:
            agent.decision[question_id] = 1
        
        
        # Other Situations
        elif 'reject' in decision:
            agent.decision[question_id] = 0
        elif 'accept' in decision:
            agent.decision[question_id] = 1
        else:
            agent.decision[question_id] = 0
    
    except:
        agent.decision[question_id] = 0
    
    if agent.decision[question_id] == 1:
        print("# Accept")
    else:
        print("# Reject")

# TCU Test Results
def TCU_distribution(agents):
    # TCU Test Data
    HS = [agent.tcu_scale["Hostility"] for agent in agents]
    RT = [agent.tcu_scale["Risk Taking"] for agent in agents]
    SS = [agent.tcu_scale["Social Support"] for agent in agents]
    mean_scores = [np.mean(HS), np.mean(RT), np.mean(SS)]
    tile_25 = [np.percentile(HS, 25), np.percentile(RT, 25), np.percentile(SS, 25)]
    tile_75 = [np.percentile(HS, 75), np.percentile(RT, 75), np.percentile(SS, 75)]
    
    # Empirical Data
    empirical_mean_scores = [25.4, 29.7, 39.5]
    empirical_tile_25 = [20, 24, 37]
    empirical_tile_75 = [31, 34, 43]

    return [mean_scores, tile_25, tile_75, empirical_mean_scores, empirical_tile_25, empirical_tile_75]

# Plea Bargain Results
def group_agents(agents, group_num, situation_num):
    groups = [[[] for _ in range(situation_num)] for _ in range(group_num)]
    
    for agent in agents:
        for qid in range(situation_num):
            if agent.decision[qid] != 2:
                groups[agent.group - 1][qid].append(agent.decision[qid])
    
    return groups

def group_agents_specific(agents, group_num, situation_num):
    groups = [[[] for _ in range(situation_num)] for _ in range(group_num)]
    
    for agent in agents:
        for qid in range(situation_num):
            if agent.decision[qid] != 2:
                groups[0][qid].append(agent.decision[qid])
    
    return groups
