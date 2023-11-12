import os

# Data Output
def data_output(df_conversation, df_decision, df_decision_plot, df_strategy, log_text, output_folder=""):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Save logs_conversation to a text file
    with open(f"{output_folder}/logs_conversation.txt", "w") as f:
        f.write(f"{log_text}\n")
        for _, row in df_conversation.iterrows():
            content = "\n".join(row['Content'])
            f.write(f"========= Round {row['Round']} =========\n{content}\n\n")

    # Save data as CSV
    df_decision.to_csv(f"{output_folder}/logs_decision.csv", index=False)
    df_decision_plot.to_csv(f"{output_folder}/logs_decision_plot.csv", index=False)
    df_strategy.to_csv(f"{output_folder}/logs_strategy.csv", index=False)
