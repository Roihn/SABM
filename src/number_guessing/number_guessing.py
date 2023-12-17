import src.number_guessing.agent as GPT
import src.number_guessing.prompt as prompt

# Settings
api_key = "sk-"
persona_type = "default"

fixed_guess_number = False
api_type = "openai"
api_base = ""
interpretation_guess = False
advanced_settings = "default"
model_ver = 'gpt-4-0613'

# Simulation
def simulation():
    # Agent setup
    agent1 = GPT.Agent(temperature = 0.5, model= model_ver, max_tokens = 128, api_key = api_key, api_type = api_type, api_base = api_base)
    agent2 = GPT.Agent(temperature = 0.5, model= model_ver, max_tokens = 128, api_key = api_key, api_type = api_type, api_base = api_base)

    # Generate target number
    if fixed_guess_number == False:
        target_number = agent2.communicate(prompt.background_prompt_judge["generate_number"])
    else:
        target_number = 28
    print(f"Target: {target_number}")

    # First guess
    guess = []
    guess_round = 1

    if advanced_settings not in ["reasoning", "planning", "hint"]:
        answer = agent1.communicate(prompt.background_prompt_guess["first_guess"].format(persona = prompt.persona_prompt[persona_type], advanced_settings = prompt.advanced_settings_prompt[advanced_settings]))
        guess.append(int(answer))
    elif advanced_settings == "reasoning":
        answer = agent1.communicate(prompt.background_prompt_guess["reasoning_first_guess"].format(persona = prompt.persona_prompt[persona_type]))
        print(answer.split('\n')[0])
        guess.append(int(answer.split('\n')[1]))     
    elif advanced_settings == "planning":
        answer = agent1.communicate(prompt.background_prompt_guess["first_guess"].format(persona = prompt.persona_prompt[persona_type], advanced_settings = prompt.advanced_settings_prompt["default"]))
        guess.append(int(answer))
    elif advanced_settings == "hint":
        hint = agent2.communicate(prompt.background_prompt_judge["hint"].format(target_number = target_number))
        print(hint)

        answer = agent1.communicate(prompt.background_prompt_guess["hint_first_guess"].format(hint = hint, persona = prompt.persona_prompt[persona_type]))
        guess.append(int(answer))

    if interpretation_guess:
        print(agent1.communicate(prompt.background_prompt_guess["explain_guess"].format(prev_guess = guess[-1], history = guess)))

    # Loop of guessing
    while True:
        # Judge
        response = agent2.communicate(prompt.background_prompt_judge["judge_guess"].format(target_number = target_number, guess = guess[-1]))
        guess[-1] = str(guess[-1])
        guess[-1] += f" {response}"
        print(guess[-1])

        # Exit condition
        if 'congratulations' in response.lower(): break
        guess_round += 1

        # Guess
        if advanced_settings not in ["reasoning", "planning", "hint"]:
            answer = agent1.communicate(prompt.background_prompt_guess["make_guess"].format(prev_guess = guess[-1], history = guess, persona = prompt.persona_prompt[persona_type], advanced_settings = prompt.advanced_settings_prompt[advanced_settings]))
            guess.append(int(answer))
        elif advanced_settings == "reasoning":
            answer = agent1.communicate(prompt.background_prompt_guess["reasoning_make_guess"].format(prev_guess = guess[-1], history = guess, persona = prompt.persona_prompt[persona_type]))
            print(answer.split('\n')[0])
            guess.append(int(answer.split('\n')[1]))
        elif advanced_settings == "planning":
            if guess_round % 3 != 1:
                answer = agent1.communicate(prompt.background_prompt_guess["make_guess"].format(prev_guess = guess[-1], history = guess, persona = prompt.persona_prompt[persona_type], advanced_settings = prompt.advanced_settings_prompt['default']))
                guess.append(int(answer))
            else:
                strategy = agent1.communicate(prompt.background_prompt_guess["planning"].format(prev_guess = guess[-1], history = guess, persona = prompt.persona_prompt[persona_type]))
                print(strategy)

                answer = agent1.communicate(prompt.background_prompt_guess["planning_reprompt"].format(prev_guess = guess[-1], history = guess, persona = prompt.persona_prompt[persona_type], strategy = strategy))
                guess.append(int(answer))
        elif advanced_settings == "hint":
            answer = agent1.communicate(prompt.background_prompt_guess["hint_make_guess"].format(hint = hint, prev_guess = guess[-1], history = guess, persona = prompt.persona_prompt[persona_type]))
            guess.append(int(answer))

        if interpretation_guess:
            print(agent1.communicate(prompt.background_prompt_guess["explain_guess"].format(prev_guess = guess[-1], history = guess)))

    # Results
    print(guess)
