import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument("--model_version", type=str, default='gpt-4-0613')
argparser.add_argument("--persona", type=str, default='default')

argparser.add_argument("--set_guess_number", dest='set_guess_number', action='store_true')
argparser.set_defaults(set_guess_number=False)

argparser.add_argument("--interpretation_guess", dest='interpretation_guess', action='store_true')
argparser.set_defaults(interpretation_guess=False)

argparser.add_argument("--api_type", type=str, default='openai')
argparser.add_argument("--api_base", type=str, default='')

argparser.add_argument("--advanced", type=str, default='default')
