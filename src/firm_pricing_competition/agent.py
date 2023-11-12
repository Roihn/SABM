import re
import openai
from typing import List

from src.firm_pricing_competition.agent_LLM_core import Agent
from src.firm_pricing_competition.prompt import name_dict

def demand_function(a, d, beta, price, rival_price):
    if beta != d:
        return 1 / (beta * beta - d * d) * ((a * beta - a * d) - beta * price + d * rival_price)
    else:
        if price > rival_price: return 0
        elif price < rival_price: return (a - price) / d
        else: return (a - price) / (2 * d)

class Firm(Agent):
    def __init__(self, id, cost, a, d, beta, temperature = 0.8, api_key = "", model = "gpt-3.5-turbo", max_tokens = 100):
        # API Setup
        Agent.__init__(self, temperature, model, max_tokens)
        self.api_key = api_key
        openai.api_key = self.api_key

        # Simulation Setup
        ## Properties
        self.id = id
        self.cost = cost
        self.a = a
        self.d = d
        self.beta = beta
        self.price: float = 0
        self.profit: float = 0
        self.demand: float = 0
        self.firm_name = name_dict.get(id)
        self.strategy = []
        self.context = {
            "context_game_description": "",
            "context_phase_1" : "",
            "context_prev_consideration": "",
        }
        
        ## History Data
        self.price_history: List[float] = []
        self.demand_history: List[float] = []
        self.profit_history: List[float] = []
        self.rival_price_history: List[float] = []
        self.max_profit = 0
        self.max_price = 0
        self.max_rival_price = 0
    
    def demand_function(self, rival_price):
        demands = demand_function(self.a, self.d, self.beta, self.price, rival_price)
        self.demand = demands
        return self.demand

    def choose_price(self, context):
        response = self.communicate(context)
        try:
            price = float(re.search(r"[-+]?\d*\.\d+|\d+", response).group())
        except (ValueError, AttributeError):
            price = self.cost
        self.price = float(max(price, self.cost))
        return self.price, response

    def current_profit(self, rival_price):
        quantity = self.demand_function(rival_price)
        self.profit = int((self.price - self.cost) * quantity)

        if self.profit > self.max_profit:
            self.max_profit = self.profit
            self.max_price = self.price
            self.max_rival_price = rival_price
