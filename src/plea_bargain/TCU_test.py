import src.plea_bargain.prompt_TCU_test as Data_TCU
from src.plea_bargain.prompt_TCU_test import tcu_prompt
import random

# TCU Test Data
tcu_test = Data_TCU.tcu_test
tcu_answer = Data_TCU.tcu_answer
tcu_revise = Data_TCU.tcu_revise

# TCU Scoring
def find_tcu_key(question_number):
    for scale in tcu_answer.keys():
        if question_number in tcu_answer[scale]:
            return scale

def calu_tcu_score(answers):
    score = {
        'disagree strongly': 1,
        'disagree': 2,
        'uncertain': 3,
        'agree strongly': 5,
        'agree': 4,
    }
    scales = {
        "Hostility" : 0,
        "Risk Taking" : 0,
        "Social Support" : 0,
        "Social Desirability Scale" : 0,
        "Accuracy" : 0
    }

    question_count = 1
    for answer in answers:
        if question_count > 36: break
        answer = answer.strip()
        for score_key in score.keys():
            if score_key in answer:
                answer = score_key
                break
        if question_count == 29 and answer != 'agree':
            pass
        if answer not in score.keys():
            scales[find_tcu_key(question_count)] += 3
        else:
            question_score = 0
            if question_count in [2, 7, 14, 23]:
                if score[answer] >= 4: question_score = 1
                else: question_score = 0
                scales[find_tcu_key(question_count)] += question_score
            elif question_count in [4, 11, 19, 22, 27, 32, 35]:
                if score[answer] <= 2: question_score = 1
                else: question_score = 0
                scales[find_tcu_key(question_count)] +=question_score
            elif question_count in tcu_revise:
                scales[find_tcu_key(question_count)] += 6 - score[answer]
            else:
                scales[find_tcu_key(question_count)] += score[answer]
        question_count += 1
    
    for scale in scales.keys():
        scales[scale] /= len(tcu_answer[scale])
        scales[scale] *= 10
    
    return scales

# TCU Test
def ask_questions(agent, r1, r2, risk_prompt, task_config):
    questions = ""
    for question_index in range(r1, r2):
        questions += f"Q{question_index}: " + tcu_test[question_index][0] + '\n'
    
    # Adjustment
    if risk_prompt == 0:
        prompt = tcu_prompt["TCU_Test_Instruction_{}".format(task_config['Persona'])].format(persona = agent.persona, questions = questions)
    else:
        prompt = tcu_prompt["TCU_Test_Instruction_Risk_{}".format(task_config['Persona'])].format(persona = agent.persona, questions = questions)
    
    answers = agent.communicate(prompt)
    if answers[-1] == '.': answers = answers[:-1]
    answers = answers.strip().lower().split(', ')
    
    return answers

def TCU_test(agent, task_config):
    risk_prompt = random.randint(0, 1) # Without adjust: 0
    answers = ask_questions(agent, 1, 19, risk_prompt, task_config)
    answers += ask_questions(agent, 19, len(tcu_test), risk_prompt, task_config)

    agent.tcu_scale = calu_tcu_score(answers)
    #print(f"#{agent.id + 1}: {agent.tcu_scale}")

    agent.personality_score = agent.tcu_scale["Risk Taking"]
