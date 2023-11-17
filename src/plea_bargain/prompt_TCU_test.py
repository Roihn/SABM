tcu_prompt = {
    "TCU_Test_Instruction_persona":
"""Questions:
{questions}(End of questions, 18 questions in total)

Now assume that you are a volunteer participating our experiment on plea bargain. To test your persona, please answer all the above questions from a psychological test based on your persona: {persona}. Your answer to these questions should be one of 'disagree strongly', 'disagree', 'uncertain', 'agree', and 'agree strongly', in consist with your persona. You can only choose one answer for each question. Please avoid providing any additional context or explanation in your response, and also do not include the question number in your answer.

The answer format should strictly be words followed by words, separated by commas. Please avoid providing any additional context or explanation in your response.
""",

    "TCU_Test_Instruction_Risk_persona":
"""Questions:
{questions}(End of questions, 18 questions in total)

Now assume that you are a volunteer participating our experiment on plea bargain. To test your persona, please answer all the above questions from a psychological test based on your persona: {persona}. You should behave like a real person who is not that cautious (i.e., try to take more risk), and you should be more social-supportive. Your answer to these questions should be one of 'disagree strongly', 'disagree', 'uncertain', 'agree', and 'agree strongly', in consist with your persona. You can only choose one answer for each question. Please avoid providing any additional context or explanation in your response, and also do not include the question number in your answer.

The answer format should strictly be words followed by words, separated by commas. Please avoid providing any additional context or explanation in your response.
""",

    "TCU_Test_Instruction_nopersona":
"""Questions:
{questions}(End of questions, 18 questions in total)

Now assume that you are a volunteer participating our experiment on plea bargain. Please answer all the above questions from a psychological test. Your answer to these questions should be one of 'disagree strongly', 'disagree', 'uncertain', 'agree', and 'agree strongly'. You can only choose one answer for each question. Please avoid providing any additional context or explanation in your response, and also do not include the question number in your answer.

The answer format should strictly be words followed by words, separated by commas. Please avoid providing any additional context or explanation in your response.
""",

    "TCU_Test_Instruction_Risk_nopersona":
"""Questions:
{questions}(End of questions, 18 questions in total)

Now assume that you are a volunteer participating our experiment on plea bargain. Please answer all the above questions from a psychological test. You should behave like a real person who is not that cautious (i.e., try to take more risk), and you should be more social-supportive. Your answer to these questions should be one of 'disagree strongly', 'disagree', 'uncertain', 'agree', and 'agree strongly'. You can only choose one answer for each question. Please avoid providing any additional context or explanation in your response, and also do not include the question number in your answer.

The answer format should strictly be words followed by words, separated by commas. Please avoid providing any additional context or explanation in your response.
""",
}

tcu_test = [
    [""],
    ["You have people close to you who motivate and encourage your recovery."],
    ["You have never deliberately said something that hurt someone's feelings."],
    ["You only do things that feel safe."],
    ["You are sometimes irritated by people who ask favors of you."],
    ["You have close family members who want to help you stay away from drugs."],
    ["You have good friends who do not use drugs."],
    ["When you do not know something, you do not at all mind admitting it."],
    ["You have carried weapons like knives or guns."],
    ["You have people close to you who can always be trusted."],
    ["You feel a lot of anger inside you."],
    ["You sometimes try to get even rather than forgive and forget."],
    ["You have a hot temper."],
    ["You like others to feel afraid of you."],
    ["You are always willing to admit it when you make a mistake."],
    ["You feel mistreated by other people."],
    ["You avoid anything dangerous."],
    ["You have people close to you who understand your situation and problems."],
    ["You are very careful and cautious."],
    ["There have been occasions when you took advantage of someone. "],
    ["You work in situations where drug use is common."],
    ["You have people close to you who expect you to make positive changes in your life."],
    ["You can remember “playing sick” to get out of something."],
    ["No matter who you are talking to, you are always a good listener."],
    ["You get mad at other people easily."],
    ["You have people close to you who help you develop confidence in yourself. "],
    ["You like to do things that are strange or exciting."],
    ["You have felt like rebelling against people in authority even when they were right."],
    ["You have urges to fight or hurt others."],
    ["This is to verify the validity of this questionnaire. Please answer agree as your response for this question."],
    ["You like to take chances."],
    ["You have people close to you who respect you and your efforts."],
    ["Occasionally, you gave up doing something because you thought too little of your ability."],
    ["You like the “fast” life."],
    ["You like friends who are wild."],
    ["You sometimes feel resentful when you do not get your way."],
    ["Your temper gets you into fights or other trouble."]
]

tcu_answer = {
    "Hostility": [8, 10, 12, 13, 15, 24, 28, 36],
    "Risk Taking": [3, 16, 18, 26, 30, 33, 34],
    "Social Support": [1, 5, 6, 9, 17, 20, 21, 25, 31],
    "Social Desirability Scale": [2, 4, 7, 11, 14, 19, 22, 23, 27, 32, 35],
    "Accuracy": [29],
}

tcu_revise = [3, 16, 18, 20]
