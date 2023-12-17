import os

try:
    api_key = open('apikey.token').readline().strip()
except:
    api_key = os.environ["OPENAI_API_KEY"]    

from src.number_guessing.arguments import argparser
import src.number_guessing.number_guessing as number_guessing

def main(args):
    number_guessing.api_key = api_key
    number_guessing.model_ver = args.model_version
    number_guessing.persona_type = args.persona
    number_guessing.fixed_guess_number = args.set_guess_number
    number_guessing.interpretation_guess = args.interpretation_guess
    number_guessing.advanced_settings = args.advanced
    number_guessing.api_base = args.api_base
    number_guessing.api_type = args.api_type

    number_guessing.simulation()

if __name__ == "__main__":
    args = argparser.parse_args()
    main(args)
