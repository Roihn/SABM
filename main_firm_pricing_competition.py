import os

try:
    api_key = os.environ["OPENAI_API_KEY"]
except:
    api_key = open('apikey.token').readline().strip()

from src.firm_pricing_competition.arguments import argparser
import src.firm_pricing_competition.pricing_competition as competition
import src.firm_pricing_competition.GUI as GUI

def main(args):
    if args.gui == True:
        competition.my_apikey1 = api_key
        competition.my_apikey2 = api_key
        simulation_parameters = GUI.gui().run()
        competition.run_simulation(simulation_parameters[0], simulation_parameters[1], simulation_parameters[2], simulation_parameters[3], simulation_parameters[4], simulation_parameters[5], simulation_parameters[6], simulation_parameters[7])
    else:
        competition.my_apikey1 = api_key
        competition.my_apikey2 = api_key
        competition.model_ver = args.model_version
        competition.rounds = args.rounds
        competition.output_max_tokens = args.output_max_tokens
        competition.breakpoint_rounds = args.breakpoint_rounds
        competition.firm_persona_1 = args.persona_firm1
        competition.firm_persona_2 = args.persona_firm2
        competition.program_run_dict['Set_Initial_Prices'] = args.set_initial_price

        competition.run_simulation(
            args.cost,
            args.parameter_a,
            args.parameter_d,
            args.parameter_beta,
            args.initial_price,
            args.load_data_location,
            args.strategy,
            args.has_conversation
        )

if __name__ == "__main__":
    args = argparser.parse_args()
    main(args)
