from multi_agents import Agent
import openai
import time
from textwrap import dedent

GROUP1_ATTRIBUTES = {
    "N0": [0, 0.1, 0.1, 0.3, 0.3, 0.2],
    "Y0": 20,
    "Z0": 30,
    "alpha1": 2.4,
    "alpha2": 3.6,
    "alpha3": 1.2,
    "alpha4": 2.4,
    "alpha5": 3.6,
    "alpha6": 1.2,
    "group_id": 1,
}

GROUP2_ATTRIBUTES = {
    "N0": [0.1, 0.1, 0.2, 0.3, 0.2, 0.1],
    "Y0": 15,
    "Z0": 28,
    "alpha1": 4.0,
    "alpha2": 4.0,
    "alpha3": 1.6,
    "alpha4": 4.0,
    "alpha5": 4.0,
    "alpha6": 1.6,
    "group_id": 2,
}

GROUP3_ATTRIBUTES = {
    "N0": [0.1, 0.2, 0.3, 0.2, 0.1, 0.1],
    "Y0": 18,
    "Z0": 25,
    "alpha1": 6.0,
    "alpha2": 1.8,
    "alpha3": 1.8,
    "alpha4": 6.0,
    "alpha5": 1.8,
    "alpha6": 1.8,
    "group_id": 3,
}

GROUP4_ATTRIBUTES = {
    "N0": [0.2, 0.3, 0.3, 0.1, 0.1, 0],
    "Y0": 15,
    "Z0": 23,
    "alpha1": 6.0,
    "alpha2": 1.5,
    "alpha3": 1.2,
    "alpha4": 6.0,
    "alpha5": 1.5,
    "alpha6": 1.2,
    "group_id": 4,
}

CM_ATTRIBUTES = {
    0: "positive",
    1: "negative",
}

CAPABILITY_PROMPTS = {
    0: "positive and full of energy.",
    1: "negative and afraid of difficulties.",
}

MENTAL_PROMPTS = {
    0: "And you are strong and fit.",
    1: "And you are not a strong person."
}

N0_mean = {
    0: 3,
    1: 2,
}

Y0_mean = {
    0: 18,
    1: 16,
}

Z0_mean = {
    0: 26,
    1: 23,
}

def get_direction(agent_pos, exit_pos):
    dx = exit_pos[0] - agent_pos[0]
    dy = exit_pos[1] - agent_pos[1]
    if dx == 0 and dy > 0:
        return "right"
    if dx == 0 and dy < 0:
        return "left"
    if dx > 0 and dy == 0:
        return "bottom"
    if dx < 0 and dy == 0:
        return "top"
    if dx > 0 and dy > 0:
        return "bottom right"
    if dx > 0 and dy < 0:
        return "bottom left"
    if dx < 0 and dy > 0:
        return "top right"
    if dx < 0 and dy < 0:
        return "top left"

def get_negative_example(agent_pos, exit_pos):
    dx = exit_pos[0] - agent_pos[0]
    dy = exit_pos[1] - agent_pos[1]
    if dx == 0 and dy > 0:
        return f"2 - go left to {(agent_pos[0], agent_pos[1] - 1)}"
    if dx == 0 and dy < 0:
        return f"0 - go right to {(agent_pos[0], agent_pos[1] + 1)}"
    if dx > 0 and dy == 0:
        return f"3 - go up to {(agent_pos[0] - 1, agent_pos[1])}"
    if dx < 0 and dy == 0:
        return f"1 - go down to {(agent_pos[0] + 1, agent_pos[1])}"
    if dx > 0 and dy > 0:
        return f"7 - go up and left to {(agent_pos[0] - 1, agent_pos[1] - 1)}"
    if dx > 0 and dy < 0:
        return f"8 - go up and right to {(agent_pos[0] - 1, agent_pos[1] + 1)}"
    if dx < 0 and dy > 0:
        return f"6 - go down and left to {(agent_pos[0] + 1, agent_pos[1] - 1)}"
    if dx < 0 and dy < 0:
        return f"5 - go down and right to {(agent_pos[0] + 1, agent_pos[1] + 1)}"


