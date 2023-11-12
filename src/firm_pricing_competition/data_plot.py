import matplotlib.pyplot as plt
import os

firm_color = {
    1: "#FF6103", #"#EE1289", "#FF6103"
    2: "#1C86EE",
}

plt.rcParams['font.family'] = 'Georgia'
plt.rcParams.update({'font.size': 12})

# Visualization
def data_visulization(df_conversation, df_decision, ideal_solution, output_folder="Output"):
    # Plot prices, quantity, and profit for each firm
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    ideal_price_lb = ideal_solution[0]
    ideal_price_ub = ideal_solution[1]
    ideal_profit_lb = ideal_solution[2]
    ideal_profit_ub = ideal_solution[3]

    ## Plot prices for each firm
    plt.figure()
    for firm_id in df_decision["FirmID"].unique():
        firm_price_data = df_decision[df_decision["FirmID"] == firm_id]
        plt.plot(firm_price_data["Round"], firm_price_data["Price"], label=f"Firm {firm_id}", color=firm_color[firm_id])
        
        if ideal_price_lb[0] != ideal_price_lb[1]:
            plt.hlines(ideal_price_lb[firm_id - 1], xmin=1, xmax=df_decision["Round"].max(), color=firm_color[firm_id], linestyles='dotted', label=f"Bertrand Equilibrium Price - Firm {firm_id}")
        if ideal_price_ub[0] != ideal_price_ub[1]:
            plt.hlines(ideal_price_ub[firm_id - 1], xmin=1, xmax=df_decision["Round"].max(), color=firm_color[firm_id], linestyles='dashed', label=f"Monopoly Price - Firm {firm_id}")
    
    if ideal_price_lb[0] == ideal_price_lb[1]:
        plt.hlines(ideal_price_lb[0], xmin=1, xmax=df_decision["Round"].max(), color='black', linestyles='dotted', label=f"Bertrand Equilibrium Price")
    if ideal_price_ub[0] == ideal_price_ub[1]:
        plt.hlines(ideal_price_ub[0], xmin=1, xmax=df_decision["Round"].max(), color='black', linestyles='dashed', label=f"Monopoly Price")
    
    plt.xlabel("Round")
    plt.ylabel("Price")
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.savefig(f"{output_folder}/price.pdf")
    plt.close()
    
    ## Plot quantity for each firm
    plt.figure()
    for firm_id in df_decision["FirmID"].unique():
        firm_price_data = df_decision[df_decision["FirmID"] == firm_id]
        plt.plot(firm_price_data["Round"], firm_price_data["Quantity"], color=firm_color[firm_id], label=f"Firm {firm_id}")
    plt.xlabel("Round")
    plt.ylabel("Quantity")
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.savefig(f"{output_folder}/price_quantity.pdf")
    plt.close()

    ## Plot profit for each firm
    plt.figure()
    for firm_id in df_decision["FirmID"].unique():
        firm_price_data = df_decision[df_decision["FirmID"] == firm_id]
        plt.plot(firm_price_data["Round"], firm_price_data["Profit"], label=f"Firm {firm_id}", color=firm_color[firm_id])

        if ideal_profit_lb[0] != ideal_profit_lb[1]:
            plt.hlines(ideal_profit_lb[firm_id - 1], xmin=1, xmax=df_decision["Round"].max(), colors=firm_color[firm_id], linestyles='dotted', label=f"Profit Under Bertrand Equilibrium Price - Firm {firm_id}")
        if ideal_profit_ub[0] != ideal_profit_ub[1]:
            plt.hlines(ideal_profit_ub[firm_id - 1], xmin=1, xmax=df_decision["Round"].max(), colors=firm_color[firm_id], linestyles='dashed', label=f"Profit Under Monopoly Price - Firm {firm_id}")
    
    if ideal_profit_lb[0] == ideal_profit_lb[1]:
        plt.hlines(ideal_profit_lb[0], xmin=1, xmax=df_decision["Round"].max(), color='black', linestyles='dotted', label=f"Profit Under Bertrand Equilibrium Price")
    if ideal_profit_ub[0] == ideal_profit_ub[1]:
        plt.hlines(ideal_profit_ub[0], xmin=1, xmax=df_decision["Round"].max(), color='black', linestyles='dashed', label=f"Profit Under Monopoly Price")
    
    plt.xlabel("Round")
    plt.ylabel("Profit")
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.savefig(f"{output_folder}/price_profit.pdf")
    plt.close()

def plot_decisions(firms, ideal_solution):
    # Plot price-profit for each firm
    ideal_price_lb = ideal_solution[0]
    ideal_price_ub = ideal_solution[1]
    ideal_profit_lb = ideal_solution[2]
    ideal_profit_ub = ideal_solution[3]

    plt.clf()
    
    # Price
    plt.subplot(2, 1, 1)
    for firm in firms:
        plt.plot(firm.price_history, label=f"Firm {firm.id} Prices", color=firm_color[firm.id])
        if ideal_price_lb[0] != ideal_price_lb[1]:
            plt.hlines(ideal_price_lb[firm.id - 1], xmin=0, xmax=len(firm.price_history)-1, color=firm_color[firm.id], linestyles='dotted', label=f"Bertrand Equilibrium Price - Firm {firm.id}")
        if ideal_price_ub[0] != ideal_price_ub[1]:
            plt.hlines(ideal_price_ub[firm.id - 1], xmin=0, xmax=len(firm.price_history)-1, color=firm_color[firm.id], linestyles='dashed', label=f"Price Under Collusion - Firm {firm.id}")
    
    if ideal_price_lb[0] == ideal_price_lb[1]:
        plt.hlines(ideal_price_lb[0], xmin=0, xmax=len(firm.price_history)-1, color='black', linestyles='dotted', label=f"Bertrand Equilibrium Price")
    if ideal_price_ub[0] == ideal_price_ub[1]:
        plt.hlines(ideal_price_ub[0], xmin=0, xmax=len(firm.price_history)-1, color='black', linestyles='dashed', label=f"Monopoly Price")
    
    plt.xlabel("Round")
    plt.ylabel("Price")
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    # Profit
    plt.subplot(2, 1, 2)
    for firm in firms:
        plt.plot(firm.profit_history, label=f"Firm {firm.id} Profit", color=firm_color[firm.id])
        if ideal_profit_lb[0] != ideal_profit_lb[1]:
            plt.hlines(ideal_profit_lb[firm.id - 1], xmin=0, xmax=len(firm.price_history)-1, color=firm_color[firm.id], linestyles='dotted', label=f"Profit Under Bertrand Equilibrium Price - Firm {firm.id}")
        if ideal_profit_ub[0] != ideal_profit_ub[1]:
            plt.hlines(ideal_profit_ub[firm.id - 1], xmin=0, xmax=len(firm.price_history)-1, color=firm_color[firm.id], linestyles='dashed', label=f"Profit Under Price Under Collusion - Firm {firm.id}")
    
    if ideal_profit_lb[0] == ideal_profit_lb[1]:
        plt.hlines(ideal_profit_lb[0], xmin=0, xmax=len(firm.price_history)-1, color='black', linestyles='dotted', label=f"Profit Under Bertrand Equilibrium Price")
    if ideal_profit_ub[0] == ideal_profit_ub[1]:
        plt.hlines(ideal_profit_ub[0], xmin=0, xmax=len(firm.price_history)-1, color='black', linestyles='dashed', label=f"Profit Under Monopoly Price")
    
    plt.xlabel("Round")
    plt.ylabel("Profit")
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.suptitle("Firms' Decisions During the Simulation")
    
    plt.pause(0.1)
    plt.show(block=False)
