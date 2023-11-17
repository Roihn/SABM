import pandas as pd
import matplotlib.pyplot as plt
import random
import os
import datetime
import time

import src.plea_bargain.agent as GPT
import src.plea_bargain.prompt_plea_bargain as Data
import src.plea_bargain.data_initialize as data_initialize
import src.plea_bargain.TCU_test as TCU_test
import src.plea_bargain.data_formatting as data_formatting
import src.plea_bargain.data_plot as data_plot

plt.ion()

# Model Setup
model_ver = "gpt-4-0314" #"gpt-3.5-turbo"
api_key = "sk-"

# Configuration
task_run_dict = {
    "TCU": False,
    "DA": True,
}
usecase_dict = {
    "Task_TCU": {
        'Persona': 'persona',
        # persona: Perform TCU Test with persona
        # nopersona: Perform TCU Test without persona
    },
    "Task_Plea_Bargain":{
        'Scenario':{
            'Persona': 'persona',
            # persona: Perform Plea Bargain Task with persona
            # nopersona: Perform Plea Bargain Task without persona
            'Presumption': 'Default',
            # 'Default': Plea Bargain Default Scenario
            # 'Presumption': Plea Bargain Scenario with the presumption of innocence
            # ('P1', 'P2', 'P5'): Paper Scenarios
        },
        'Fewshot': True
        # True: Use few-shot
        # False: Default (does not use few-shot)
    },
}
output_max_tokens = 64

# Prompt
prompts = Data.prompts

# Data
## Scenario Labels
ScenarioBase = Data.ScenarioBase
QuestionBase = Data.QuestionBase
xlabelBase = Data.xlabelBase
ylabelBase = Data.ylabelBase

# Agent Initialization
def generate_agents(N, max_tokens):
    agents = []
    
    for id in range(N):
        gender, ethnicity, education, occupation, location = data_initialize.generate_profile()
        
        agent = GPT.PersonalizedAgent(id + 1, gender, ethnicity, education, occupation, location, model = model_ver, max_tokens = max_tokens, api_key = api_key)

        agent.persona = agent.generate_persona()
        agents.append(agent)
    return agents

# Simulation Main Loop
def simulation(agents, group_num, situation_num, question='1', specific_group_number='None'):
    result = []
    member_num = int(len(agents)/group_num)

    # Set Group Labels
    if specific_group_number == 'None':
        group_size = member_num
        group_label = []
        for i in range(1, group_num+1):
            group_label += [i] * group_size
    # Test Specific Group
    else:
        group_label = [specific_group_number] * member_num

    # GPT Temperature Normalization
    temperature_scaled = data_initialize.init_temperature(member_num, lower_temp = 0.0, upper_temp = 2.0)

    # Main Loop
    agent_count = 1
    for agent in agents:
        agent.group = group_label[agent_count - 1]
        agent.temperature = temperature_scaled[(agent_count - 1) % member_num]

        # Personalize - TCU Test
        if task_run_dict.get("TCU"):
            TCU_test.TCU_test(agent, usecase_dict["Task_TCU"])

        # Plea Bargain
        task_config_pb = usecase_dict["Task_Plea_Bargain"]
        question_index = list(range(0, situation_num))
        risk_index = random.randint(0, 1)

        for qid in range(situation_num):
            ## Risk Taking Prompt
            risk_taking_text = ""
            if risk_index == 1: risk_taking_text = prompts["Risk_Taking_Prompt"]
            
            ## Plea Bargain Instruction
            context = prompts["Question_Instruction"]

            ## Plea Bargain Few-shot, except for Task 1
            if task_config_pb['Fewshot'] == True and question != '1':
                context += prompts["Fewshot_Examples"]
            
            ## Plea Bargain Scenario
            persona_text = prompts["{}_Prompt".format(task_config_pb['Scenario']['Persona'])].format(persona = agent.persona, risk_taking = risk_taking_text)
            Question_Scenario = prompts["Question_Scenario_{}".format(task_config_pb['Scenario']['Presumption'])].format(Scenario = ScenarioBase[question][agent.group - 1])
            Question_Cases = prompts["Question{}_Cases".format(question)].format(x = QuestionBase[question][question_index[qid]][0], y = QuestionBase[question][question_index[qid]][1])
            
            context += persona_text + Question_Scenario + Question_Cases
            #print(context)

            ## Decision
            agent.max_tokens = output_max_tokens
            decision = agent.communicate(context).strip().lower()
            print(decision)
            
            data_formatting.process_decision(agent, question_index[qid], decision)
        
        # Log
        dec = []
        for qid in range(situation_num):
            dec.append(agent.decision[qid])
        print(f"#{agent_count}: {dec}, Group ID: {agent.group}, temperature: {agent.temperature}")
        result.append([agent_count, dec, agent.decision_reason, agent.group, agent.temperature, agent.persona])
        
        agent_count += 1
    
    return result

def verification(agents, group_num, situation_num, question = '1', specific_group_number='None', output_path = "output/plea_bargain"):
    # Verify the distribution
    if task_run_dict.get("TCU"):
        TCU_results = data_formatting.TCU_distribution(agents)
        data_plot.plot_personalize(TCU_results, len(agents), output_path)

    # Grouping
    if specific_group_number == 'None':
        groups = data_formatting.group_agents(agents, group_num, situation_num)
    else:
        groups = data_formatting.group_agents_specific(agents, group_num, situation_num)
    
    average_choice = []
    for group in groups:
        group_decision = []
        for qid in range(situation_num):
            group_decision.append(round(sum(group[qid]) / len(group[qid]) * 100, 2))
        average_choice.append(group_decision)

    print(average_choice)

    # Plot Result
    if specific_group_number == 'None':
        data_plot.plot_decision(average_choice, xlabelBase[question], ylabelBase[question], group_num, situation_num, output_path)
    else:
        data_plot.plot_decision_specific(average_choice, xlabelBase[question], ylabelBase[question], group_num, situation_num, specific_group_number, output_path)

# Simulation
def run_simulation(N, group_num, situation_num, question, specific_group_number):
    # Agents Setup
    agents = generate_agents(N, max_tokens = 50)

    # System Setup
    output_path = f"output/plea_bargain/Record-{datetime.date.today().strftime('%y%m%d')}-{time.strftime('%H%M')}-{model_ver}"
    os.makedirs(output_path, exist_ok=True)

    # Simulation
    result = simulation(agents, group_num, situation_num, question, specific_group_number)
    verification(agents, group_num, situation_num, question, specific_group_number, output_path)

    # Data Output
    if task_run_dict.get("DA"):
        df_decision = pd.DataFrame(result, columns=['ID', 'Decision', 'Reasoning', 'Group', 'Temperature', 'Persona'])
        df_decision.to_csv(f"{output_path}/logs_decision.csv", index=False)
