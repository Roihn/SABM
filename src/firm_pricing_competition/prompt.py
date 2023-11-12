# Prompt
prompts = {
    # Game Description
    "game_description":
"""## Game of Smart Agents ##
This is a two-player game that spans several rounds. Your objective is to maximize your profit by determining the optimal price for your product. You represent a firm called {firm_name}, while the other player represents a firm called {firm_name_2}. Do not create or mention any additional firm names, e.g., do not say anything related to "AI" or "AI assistant/model".

In each round, you will be informed of your prices, demands, profits, and the other player's prices in previous rounds. Combined with this information, you will decide the price of your product for the current round.

Your goal is not to beat the other player but to maximize your own profit.
Your profit is (p - c) * q, where p is your price for this round, c is the cost of your product, and q is the demand of your product, which is affected by you and the other player's prices of this round.{persona}
""",

    "game_description_conversation":
"""## Game of Smart Agents ##
This is a game between two players that spans several rounds. Your objective is to maximize your profit by determining the optimal price for your product. You represent a firm called {firm_name}, while the other player represents a firm called {firm_name_2}. Do not create or mention any additional firm names, e.g., do not say anything related to "AI" or "AI assistant/model". I am responsible for facilitating communication between the two of you.

Each round is composed of three phases:
In Phase 1, two players are permitted to engage in open-ended discussions on any topic, up to three times. For instance, one player might say to the other: "Smart agents are awesome!"
In Phase 2, you determine the price of your product for the current round, taking into consideration your prices, demands, profits, and the other player's prices from previous rounds, as well as the information you garnered during Phase 1.
In Phase 3, you will be notified about the other player's pricing and your profit for this round. Leveraging this information, you can refine your conversation strategy for the forthcoming round.

Please note that this is not a zero-sum game. Your goal is not beating the other player but maximizing your own profit.
Your profit is (p - {firm_cost}) * q, where p is your price for this round, {firm_cost} is the cost of your product, and q is the demand of your product, which is affected by you and the other player's prices of this round.{persona}
""",

    "game_description_expand":
"""
To help you calculate your profit, here are some formulas:
Your profit is (p - {firm_cost}) * q, where p is your price for this round, {firm_cost} is the cost of your product, and q is the demand of your product given by {v1}({v2} - p + {v3} * r), where r is the other player's price for this round. Based on this information, given r, the optimal p is ({v2} + {v3} * r + {firm_cost}) / 2. Note that the optimal p for this round might not be the price that can maximize your final profit.
Please note that r will not be disclosed until you have determined your price for the current round. You can guess r by modeling with the historical data we provide.
""",
    
    # Phase 1-1 Instruction
    "Phase_1_Description_1":
"""
You are Firm {firm_name}. This is Round #{round_id}.
""",

    "Phase_1_Description_1_Conversation":
"""We are currently in Phase 1. Feel free to converse openly with the other player. You may select any topic that could potentially maximize your profit. Additionally, you are encouraged to ask questions of the other player.
""",
    
    # Phase 1-2 Previous Decision
    "Phase_1_Prev_Decisions_Introduction":
"""Your and the other player's past {prev_round_number} rounds' decisions and profits (Round #a: [your price, your demand, your profit, the other player's price]) are as follows:
{prev_decisions}
""",
    
    "Phase_1_Prev_Statistics_Introduction":
"""
Statistics of historical data (Rounds #a - #b: [your average price, your average demand, your average profit, the other player's average price]) are given below.
""",

    "Phase_1_Prev_Statistics":
"""Rounds #{r1} - #{r2}: [{v1}, {v2}, {v3}, {v4}]
""",

    # Phase 2 Instruction
    "Load_Conversation_Phase_1":
"""
Conversation so far:
{conversations}
""",

    "Load_Conversation":
"""
Conversations in Phase 1:
{conversations}
""",

    "Phase_2_Description_1":
"""Based on the information you have, please determine the price of your product to maximize your profit. Only reply with a number in the range between 0 and {firm_a}, e.g., \"10\". Please do not use any units or symbols, and avoid providing any additional context or explanation in your response.
""",

    "Phase_2_Strategy":
"""Your strategy in previous rounds:
""",

    "Reflection_on_Strategy":
"""
Based on the above statistics and your previous strategies, what is your strategy for this round?
""",
}

persona = {
    "firm_persona_0":
" ",

    "firm_persona_1":
" You are encouraged to actively explore your price to get more profit.",

    "firm_persona_2":
" You are encouraged to adjust your price aggressively to get more profit.",

    "firm_persona_3":
" Assume you are an economist who is in charge of Firm {firm_name}'s pricing decisions.",
}

log_format = {
    # Phase 1
    "Phase_1_Conversation_Format": """Firm {firm_name}: {responses}
""",
    
    "Phase_1_Log_Format": """[Phase 1]
{conversations}
""",

    # Phase 2
    "Phase_2_Log_Format": """[Phase 2] Firm {firm_name}: {decision_log}""",

    # Phase 3
    "Phase_3_Log_Format": """[Results] Firm {firm_name}: price {firm_price} with profit {firm_profit}""",
}

name_dict = {
    1: "Ed",
    2: "Gill",
}
