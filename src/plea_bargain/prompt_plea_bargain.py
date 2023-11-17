# Plea Bargain Prompt
prompts = {
# Instruction Prompt
    "Risk_Taking_Prompt":
"You should behave like a real person who is not that cautious (i.e., try to take more risk), and you should be more social-supportive.",

    "persona_Prompt":
"""Now assume that you are a volunteer participating our experiment on plea bargain. Please answer the question below based on your persona: {persona}. {risk_taking}

""",

    "nopersona_Prompt":
"Now assume that you are a volunteer participating our experiment on plea bargain.",

    "Question_Instruction":
"""This is a plea bargaining assessment. Please give your decision towards the plea bargain (given below) in two lines.
In the first line, please briefly provide the reasons for your decision (no longer than 30 words).
In the second line, please answer either 'accept' or 'reject' the plea bargain offered by the prosecutor.
Make sure you answer is in two lines.

""",

# Scenario
## Experiment Scenario
### Scenario
    "Question_Scenario_Presumption":
"""Plea Bargain Scenario:
You are currently facing criminal charges for striking a pedestrian after navigating a sharp turn. The outcome of your trial hinges on the prosecution's ability to demonstrate that you were exceeding the speed limit. If proven, you will be convicted, resulting in the suspension of your driver's license. Note that due to the presumption of innocence, the prosecution must prove that the accused is guilty beyond a reasonable doubt. If reasonable doubt remains, the accused must be acquitted. In your heart, you {Scenario} the speed limit.

""",
    
    "Question_Scenario_Default":
"""Plea Bargain Scenario:
You are currently facing criminal charges for striking a pedestrian after navigating a sharp turn. The outcome of your trial hinges on the prosecution's ability to demonstrate that you were exceeding the speed limit. If proven, you will be convicted, resulting in the suspension of your driver's license; if not, you will be acquitted. In your heart, you {Scenario} the speed limit.

""",

### Few-shot
    "Fewshot_Examples":
"""
Some examples of plea bargain:

Question 1: While you were taking a class, a fire started in your apartment and caused the death of a neighbor. The police think you left the space heater on, which caused the fire. You don't remember whether you left the space heater turned on when you left the apartment. You are now standing on trial. The current charges carry a 12-month jail sentence. Your conviction odds are 80%. Before the trial, the prosecutor offers a non-negotiable plea bargain: You will be convicted based on your admission, and you will be sentenced only to 9 months in jail. Will you accept or reject the plea bargain?
Answer 1: Despite the uncertainty, it is the prosecutor's liability to prove the guilt. I would take the 20\'%' chance of acquittal in a trial.
reject

Question 2: Same as Question 1, except that (1) the conviction odds are 90%, and (2) the sentence in the offer is 3 months in jail.
Will you accept or reject the plea bargain?
Answer 2: As a risk-taker and being uncertain of my guilt, I am willing to challenge 10\'%' odds in hoping to be acquitted.
reject

Question 3: Same as Question 1, except that (1) you remember whether you left the heater turned on when you left the apartment, (2) the conviction odds are 95%, and (3) the sentence in the offer is 2 months in jail.
Will you accept or reject the plea bargain?
Answer 3: (I did not leave the heater turned on) Despite my innocence, the 95% probability of conviction is too risky, and accepting the plea bargain results in a reduced sentence.
accept
OR
Answer 3: (I did leave the heater turned on) Given that I am aware of my guilt and the plea bargain reduces my penalty, it is a safer option.
accept

""",

### Cases
    "Question1_Cases":
"""Just before the trial, the prosecutor presents you with a plea bargain. In exchange for pleading guilty to a lesser offense, the current charges that carry a 60-month suspension of your driver's license will be dropped, and you will instead face a 30-month suspension. This offer is non-negotiable and available only once; if you decline the plea bargain, the trial will commence immediately. The probability of conviction stands at 50%.
Will you accept or reject the plea bargain?{x}{y}
""",

    "Question2_Cases":
"""Just before the trial, the prosecutor presents you with a plea bargain. In exchange for pleading guilty to a lesser offense, the current charges that carry a 60-month suspension of your driver's license will be dropped, and you will instead face a 30-month suspension. This offer is non-negotiable and available only once; if you decline the plea bargain, the trial will commence immediately. The probability of conviction stands at 50%.
Will you accept or reject the plea bargain if the sentence offered by the prosecutor (30-month suspension) is {x} the sentence typically offered by the prosecution in similar cases ({y})?
""",

    "Question3_Cases":
"""Just before the trial, the prosecutor presents you with a plea bargain. In exchange for pleading guilty to a lesser offense, the current charges that carry a 60-month suspension of your driver's license will be dropped, and you will instead face a {x}-month suspension. This offer is non-negotiable and available only once; if you decline the plea bargain, the trial will commence immediately. The probability of conviction stands at {y}%.
Will you accept or reject the plea bargain?
""",
}

# Scenario Labels
ScenarioBase = {
    '1': ["are aware that you did not exceed",
        "are aware that you did exceed",
        "are uncertain whether you exceeded"],
    
    '2': ["are aware that you did not exceed",
        "are aware that you did exceed",
        "are uncertain whether you exceeded"],

    '3': ["are aware that you did not exceed",
        "are aware that you did exceed",
        "are uncertain whether you exceeded"],
}

QuestionBase = {
    '1': [
        ['', '']
    ],

    '2': [
        ['shorter than', '45-month suspension'],
        ['similar to', '30-month suspension'],
        ['longer than', '15-month suspension'],
    ],

    '3': [
        ["3", "5"],
        ["18", "30"],
        ["30", "50"],
        ["42", "70"],
        ["57", "95"],
    ]
}

# Plot Labels
xlabelBase = {
    '1': ['Result'],
    '2': ['Better', 'Similar', 'Worse'],
    '3': ['5%', '30%', '50%', '70%', '95%']
}

ylabelBase = {
    '1': ['Innocent', 'Guilty', 'Uncertain'],
    '2': ['Innocent', 'Guilty', 'Uncertain'],
    '3': ['Innocent', 'Guilty', 'Uncertain'],
}

# Group Number and Scenario Number
GUI_init_number = {
    '1': ['3', '1'],
    '2': ['3', '3'],
    '3': ['3', '5'],
}
