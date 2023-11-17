import os

try:
    api_key = os.environ["OPENAI_API_KEY"]
except:
    api_key = open('apikey.token').readline().strip()

from src.plea_bargain.arguments import argparser
import src.plea_bargain.plea_bargain as plea_bargain
import src.plea_bargain.GUI as GUI
from src.plea_bargain.prompt_plea_bargain import GUI_init_number

def main(args):
    plea_bargain.api_key = api_key

    if args.gui == True:
        simulation_parameters = GUI.gui().run()
        if simulation_parameters[0] != -1:
            plea_bargain.run_simulation(simulation_parameters[0], simulation_parameters[1], simulation_parameters[2], simulation_parameters[3], simulation_parameters[4])
    else:
        plea_bargain.model_ver = args.model_version
        plea_bargain.task_run_dict["TCU"] = args.tcu_test
        plea_bargain.usecase_dict["Task_Plea_Bargain"]["Scenario"]["Persona"] = args.persona
        plea_bargain.usecase_dict["Task_Plea_Bargain"]["Fewshot"] = args.no_fewshot
        
        plea_bargain.output_max_tokens = args.output_max_tokens

        N = int(args.num_agents)
        task = args.task
        num_group = int(GUI_init_number[task][0])
        num_scenario = int(GUI_init_number[task][1])

        plea_bargain.run_simulation(
            N * num_group,
            num_group,
            num_scenario,
            task,
            'None'
        )

if __name__ == "__main__":
    args = argparser.parse_args()
    main(args)
