from multi_agents import Agent
import numpy as np

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


class Human(Agent):
    def __init__(self, id: int, pos, width, height, attribute, seed=0):
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

        self.Z = 0
        # for state
        self.reset_cur_state()


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

