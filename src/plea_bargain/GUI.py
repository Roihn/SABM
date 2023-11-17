import tkinter as tk
from tkinter import ttk
from src.plea_bargain.prompt_plea_bargain import GUI_init_number

class gui:
    def __init__(self):
        def automatic_setup():
            group_num = self.question_entry.get()

            if group_num in GUI_init_number.keys():
                self.situation_num_entry.config(state='normal')
                self.group_num_entry.config(state='normal')
                self.group_num_entry.delete(0, "end")
                self.group_num_entry.insert(0, GUI_init_number[group_num][0])
                self.situation_num_entry.delete(0, "end")
                self.situation_num_entry.insert(0, GUI_init_number[group_num][1])
                self.situation_num_entry.config(state='readonly')
                self.group_num_entry.config(state='readonly')
            
            return True
        
        self.data = None

        self.root = tk.Tk()
        self.root.title("Smart Agents Online: Plea Bargain Simulation")

        self.N_label = ttk.Label(self.root, text = 'Number of Agents per Group:')
        self.N_entry = ttk.Entry(self.root)

        self.question_label = ttk.Label(self.root, text = 'Sub-Task Number:')
        self.question_entry = ttk.Entry(self.root, validate='focusout', validatecommand=automatic_setup)

        self.situation_num_label = ttk.Label(self.root, text = 'Number of Scenarios:')
        self.situation_num_entry = tk.Entry(self.root, bg='gray')

        self.group_num_label = ttk.Label(self.root, text = 'Number of Groups:')
        self.group_num_entry = tk.Entry(self.root, bg='gray')

        self.specific_group_label = ttk.Label(self.root, text = 'Test Specific Group:')
        self.specific_group_entry = ttk.Combobox(self.root, values = ['None', '1', '2', '3'])
            
        self.submit_button = ttk.Button(self.root, text="Run Simulation", command=self.on_submit)

        # Set default values
        self.N_entry.insert(0, '100')
        self.question_entry.insert(0, '1')
        self.group_num_entry.insert(0, '3')
        self.situation_num_entry.insert(0, '1')
        self.specific_group_entry.insert(0, 'None')
        
        self.N_label.grid(row=0, column=0, sticky = 'w')
        self.N_entry.grid(row=0, column=1)

        self.question_label.grid(row=1, column=0, sticky = 'w')
        self.question_entry.grid(row=1, column=1)

        self.group_num_label.grid(row=2, column=0, sticky = 'w')
        self.group_num_entry.grid(row=2, column=1)
        self.situation_num_label.grid(row=3, column=0, sticky = 'w')
        self.situation_num_entry.grid(row=3, column=1)

        self.specific_group_label.grid(row=4, column=0, sticky = 'w')
        self.specific_group_entry.grid(row=4, column=1)

        self.situation_num_entry.config(state='readonly')
        self.group_num_entry.config(state='readonly')

        self.submit_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    def on_submit(self):
        N = int(self.N_entry.get())

        group_num = int(self.group_num_entry.get())
        situation_num = int(self.situation_num_entry.get())
        question = str(self.question_entry.get())
        specific_group_number = str(self.specific_group_entry.get())


        if specific_group_number == 'None':
            self.data = N * group_num, group_num, situation_num, question, specific_group_number
        else:
            specific_group_number = int(specific_group_number)
            if specific_group_number > group_num:
                print("Group Number Value Error!")
                self.data = -1, -1, -1, -1, -1
            else:
                group_num = 1
                self.data = N * group_num, group_num, situation_num, question, specific_group_number
        
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()
        return self.data
