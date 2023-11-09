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

def process_response(response):
    # Define valid words
    valid_words = ['minimal', 'mild', 'moderate', 'high', 'extreme']
    
    # if response end with a period, remove it
    if response[-1] == '.':
        response = response[:-1]

    # Split the string into words by comma
    words = [word.strip() for word in response.split(',')]


    
    # Check if there are exactly three words
    if len(words) != 3:
        return False, "Input string should contain exactly three words."
    
    # Check if all words are in the valid words list
    for word in words:
        if word not in valid_words:
            return False, f"Invalid word '{word}'. Only these words are allowed: {valid_words}"
            
    # If all checks pass, return the words
    return True, words


class Human(Agent):
    def __init__(self, id: int, pos, width, height, attribute, seed=0, history_buffer_length=10, model="gpt-4-0314", api_key=None):
        super().__init__(id, str(id), seed)
        self.cur_pos = pos
        self.init_pos = pos
        self.env_width = width
        self.env_height = height
        self.action_history = []
        self.N0 = attribute["N0"]
        self.Y0 = attribute["Y0"]
        self.Z0 = attribute["Z0"]
        self.alpha1 = attribute["alpha1"]
        self.alpha2 = attribute["alpha2"]
        self.alpha3 = attribute["alpha3"]
        self.alpha4 = attribute["alpha4"]
        self.alpha5 = attribute["alpha5"]
        self.alpha6 = attribute["alpha6"]
        self.status = "normal"
        self.group_id = attribute["group_id"]
        self.pos_history = [self.init_pos]
        self.model = model
        self.api_key = api_key
        self.beta1 = None
        self.beta2 = None
        self.beta3 = None

        self.Z = 0
        # for state
        self.reset_cur_state()

        self.state_history = []
        self.history_buffer_length = history_buffer_length


    def reset(self):
        self.cur_pos = self.init_pos
        self.action_history = []
    
    def reset_cur_state(self):
        self.Y = 0
        self.beta0 = 0
        self.dist_to_nearest_exit = float('inf')
        self.target_exit = None
        self.velocity = 0

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
                Round {round}: There are {num_agents_around} people around you (8 at most).
                The distance to Nearest exit is {dist_to_nearest_exit:.2f}.
                Your inclination: Exit Proximity: {beta1}, People Count: {beta2}, Crowd Density: {beta3}
            """)
        return dedent(prompt)
    
    def form_current_state(self, round, num_agents_around, dist_to_nearest_exit):
        prompt = f"""\
            Now at round {round}, there are {num_agents_around} people around you (8 at most).
            And the distance to Nearest exit is {dist_to_nearest_exit:.2f}.
            Please tell me your inclination: Exit Proximity, People Count, Crowd Density.
            For each aspect, please use one of the five words listed below:
            [minimal, mild, moderate, high, extreme]
            Your output should only contain three words, with comma between them.
            For example, 'minimal, mild, moderate' is a valid output. No period at the end.
            This output indicates that you are extremely focus on Exit Proximity, and you are mildly focus on People Count, and you are moderately focus on Crowd Density.
            """
        return dedent(prompt)

    
    def communicate(self, context):
        prompt = context + "\n\n"
        self.max_tokens = 512
        self.temperature = 0
        message = ""

        retries = 5
        backoff_factor = 2
        current_retry = 0

        openai.api_key = self.api_key

        while current_retry < retries:
            try:
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
                message = response['choices'][0]['message']['content'].strip().lower()
                is_valid, words = process_response(message)
                if not is_valid:
                    raise ValueError(message)
                #print(message)
                return words, message
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
                    wait_time = backoff_factor ** current_retry
                    print(f"{e}\nRetrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}. Retries exhausted.")
                    return None, message

