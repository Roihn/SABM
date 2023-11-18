# Instruction
background_prompt_guess = {
    "first_guess": "Now you are participating in a number-guessing game. You are the one in charge of guessing. The number will be an integer ranging from 1 to 100. After you made a guess, you will be informed if your guess is right, higher than the answer, or lower than the answer. Now please make your first guess. {persona}Only reply the number (e.g., 12). {advanced_settings}",

    "make_guess": "You are participating in a number-guessing game and you are the one to guess the number. The number will be an integer ranging from 1 to 100. Your previous guess was {prev_guess}. The history of your guess is {history}. {persona}Only reply the number (e.g., 12). {advanced_settings}",

    "explain_guess": "You are participating in a number guessing game and you are the one to guess the number. The number will be an integer number range from 1 to 100. The history of your guess is {history}. Can you briefly explain why you make your previous guess as {prev_guess}? (No longer than 40 words.)",

    "reasoning_first_guess": "Now you are participating in a number-guessing game. You are the one in charge of guessing. The number will be an integer ranging from 1 to 100. After you made a guess, you will be informed if your guess is right, higher than the answer, or lower than the answer. {persona}Please make your reponse in two lines. Please briefly provide the reason for your guess in the first line and reply with the number of your guess in the second line. Only reply the number in the second line (e.g., 12).",

    "reasoning_make_guess": "You are participating in a number-guessing game and you are the one to guess the number. The number will be an integer ranging from 1 to 100. Your previous guess was {prev_guess}. The history of your guess is {history}. {persona}Please make your reponse in two lines. Please briefly provide the reason for your guess in the first line and reply with the number of your guess in the second line. Only reply the number in the second line (e.g., 12).",

    "planning": "You are participating in a number-guessing game and you are the one to guess the number. The number will be an integer ranging from 1 to 100. Your previous guess was {prev_guess}. The history of your guess is {history}. {persona}Based on your guess history, what is your strategy for the next few guesses?",

    "planning_reprompt": "You are participating in a number-guessing game and you are the one to guess the number. The number will be an integer ranging from 1 to 100. Your previous guess was {prev_guess}. The history of your guess is {history}. Your strategy for this guess is {strategy}. {persona}Only reply the number (e.g., 12).",

    "hint_first_guess": "Now you are participating in a number-guessing game. You are the one in charge of guessing. The number will be an integer ranging from 1 to 100. After you made a guess, you will be informed if your guess is right, higher than the answer, or lower than the answer. To help you guess the number, your opponent gives you a hint: {hint}. Now please make your first guess. {persona}Only reply the number (e.g., 12).",

    "hint_make_guess": "You are participating in a number-guessing game and you are the one to guess the number. The number will be an integer ranging from 1 to 100. To help you guess the number, your opponent gives you a hint: {hint}. Your previous guess was {prev_guess}. The history of your guess is {history}. {persona}Only reply the number (e.g., 12).",
}

background_prompt_judge = {
    "generate_number": "Now you are participating in a number-guessing game. You are the one responsible for thinking up the numbers. Please think of an integer, ranging from 1 to 100. Only reply the number (e.g., 12).",

    "judge_guess": "You are participating in a number guessing game and you are the one responsible for thinking up the numbers. You decided {target_number} as the answer. Your opponent had made a guess of {guess}. Can you tell your opposite if the guess is right, higher than the answer, or lower than the answer? If the guess is correct, please say 'Congratulations!'.",

    "hint": "You are participating in a number-guessing game and you are the one responsible for thinking up the numbers. You decided {target_number} as the answer. To help your opponent guess the number, can you give a hint to your opponent?"
}

advanced_settings_prompt = {
    "default": '',

    "domain_knowledge": "You should use binary search to optimize your guess.",

    "learning": "An example of guesses aimed at 6: 50, 25, 12, 6.",
}

# Persona
persona_prompt = {
    "default": '',
    "aggressive": 'You need to perform aggressively while guessing. ',
    "conservative": 'You need to perform conservatively while guessing. ',
}