class Human(Agent):
    def __init__(self, id: int, pos, width, height, attribute, seed=0, history_buffer_length=10, model="gpt-4-0314", api_key=None):
        super().__init__(id, str(id), seed)
        self.cur_pos = pos
        self.init_pos = pos
        self.env_width = width
        self.env_height = height
        self.action_history = []
        # self.N0 = attribute["N0"]
        # self.Y0 = attribute["Y0"]
        # self.Z0 = attribute["Z0"]
        # self.alpha1 = attribute["alpha1"]
        # self.alpha2 = attribute["alpha2"]
        # self.alpha3 = attribute["alpha3"]
        # self.alpha4 = attribute["alpha4"]
        # self.alpha5 = attribute["alpha5"]
        # self.alpha6 = attribute["alpha6"]

        self.capability = attribute["capability"]
        self.mental = attribute["mental"]

        self.N0 = self.rng.normal(N0_mean[self.capability], 1)
        self.Y0 = self.rng.normal(Y0_mean[self.capability], 1)
        self.Z0 = self.rng.normal(Z0_mean[self.capability], 1)
        
        self.capability_text = CM_ATTRIBUTES[self.capability]
        self.mental_text = CM_ATTRIBUTES[self.mental]
        self.status = "normal"
        # self.group_id = attribute["group_id"]
        self.pos_history = [self.init_pos]
        self.model = model
        self.api_key = api_key
        self.response1 = ""
        self.response2 = ""
        self.response3 = ""
        self.response4 = ""

        self.action = None
        self.target_exit = None

        self.Z = 0
        # for state
        self.reset_cur_state()

        self.state_history = []
        self.history_buffer_length = history_buffer_length
        self.target_exit_history = []


    def words_split(self, response):
        # Define valid words
        valid_words = ['minimal', 'mild', 'moderate', 'high', 'extreme']
        
        # if response end with a period, remove it
        if response[-1] == '.':
            response = response[:-1]

        # Split the string into words by comma
        words = [word.strip() for word in response.split(',')]

        # Check if there are exactly three words
        # if len(words) != 3:
        if len (words) != 2:
            return False, "Input string should contain exactly two words."
        
        # Check if all words are in the valid words list
        for word in words:
            if word not in valid_words:
                return False, f"Invalid word '{word}'. Only these words are allowed: {valid_words}"
                
        # If all checks pass, return the words
        return True, words

    def get_attribute_prompt(self):
        prompt = f"{CAPABILITY_PROMPTS[self.capability]} {MENTAL_PROMPTS[self.mental]}"
        return prompt

    @property
    def persona(self):
        prompt = f"{CAPABILITY_PROMPTS[self.capability]} {MENTAL_PROMPTS[self.mental]}"
        return prompt

    def reset(self):
        self.cur_pos = self.init_pos
        self.action_history = []
    
    def reset_cur_state(self):
        self.dist_to_nearest_exit = float('inf')
        self.velocity = 0
        self.response1 = ""
        self.response2 = ""
        self.response3 = ""
        self.response4 = ""
        self.action = None

    def move(self, action: int):
        if action == 0:
            # move right
            if self.cur_pos[0] < self.env_width - 1:
                self.cur_pos[0] += 1
        elif action == 1:
            # move downward
            if self.cur_pos[1] < self.env_height - 1:
                self.cur_pos[1] += 1
        elif action == 2:
            # move left
            if self.cur_pos[0] > 0:
                self.cur_pos[0] -= 1
        elif action == 3:
            # move upward
            if self.cur_pos[1] > 0:
                self.cur_pos[1] -= 1
        elif action == 4:
            # stay
            pass
        else:
            raise ValueError("Invalid action.")
        self.action_history.append(action)
        return self.cur_pos
    
    def get_action_history(self):
        return self.action_history
    
    def __repr__(self) -> str:
        return super().__repr__() + f" at {self.cur_pos}, with N0 = {self.N0}"


    def update_state_history(self, state):
        """Update state history buffer.
        
        Args:
            state (dict): stores the current agent's beta1, beta2, and beta3.
            
        """
        self.state_history.append(state)

    
    def get_state_history(self):
        """Return the state history buffer.
        
        **Won't use in case 2.**

        Returns:
            list: a list of state history.
            
        """
        prompt = "Your latest chat history:"
        if len(self.state_history) == 0:
            prompt += " None yet."
        # get the latest 10 states
        for state in self.state_history[-self.history_buffer_length:]:
            # get text form of beta1, beta2, beta3
            round, beta1, beta2, beta3 = state["round"], state["beta1"], state["beta2"], state["beta3"]
            num_agents_around, dist_to_nearest_exit = state['num_agents_around'], state['dist_to_nearest_exit']
            prompt += dedent(f"""\
                Round {round}: There are {num_agents_around:.2f} people around you (8 at most).
                The distance to Nearest exit is {dist_to_nearest_exit:.2f}.
                Your inclination: Exit Proximity: {beta1}, People Count: {beta2}, Crowd Density: {beta3}
            """)
        return dedent(prompt)
    
    def form_communication_stage(self, persona, data, communicate_samples):
        prompt = f"You are a person that {persona}.\n"
        for exit_id, exit in data.items():
            dist_to_exit = exit['dist']
            num_agents_around = exit['num_agents_around']
            prompt += dedent(f"""Exit {exit_id}: {dist_to_exit:.2f} away, {num_agents_around:.2f} people around. \n""")

        if len(communicate_samples) > 0:
            prompt += f"You hear {len(communicate_samples)} people around you say:\n"
            for agent_id, sample in communicate_samples:
                prompt += dedent(f"""agent#{agent_id}: {sample}\n""")
        
        prompt += dedent(f"""You may briefly share information about evacuation with others, such as your feeling, which exit seems to be the best option for a quick escape, or anything else you would like to deliver. Avoid using numbers in the communication. Use less than 50 words, not too long.""")

        return dedent(prompt)

    def form_current_state_stage1(self, persona, num_agents_around, dist_to_nearest_exit):
        prompt = f"The distance to Nearest exit is {dist_to_nearest_exit:.2f}."
        prompt += dedent(f"""\
            And there are {num_agents_around} people in your visible range.
            You are a person that {persona} Please tell me your feeling about the situation around you in one sentence showing if you are panic or not.
            """)
        return dedent(prompt)
    
    # def form_current_state_stage2(self, round, panic_level_str, data):
    #     prompt = dedent("""\
    #         To escape from the room, you need to consider the following three aspects: Exit proximity, people count, and crowd density.
    #         The exit proximity is the distance between you and the nearest exit. The people count is the number of people you can see. The crowd density is the density of people you can see.
    #         """)
    #     prompt += dedent(f"""\
    #         Now at round {round}, you feel like: "{panic_level_str}".

    #         Here shows you the distances to different exits, the number of people you can see towards those exits, and the related crowdess.
    #         """)
        
    #     for exit_id, exit in data.items():
    #         dist_to_exit = exit['dist']
    #         num_agents_around = exit['num_agents_around']
    #         crowdness = exit['crowdness']
    #         prompt += dedent(f"""\
    #             Exit {exit_id}: {dist_to_exit:.2f} away, {num_agents_around} people around, crowdness: {crowdness:.2f}
    #         """)
        
    #     prompt += dedent(f"""\
    #         Please tell me your feeling to the three aspects of each exit. For each aspect, please use one of the five words listed below:
    #         [minimal, mild, moderate, high, extreme]
    #         Your output should only contain {len(data)} lines of words. For each line, it contains three words, with comma between them.
    #         For example, 'minimal, mild, moderate' is a valid output of one line, which means you feel the exit has minimal distance to you, and moderate number of people around. No period at the end.
    #         """)

    #     return dedent(prompt)
    
    def form_current_state_stage2(self, persona, panic_level_str, data):
        prompt = f"You are a person that {persona}"
        prompt += dedent(f"""Now you feel: "{panic_level_str}".Here shows you the distances to different exits and the number of people you can see towards those exits.""")
        
        for exit_id, exit in data.items():
            dist_to_exit = exit['dist']
            num_agents_around = exit['num_agents_around']
            prompt += dedent(f"""Exit {exit_id}: {dist_to_exit:.2f} away, {num_agents_around:.2f} people around.\n""")
        prompt += dedent(f"""Please tell me briefly how will you evaluate the two aspects of each exit based on your personal mental and physical characteristics in one sentence. Please give 3 sentences for each exit (around 15 words).""")

        return dedent(prompt)

    
    def form_current_state_stage3(self, persona, stage1_feeling, evaluation, communicate_samples):
        prompt = f"You are a person that {persona}"
        prompt += dedent(f"""Now you feel: \"{stage1_feeling}\".There are 3 exits in this room. Base on the current situation, your personal feeling on each exit are:
{evaluation}""")
        if len(communicate_samples) == 0:
            prompt += "No one is talking around you."
        else:
            prompt += f"You hear {len(communicate_samples)} people around you say:\n"
            for agent_id, sample in communicate_samples:
                prompt += dedent(f"""agent#{agent_id}: {sample}\n""")
        target_exit = None
        if self.target_exit:
            if self.target_exit.pos[1] == 0:
                target_exit = "left"
            elif self.target_exit.pos[0] == 32:
                target_exit = "bottom"
            else:
                target_exit = "right"
        prompt += dedent(f"""
Here are the previous decisions you made for the target exit from the beginning: {self.target_exit_history}.
This means most recently you were heading to exit {target_exit}. Please keep these in mind when you make your decision.
Please tell me which exit you would like to choose to escape, and you always want to escape as quick as possible. Please use the exit id to indicate your choice. 
For example, if you want to choose exit left, you can say 'left'. Only output one word of text to indicate your choice.
You can choose from ['bottom', 'left', 'right']. Give your answer without any additional text.
            """)
        # print(prompt)
        # exit()

        return dedent(prompt)
    
    def form_action(self, target_exit, cur_pos, move_list, action_count):
        # agent_pos = (agent_pos[0] + 1, agent_pos[0] + 1)
        agent_pos = cur_pos
        last_pos = self.pos_history[-2] if len(self.pos_history) > 1 else None
        exit_pos = target_exit.pos
        # exit_pos = (target_exit.pos[0] + 1, target_exit.pos[1] + 1)
        if last_pos:
            prompt = dedent(f"""\
            You were at {last_pos} last time.
            """)
        else:
            prompt = ""
        prompt += dedent(f"""\
            To escape from the room, you have chosen the exit at {exit_pos} and you are at {cur_pos}, so the exit is on your {get_direction(agent_pos, exit_pos)}.
            Select your move from these possible options (You can move in diagonal or horizontal directions, options with obstacles or other people are excluded and not in the path, and option codes are in random order):
            {move_list}
            Please tell me your best choice to escape as fast as possible with one single code without any additional texts. You can choose from 'a' to '{chr(ord('a') + action_count - 1)}'.
            """)

        return dedent(prompt)


    def communicate(self, context, reject_func=None):
        prompt = context + "\n\n"
        # print(prompt)
        self.max_tokens = 512
        self.temperature = 0
        message = ""

        retries = 5
        backoff_factor = 2
        current_retry = 0

        openai.api_key = self.api_key

        while current_retry < retries:
            try:
                # start = time.time()
                # print("start", start)
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt},
                        # {"role": "user", "content": ""}
                    ],
                    max_tokens=self.max_tokens,
                    n=1,
                    temperature=self.temperature,
                    top_p=1
                )
                # print("end", time.time() - start)
                message = response['choices'][0]['message']['content'].strip()
                if reject_func is not None and reject_func(message):
                    raise ValueError(f"Invalid response, response = {message}")
                #print(message)
                return True, message
            # except openai.error.RateLimitError as e:
            #     if current_retry < retries - 1:
            #         wait_time = backoff_factor ** current_retry
            #         print(f"RateLimitError: Retrying in {wait_time} seconds...")
            #         time.sleep(wait_time)
            #         current_retry += 1
            #     else:
            #         print(f"Error {e}")
            #         raise e
            except ValueError as e:
                print(f"ValueError: {e}, retrying...")
                current_retry += 1
                if current_retry == retries:
                    raise e
            except Exception as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry * 2
                    print(f"{e}\nRetrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}. Retries exhausted.")
                    return None, message

