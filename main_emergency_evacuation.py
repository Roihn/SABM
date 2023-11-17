import os

try:
    api_key = os.environ["OPENAI_API_KEY"]
except:
    api_key = open('apikey.token').readline().strip()

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.emergency_evacuation.task1 import EscapeSociety as EscapeSociety_task1
from src.emergency_evacuation.task2 import EscapeSociety as EscapeSociety_task2
from src.emergency_evacuation.task3 import EscapeSociety as EscapeSociety_task3
from src.emergency_evacuation.task4 import EscapeSociety as EscapeSociety_task4
from src.emergency_evacuation.arguments import argparser

def eval_physical_mental_statics(society, logging):
    physical_positive_escaped, physical_positive_dead = 0, 0
    physical_negative_escaped, physical_negative_dead = 0, 0
    mental_positive_escaped, mental_positive_dead = 0, 0
    mental_negative_escaped, mental_negative_dead = 0, 0
    num_physical_positive, num_physical_negative = 0, 0
    num_mental_positive, num_mental_negative = 0, 0
    for agent in society.human_list:
        if agent.capability == 0:
            if agent.status == "escaped":
                physical_positive_escaped += 1
            elif agent.status == "dead":
                physical_positive_dead += 1
            num_physical_positive += 1
        elif agent.capability == 1:
            if agent.status == "escaped":
                physical_negative_escaped += 1
            elif agent.status == "dead":
                physical_negative_dead += 1
            num_physical_negative += 1
        if agent.mental == 0:
            if agent.status == "escaped":
                mental_positive_escaped += 1
            elif agent.status == "dead":
                mental_positive_dead += 1
            num_mental_positive += 1
        elif agent.mental == 1:
            if agent.status == "escaped":
                mental_negative_escaped += 1
            elif agent.status == "dead":
                mental_negative_dead += 1
            num_mental_negative += 1
    
    logging.info("Physical Ability Result:")
    if num_physical_positive != 0:
        logging.info(f"physical_positive_escaped: {physical_positive_escaped} / {num_physical_positive} = {physical_positive_escaped / num_physical_positive}")
        logging.info(f"physical_positive_dead: {physical_positive_dead} / {num_physical_positive} = {physical_positive_dead / num_physical_positive}")
    if num_physical_negative != 0:
        logging.info(f"physical_negative_escaped: {physical_negative_escaped} / {num_physical_negative} = {physical_negative_escaped / num_physical_negative}")
        logging.info(f"physical_negative_dead: {physical_negative_dead} / {num_physical_negative} = {physical_negative_dead / num_physical_negative}")
    
    logging.info("Mental Ability Result:")
    if num_mental_positive != 0:
        logging.info(f"mental_positive_escaped: {mental_positive_escaped} / {num_mental_positive} = {mental_positive_escaped / num_mental_positive}")
        logging.info(f"mental_positive_dead: {mental_positive_dead} / {num_mental_positive} = {mental_positive_dead / num_mental_positive}")
    if num_mental_negative != 0:
        logging.info(f"mental_negative_escaped: {mental_negative_escaped} / {num_mental_negative} = {mental_negative_escaped / num_mental_negative}")
        logging.info(f"mental_negative_dead: {mental_negative_dead} / {num_mental_negative} = {mental_negative_dead / num_mental_negative}")


def main(args):
    if args.task == 1:
        EscapeSociety = EscapeSociety_task1
    elif args.task == 2:
        EscapeSociety = EscapeSociety_task2
    elif args.task == 3:
        EscapeSociety = EscapeSociety_task3
    elif args.task == 4:
        EscapeSociety = EscapeSociety_task4

    society = EscapeSociety(
        "escape",
        num_humans=args.num_humans,
        agent_chat_range=5,
        width=33,
        height=33,
        exit_width=3,
        seed=args.seed,
        need_obstacle=bool(args.need_obstacle),
        random_agent=bool(args.random_agent),
        is_panic=bool(args.is_panic),
        model="gpt-4-0314",
        api_key=api_key,
    )
    for step_count in tqdm(range(51), desc="Simulation Processing"):
        society.step()
        # society.render(society.human_list)
        society.render()
        # print("count", count, society.cur_human_list)
        if len(society.cur_human_list) == 0:
            break
    
    if len(society.cur_human_list) == 0:
        print("All humans escaped in advance!")

    print("Simulation finished.")
    print("Evaluation processing...")
    
    society.logging.info("Simulation finished.")
    society.logging.info("Total Round: %d", society.round)
    society.logging.info(f"Escape rate: {society.num_escaped} / {society.num_humans} = {society.num_escaped / society.num_humans}")
    society.logging.info(f"Death rate: {society.num_dead} / {society.num_humans} = {society.num_dead / society.num_humans}")

    if args.task > 1:
        eval_physical_mental_statics(society, society.logging)
    
    # save society.escaped_list and society.dead_list
    with open(f"output/emergency_evacuation/task{args.task}/need_obstacle_{args.need_obstacle}/{args.num_humans}humans/is_panic_{args.is_panic}_seed{args.seed}/escaped_list.npy", "wb") as f:
        np.save(f, society.escaped_list)
    with open(f"output/emergency_evacuation/task{args.task}/need_obstacle_{args.need_obstacle}/{args.num_humans}humans/is_panic_{args.is_panic}_seed{args.seed}/dead_list.npy", "wb") as f:
        np.save(f, society.dead_list)
    os.makedirs(f"output/emergency_evacuation/task{args.task}/need_obstacle_{args.need_obstacle}/{args.num_humans}humans/is_panic_{args.is_panic}_seed{args.seed}/agent_logs", exist_ok=True)
    os.makedirs(f"output/emergency_evacuation/task{args.task}/need_obstacle_{args.need_obstacle}/{args.num_humans}humans/is_panic_{args.is_panic}_seed{args.seed}/agent_chat_logs", exist_ok=True)
    for agent in society.human_list:
        with open(f"output/emergency_evacuation/task{args.task}/need_obstacle_{args.need_obstacle}/{args.num_humans}humans/is_panic_{args.is_panic}_seed{args.seed}/agent_logs/agent{agent.id}_pos_history.npy", "wb") as f:
            np.save(f, agent.pos_history)
            df = pd.DataFrame(columns=agent.state_history[0].keys())
            df = pd.concat([df, pd.DataFrame(agent.state_history)], ignore_index=True)
            df.to_csv(f"output/emergency_evacuation/task{args.task}/need_obstacle_{args.need_obstacle}/{args.num_humans}humans/is_panic_{args.is_panic}_seed{args.seed}/agent_chat_logs/agent{agent.id}_chat_history.csv", index=False)

    print("Evaluation finished. Please check `output/` folder for the results.")

if __name__ == "__main__":
    args = argparser.parse_args()
    main(args)
