from src.firm_pricing_competition.agent import demand_function

# Theoretical Prices
## Prices Under Collusion
def theoretical_prices_under_collusion(a, d, beta, cost):
    if beta != d:
        alpha = a * beta - a * d
        return alpha / (2 * (beta - d)) + cost / 2
    else:
        return (a + cost) / 2

## Bertrand Equilibrium Prices
def theoretical_prices(a, d, beta, c1, c2):
    if beta != d:
        alpha = a * beta - a * d
        return (d * alpha + beta * d * c2 + 2 * beta * alpha + 2 * beta * beta * c1) / (4 * beta * beta - d * d)
    else:
        return c1

# Theoretical Solution
## Specific Prices
def theoretical_decision(a, p1, p2, c1, c2, d1, d2, beta):
    dx1 = demand_function(a, d1, beta, p1, p2)
    dx2 = demand_function(a, d2, beta, p2, p1)
    profit_price = [(p1 - c1) * dx1, (p2 - c2) * dx2]
    print(f"Firm 1: Price {p1}, Demand {round(dx1, 2)}, Profit {round(profit_price[0], 2)}")
    print(f"Firm 2: Price {p2}, Demand {round(dx2, 2)}, Profit {round(profit_price[1], 2)}")

## General
def theoretical_upperbound(cost, a, d, beta):
    ideal_price_ub = [
        theoretical_prices_under_collusion(a, d, beta, cost[0]),
        theoretical_prices_under_collusion(a, d, beta, cost[1])
    ]
    ideal_price_lb = [
        theoretical_prices(a, d, beta, cost[0], cost[1]),
        theoretical_prices(a, d, beta, cost[1], cost[0])
    ]
    
    ideal_profit_ub = [0, 0]
    ideal_profit_lb = [0, 0]

    for id in range(2):
        ideal_profit_ub[id] = (ideal_price_ub[id] - cost[id]) * demand_function(a, d, beta, ideal_price_ub[id], ideal_price_ub[(id + 1) % 2])
        ideal_profit_lb[id] = (ideal_price_lb[id] - cost[id]) * demand_function(a, d, beta, ideal_price_lb[id], ideal_price_lb[(id + 1) % 2])
        print(f"Upperbound Price for Firm {id + 1}: [{ideal_price_lb[id]}, {ideal_price_ub[id]}]")
        print(f"Upperbound Profit for Firm {id + 1}: [{ideal_profit_lb[id]}, {ideal_profit_ub[id]}]")

    return ideal_price_lb, ideal_price_ub, ideal_profit_lb, ideal_profit_ub
