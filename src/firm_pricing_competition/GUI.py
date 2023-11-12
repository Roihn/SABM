import tkinter as tk
from tkinter import ttk

class gui:
    def __init__(self):
        self.root = tk.Tk()
        self.data = None

        self.root.title("Smart Agents Online: Collusion Simulation")

        self.cost_label = ttk.Label(self.root, text="Cost Parameters:")
        self.cost1_entry = ttk.Entry(self.root)
        self.cost2_entry = ttk.Entry(self.root)

        self.a_label = ttk.Label(self.root, text="Parameter 'a':")
        self.a_entry = tk.Entry(self.root, bg='gray')

        self.d_label = ttk.Label(self.root, text="Parameter 'd':")
        self.d_entry = ttk.Entry(self.root)

        self.beta_label = ttk.Label(self.root, text="Parameter 'β':")
        self.beta_entry = ttk.Entry(self.root)

        self.p_label = ttk.Label(self.root, text="Initial Prices:")
        self.p1_entry = ttk.Entry(self.root)
        self.p2_entry = ttk.Entry(self.root)

        self.load_data_label = ttk.Label(self.root, text="Load Data:")
        self.load_data_entry = ttk.Entry(self.root)

        self.load_strategy_label = ttk.Label(self.root, text = 'Load Strategy:')
        self.load_strategy_entry = ttk.Combobox(self.root, values = ['True', 'False'])

        self.has_conversation_label = ttk.Label(self.root, text = 'Conversation:')
        self.has_conversation_entry = ttk.Combobox(self.root, values = ['False', 'True'])


        self.submit_button = ttk.Button(self.root, text="Run Simulation", command=self.on_submit)

        # Set default values
        self.cost1_entry.insert(0, '2')
        self.cost2_entry.insert(0, '2')
        self.a_entry.insert(0, '14')
        self.d_entry.insert(0, '0.00333333333333')
        self.p1_entry.insert(0, '2')
        self.p2_entry.insert(0, '2')
        self.beta_entry.insert(0, '0.00666666666666')
        self.load_data_entry.insert(0, '')
        self.load_strategy_entry.insert(0, 'True')
        self.has_conversation_entry.insert(0, 'False')

        # Set interface
        self.cost_label.grid(row=0, column=0, sticky='w')
        self.cost1_entry.grid(row=0, column=1)
        self.cost2_entry.grid(row=0, column=2)

        self.a_label.grid(row=1, column=0, sticky='w')
        self.a_entry.grid(row=1, column=1)

        self.d_label.grid(row=2, column=0, sticky='w')
        self.d_entry.grid(row=2, column=1)

        self.beta_label.grid(row=3, column=0, sticky='w')
        self.beta_entry.grid(row=3, column=1)

        self.p_label.grid(row=4, column=0, sticky='w')
        self.p1_entry.grid(row=4, column=1)
        self.p2_entry.grid(row=4, column=2)

        self.load_data_label.grid(row=5, column=0, sticky='w')
        self.load_data_entry.grid(row=5, column=1)

        self.load_strategy_label.grid(row=6, column=0, sticky='w')
        self.load_strategy_entry.grid(row=6, column=1)

        self.has_conversation_label.grid(row=7, column=0, sticky='w')
        self.has_conversation_entry.grid(row=7, column=1)

        self.a_entry.config(state='readonly')

        self.submit_button.grid(row=8, column=0, columnspan=3, pady=10)


    def on_submit(self):
        para_cost = [int(self.cost1_entry.get()), int(self.cost2_entry.get())]
        para_a = int(self.a_entry.get())
        para_d = float(self.d_entry.get())
        para_beta = float(self.beta_entry.get())
        initial_price = [int(self.p1_entry.get()), int(self.p2_entry.get())]
        load_data_key = self.load_data_entry.get()
        load_strategy = self.load_strategy_entry.get()
        has_conversation_data = self.has_conversation_entry.get()
        
        if load_data_key != '':
            load_data = f"Output/{load_data_key}/"
        else:
            load_data = ''
        
        if load_strategy == 'True': strategy = True
        else: strategy = False

        if has_conversation_data == 'True': has_conversation = True
        else: has_conversation = False
        
        self.data = para_cost, para_a, para_d, para_beta, initial_price, load_data, strategy, has_conversation

        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.data
