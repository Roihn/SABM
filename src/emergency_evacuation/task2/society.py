from multi_agents import Society
from .agent import *
import numpy as np
import random
import math
from typing import List, Tuple
from matplotlib import pyplot as plt
from copy import deepcopy as dc
import logging
import pandas as pd
import os

# ACTIONS = {
#     3: (-1, 0),
#     1: (1, 0),
#     2: (0, -1),
#     0: (0, 1),
#     4: (0, 0),
#     7: (-1, -1),
#     8: (-1, 1),
#     6: (1, -1),
#     5: (1, 1),
# }

ACTIONS = {    
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
    4: (0, 0),    
    5: (1, 1),
    6: (1, -1),
    7: (-1, -1),
    8: (-1, 1),
}

class Obstacle:
    def __init__(self, x, y):
        self.name = "obstacle"
        self.can_pass = False
        self.pos = (x, y)

class Wall(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "wall"
        self.can_pass = False

class Exit:
    def __init__(self, x, y):
        self.name = "exit"
        self.label = ""
        self.can_pass = True
        self.pos = (x, y)
        self.escaped_agent_list = []
        # self.targeted_agent_list = []
    
    def escaped_agent(self, agent):
        self.escaped_agent_list.append(agent.id)
    
    def get_escaped_num(self):
        return len(self.escaped_agent_list)
    
    # def targeted_agents(self, agent):
    #     self.targeted_agent_list.append(agent)

def bresenham(start: Tuple[int, int], end: Tuple[int, int], obstacles: List[Obstacle]) -> List[Tuple[int, int]]:
    """Bresenham's Line Algorithm to find all points on the line between two points."""
    x1, y1 = start
    x2, y2 = end
    points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1

    if dx > dy:
        err = dx / 2.0
        while x != x2:
            points.append((x, y))
            if (x, y) in [obstacle.pos for obstacle in obstacles]:
                return points
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            points.append((x, y))
            if (x, y) in [obstacle.pos for obstacle in obstacles]:
                return points
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    points.append((x, y))

    return points

def calculateVisualRange(agent: Human, target: Tuple[int, int], agents: List[Human], obstacles: List[Obstacle]) -> int:
    line = bresenham(agent.cur_pos, target, obstacles)
    line_agents = [point for point in line if point in [other.cur_pos for other in agents]]
    line_agents.sort(key=lambda point: math.sqrt((point[0] - agent.cur_pos[0]) ** 2 + (point[1] - agent.cur_pos[1]) ** 2))
    if len(line_agents) >= 5:
        visual_range = math.sqrt((line_agents[4][0] - agent.cur_pos[0]) ** 2 + (line_agents[4][1] - agent.cur_pos[1]) ** 2)
    else:
        visual_range = math.sqrt((line[-1][0] - agent.cur_pos[0]) ** 2 + (line[-1][1] - agent.cur_pos[1]) ** 2)

    if line[-1] in [obstacle.pos for obstacle in obstacles]:
        obstacle_dist = math.sqrt((line[-1][0] - agent.cur_pos[0]) ** 2 + (line[-1][1] - agent.cur_pos[1]) ** 2)
        visual_range = min(visual_range, obstacle_dist)

    return visual_range

def circle_points(radius, n=100):
    return [(math.cos(2 * math.pi / n * x) * radius, math.sin(2 * math.pi / n * x) * radius) for x in range(0, n+1)]

def distance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

def n_closest_messages(agent, messages, threshold_dist=5):
    # Calculate distances
    distances = [(agent_id, message, distance(agent.cur_pos, position)) for agent_id, position, message in messages]
    # for m in messages:
    #     print(f"agent {m[0]} pos {m[1]} message {m[2]} distance {distance(agent.cur_pos, m[1])} to agent {agent.id} pos {agent.cur_pos}")
    # Sort by distance
    sorted_messages = sorted(distances, key=lambda x: x[2])
    res = [(m[0], m[1]) for m in sorted_messages if m[2] <= threshold_dist and m[0] != agent.id]
    # print(res)
    return res


class EscapeSociety(Society):
    def __init__(self, name, num_humans:int, agent_chat_range:int, width:int, height:int, exit_width:int=3, seed=0, need_obstacle=False, random_agent=True, is_panic=True, update_rounds=5, model="gpt-4-0314", api_key=None) -> None:
        print(locals())
        super().__init__(name, seed)
        random.seed(seed)
        self.agent_chat_range = agent_chat_range
        self.width = width
        self.height = height
        self.exit_width = exit_width
        self.need_obstacle = need_obstacle
        self.exit_list = []
        self.num_humans = num_humans
        self.human_list = []
        self.obstacle_list = []
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.is_panic = is_panic
        self.model = model
        self.api_key = api_key
        random_agent = random_agent if self.need_obstacle else True
        if random_agent:
            self.output_path = f"output/emergency_evacuation/task2/need_obstacle_{self.need_obstacle}/{self.num_humans}humans/is_panic_{self.is_panic}_seed{self.seed}"
        else:
            self.num_humans = 66 * 4
            self.output_path = f"output/emergency_evacuation/task2/need_obstacle_{self.need_obstacle}/fixed_agent/is_panic_{self.is_panic}_seed{self.seed}"
        os.makedirs(self.output_path, exist_ok=True)
        logging.basicConfig(filename=f"{self.output_path}/society.log", level=logging.INFO, filemode='w')
        logging.info(f"locals: {locals()}")
        self.logging = logging
        
        self.gen_grid(self.need_obstacle)
        # self.grid_without_human = dc(self.grid)
        # self.next_grid = dc(self.grid_without_human) # next_grid should contain no humans
        self.add_human_reproduce(random_agent)
        self.cur_human_list = list(self.human_list)
        self.next_grid = list(self.grid)
        self.render()

        # Initialize the log
        df = pd.DataFrame(columns=['round', 'id', 'pos', 'status', 'response1', 'response2', 'response3', 'response4', 'target_exit', 'velocity', 'action'])
        df.to_csv(f"{self.output_path}/agent_log.csv", index=False)
        df = pd.DataFrame(columns=['round', 'pos', 'escaped_num', 'escaped_agents'])
        df.to_csv(f"{self.output_path}/exit_log.csv", index=False)

        # Log the first round
        self.agent_log()
        self.agent_info_log()
        self.exit_log()

        self.num_dead = 0
        self.num_escaped = 0
        self.dead_list = []
        self.escaped_list = []
        self.update_rounds = update_rounds
        self.generate_env_prompt()
    
    def agent_info_log(self):
        df = pd.DataFrame(columns=['id', 'init_pos', 'group_id', 'N0', 'Y0', 'Z0', 'alpha1', 'alpha2', 'alpha3', 'alpha4', 'alpha5', 'alpha6'])
        for agent in self.human_list:
            new_row = {
                'id': agent.id,
                'init_pos': agent.init_pos,
                'capability': agent.capability_text,
                'mental': agent.mental_text,
                # 'group_id': agent.group_id,
                'N0': agent.N0,
                'Y0': agent.Y0,
                'Z0': agent.Z0,
                # 'alpha1': agent.alpha1,
                # 'alpha2': agent.alpha2,
                # 'alpha3': agent.alpha3,
                # 'alpha4': agent.alpha4,
                # 'alpha5': agent.alpha5,
                # 'alpha6': agent.alpha6,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(f"{self.output_path}/agent_info.csv", index=False)

    def agent_log(self):
        df = pd.read_csv(f"{self.output_path}/agent_log.csv")
        new_rows = []
        for agent in self.human_list:
            new_rows.append({
                'round': self.round, 
                'id': agent.id, 
                'pos': agent.cur_pos,
                'status': agent.status,
                'capability': agent.capability_text,
                'mental': agent.mental_text,
                'response1': agent.response1,
                'response2': agent.response2,
                'response3': agent.response3,
                'response4': agent.response4,
                'target_exit': agent.target_exit.pos if agent.target_exit is not None else None, 
                'velocity': agent.velocity,
                'action': agent.action if agent.action is not None else None,
            })
            agent.reset_cur_state()
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
        df.to_csv(f"{self.output_path}/agent_log.csv", index=False)

    def exit_log(self):
        df = pd.read_csv(f"{self.output_path}/exit_log.csv")
        new_rows = []
        for exit in self.exit_list:
            new_rows.append({
                'round': self.round, 
                'pos': exit.pos, 
                'escaped_num': exit.get_escaped_num(),
                'escaped_agents': exit.escaped_agent_list,
            })
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
        df.to_csv(f"{self.output_path}/exit_log.csv", index=False)

    def generate_env_prompt(self):
        prompt = f"""\
        
            Because of earthquake, you need to escape from the room where you are as fast as possible. 
            The room has a size of 33 * 33. There are 3 exits in the room. The exits are located at the left, bottom and right of the room.
            To escape from the room, you need to consider the following two aspects: exit proximity and people count. 
            The exit proximity is the distance between you and the nearest exit. The people count is the number of people you can see.
        """
 
        # if self.is_panic:
        #     prompt += " You are in a panic state.\n"
        # else:
        #     prompt += " You are not in a panic state.\n"

        self.env_prompt = dedent(prompt)

        short_prompt = f"""\
            You need to escape to the exit as fast as possible. The room has a size of 33 * 33. 
            We use (x, y) to denote the position, smaller x means top and bigger x means buttom; smaller y means left and bigger y means right. 
            Position (1, 1) is at the top left of the room. It is possible to move diagonally, e.g. from (1, 1) to (2, 2) is one move to the lower right, and is faster than (1, 1)->(1, 2)->(2, 2).
        """
        self.env_short_prompt = dedent(short_prompt)

    def gen_grid(self, need_obstacle=False):
        # Generate the Walls
        for i in range(self.width):
            self.grid[0][i] = Wall(0, i)
            self.grid[self.height - 1][i] = Wall(self.height - 1, i)
        for i in range(self.height):
            self.grid[i][0] = Wall(i, 0)
            self.grid[i][self.width - 1] = Wall(i, self.width - 1)

        # Generate the Exit
        for i in range(self.exit_width):
            self.grid[self.height - 1][int((self.width - self.exit_width) / 2) + i] = None
            self.grid[int((self.height - self.exit_width) / 2) + i][0] = None
            self.exit_list.append(Exit(self.height - 1, int((self.width - self.exit_width) / 2) + i))
            self.exit_list.append(Exit(int((self.height - self.exit_width) / 2) + i, 0))
            
            if i == 2:
                self.grid[int((self.height - self.exit_width) / 2) + i][self.width - 1] = None
                self.exit_list.append(Exit(int((self.height - self.exit_width) / 2) + i, self.width - 1))

        # Generate the Obstacles
        # TODO: Generate the Obstacles
        if need_obstacle:
            row = [2, 4, 6, 8, 10, 12, 19, 21, 23, 25, 27, 29]
            col = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
            for i in row:
                for j in col:
                    self.grid[i][j] = Obstacle(i, j)
                    self.obstacle_list.append(Obstacle(i, j))
            # for _ in range(80):
            #     x = self.rng.integers(self.width)
            #     y = self.rng.integers(self.height)
            #     if self.grid[x][y] is None and (x,y) not in [exit.pos for exit in self.exit_list]:
            #         self.grid[x][y] = Obstacle(x, y)
            #         self.obstacle_list.append(Obstacle(x, y))
        return

    def get_neighbor_chatgroups(self, agent_pos):
        x, y = agent_pos
        neighbor_chatgroups = []
        for i in range(x - self.agent_chat_range, x + self.agent_chat_range + 1):
            for j in range(y - self.agent_chat_range, y + self.agent_chat_range + 1):
                if i >= 0 and i < self.width and j >= 0 and j < self.height:
                    if abs(x - i) + abs(y - j) <= self.agent_chat_range:
                        neighbor_chatgroups.append(self.grid[i][j])
        return neighbor_chatgroups
    
    def get_empty_grid(self):
        while True:
            x = self.rng.integers(self.width)
            y = self.rng.integers(self.height)
            if self.grid[x][y] is None and (x,y) not in [exit.pos for exit in self.exit_list]:
                return (x, y)

    def add_human_reproduce(self, random_agent=True):
        if not random_agent:
            # self.num_humans = 66 * 4
            row = [2, 4, 6, 8, 10, 12, 19, 21, 23, 25, 27, 29]
            col = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
            pos_list = []
            for i in row:
                for j in col:
                    pos_list.append((i+1, j))
            self.rng.shuffle(pos_list)
        human_count = 0
        for human_count in range(self.num_humans):
            # Internally have different capabilities, which are not known to the agent, and only affects the meta info of the agent
            capability = human_count % 4 // 2
            mental = human_count % 2
            x = {"capability": capability, "mental": mental}
            if not random_agent:
                pos = pos_list.pop()
            else:
                pos = self.get_empty_grid()
            new_human = Human(human_count, pos, self.width, self.height, x, self.seed, model=self.model, api_key=self.api_key)
            self.grid[pos[0]][pos[1]] = new_human
            self.human_list.append(new_human)
            # if human_count >= 5:
            #     return

    def get_Y(self, agent):
        x, y = agent.cur_pos
        N0 = agent.N0
        # Get Y0 of the surrounding agents
        Y = 0
        N = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x + i >= self.height or x + i < 0 or y + j >= self.width or y + j < 0:
                    continue
                if self.grid[x + i][y + j] is not None:
                    if isinstance(self.grid[x + i][y + j], Human):
                        Y += (self.grid[x + i][y + j].N0 - N0)
                        N += 1
        return Y, 1 + N / 10

    def findVisibleGrids(self, agent: Human, target: Tuple[int, int], agents: List[Human], obstacles: List[Obstacle]) -> List[Tuple[int, int]]:
        # visual_range = calculateVisualRange(agent, target, agents, obstacles)
        visual_range = 10
        boundary_points = circle_points(visual_range)

        visible_grids = []
        for dx, dy in boundary_points:
            dx_target = target[0] - agent.cur_pos[0]
            dy_target = target[1] - agent.cur_pos[1]
            dot_product = dx * dx_target + dy * dy_target
            mag_product = math.sqrt(dx ** 2 + dy ** 2) * math.sqrt(dx_target ** 2 + dy_target ** 2)
            if mag_product != 0 and math.degrees(math.acos(dot_product / mag_product)) <= 45:
                x, y = agent.cur_pos[0] + int(round(dx)), agent.cur_pos[1] + int(round(dy))
                line = bresenham(agent.cur_pos, (x, y), obstacles)
                for (x,y) in line:
                    if x < 0 or y < 0 or x >= self.height or y >= self.width:
                        continue
                    if (x, y) not in visible_grids:
                        visible_grids.append((x, y))

        return visible_grids

    def set_agent_status(self, agent):
        Y, beta0 = self.get_Y(agent)
        agent.Y, agent.beta0 = Y, beta0
        if Y > agent.Y0:
            agent.Z += 1
        if Y > agent.Y0 and agent.Z < agent.Z0:
            # Be overtaken
            logging.warning(f"agent {agent} be overtaken, Y={Y}, Y0={agent.Y0}, Z={agent.Z}, Z0={agent.Z0}")
            agent.status = "overtaken"
            return False, Y, beta0
        elif Y > agent.Y0 and agent.Z == agent.Z0:
            # Dead
            self.grid[agent.cur_pos[0]][agent.cur_pos[1]] = None
            agent.status = "dead"
            agent.reset_cur_state()
            self.cur_human_list.remove(agent)
            self.num_dead += 1
            return False, Y, beta0
        else:
            agent.status = "normal"
            return True, Y, beta0

    def step(self):
        agent_target_dict = {}
        self.next_grid = list(self.grid)
        # First check whether there are agents that can exit
        for exit in self.exit_list:
            if isinstance(self.grid[exit.pos[0]][exit.pos[1]], Human):
                agent = self.grid[exit.pos[0]][exit.pos[1]]
                # print("escaped agent", agent, "exit at", exit.pos, len(self.cur_human_list), len(self.human_list))
                self.grid[exit.pos[0]][exit.pos[1]] = None
                agent.status = "escaped"
                self.cur_human_list.remove(agent)
                agent.reset_cur_state()
                self.num_escaped += 1
                exit.escaped_agent(agent)

        # Get the target exit of each agent
        self.rng.shuffle(self.cur_human_list)
        # First update self.num_humans / self.update_rounds humans
        if self.round == 0:
            gpt_human_list = list(self.cur_human_list)
        else:
            # prob = 1 / self.update_rounds
            prob = 0.2
            gpt_human_list = []
            for agent in self.cur_human_list:
                if self.rng.random() < prob:
                    gpt_human_list.append(agent)
        # if self.round % 5 == 0:
        #     gpt_human_list = list(self.cur_human_list)
        # else:
        #     gpt_human_list = []

        for agent in gpt_human_list:
            is_normal, Y, beta0 = self.set_agent_status(agent)
            if not is_normal:
                # agent is overtaken or dead
                continue
            # Decide the target exit
            target_exit = None

            num_agents_around = int(beta0 * 10) - 10
            from collections import defaultdict
            exit_data = defaultdict(lambda: defaultdict(list))
            dist_to_nearest_exit = float('inf')
            for exit in self.exit_list:
                # Calculate the distance to the exit
                dist = math.sqrt((exit.pos[0] - agent.cur_pos[0]) ** 2 + (exit.pos[1] - agent.cur_pos[1]) ** 2)
                dist_to_nearest_exit = min(dist_to_nearest_exit, dist)
                visible_grids = self.findVisibleGrids(agent, exit.pos, self.human_list, self.obstacle_list)
                P_ij = 0
                for (x, y) in visible_grids:
                    if self.grid[x][y] is not None:
                        if self.grid[x][y].name != "wall":
                            P_ij += 1
                Q_ij = P_ij / len(visible_grids)
                if agent.cur_pos in visible_grids:
                    visible_grids.remove(agent.cur_pos)
                if exit.pos[1] == 0:
                    exit_data["left"]["dist"].append(dist)
                    exit_data["left"]["num_agents_around"].append(P_ij)
                    exit_data["left"]["crowdness"].append(Q_ij)
                elif exit.pos[0] == 32:
                    exit_data["bottom"]["dist"].append(dist)
                    exit_data["bottom"]["num_agents_around"].append(P_ij)
                    exit_data["bottom"]["crowdness"].append(Q_ij)
                else:
                    exit_data["right"]["dist"].append(dist)
                    exit_data["right"]["num_agents_around"].append(P_ij)
                    exit_data["right"]["crowdness"].append(Q_ij)

            for _, exit in exit_data.items():
                exit["dist"] = np.mean(exit["dist"])
                exit["num_agents_around"] = np.mean(exit["num_agents_around"])
                exit["crowdness"] = np.mean(exit["crowdness"])

            state_history_prompt = ""
            prompt_stage1 = agent.form_current_state_stage1(num_agents_around, dist_to_nearest_exit)
            prompt1 = f"{self.env_prompt}\n {prompt_stage1}"

            flag, panic_index_str = agent.communicate(prompt1)
            logging.info(f"round {self.round} agent {agent.id} prompt 1: {prompt1}")
            logging.info(f"response: {panic_index_str}")
            agent.response1 = panic_index_str
            if flag is None:
                if agent.target_exit is None:
                    raise Exception(f"Agent is not well initializied, response={panic_index_str}")
            else:
                prompt_stage2 = agent.form_current_state_stage2(panic_index_str, exit_data)
            prompt2 = f"{self.env_prompt}\n {prompt_stage2}"
            _, resp2 = agent.communicate(prompt2)
            logging.info(f"round {self.round} agent {agent.id} prompt 2: {prompt2}")
            logging.info(f"response: {resp2}")
            agent.response2 = resp2
            # print(communicate_list)

            prompt_stage3 = agent.form_current_state_stage3(panic_index_str, resp2)
            prompt3 = f"{self.env_prompt}\n {prompt_stage3}"
            logging.info(f"round {self.round} agent {agent.id} prompt 3: {prompt3}")
            _, resp = agent.communicate(prompt3)
            logging.info(f"response: {resp}")
            agent.response3 = resp
            if resp not in ['left', 'bottom', 'right']:
                raise Exception(f"Invalid exit, resp={resp}")

            target_exit = None
            dist_to_nearest_exit = float('inf')
            for exit in self.exit_list:
                if exit.pos[1] == 0 and resp == 'left':
                    dist = math.sqrt((exit.pos[0] - agent.cur_pos[0]) ** 2 + (exit.pos[1] - agent.cur_pos[1]) ** 2)
                    if dist < dist_to_nearest_exit:
                        dist_to_nearest_exit = dist
                        target_exit = exit
                elif exit.pos[0] == 32 and resp == 'bottom':
                    dist = math.sqrt((exit.pos[0] - agent.cur_pos[0]) ** 2 + (exit.pos[1] - agent.cur_pos[1]) ** 2)
                    if dist < dist_to_nearest_exit:
                        dist_to_nearest_exit = dist
                        target_exit = exit
                elif exit.pos[1] == 32 and resp == 'right':
                    dist = math.sqrt((exit.pos[0] - agent.cur_pos[0]) ** 2 + (exit.pos[1] - agent.cur_pos[1]) ** 2)
                    if dist < dist_to_nearest_exit:
                        dist_to_nearest_exit = dist
                        target_exit = exit

            # print("######## Agent", agent.id, "########\n", target_exit.pos)
            agent_state = {
                'round': self.round,
                'prompt1': prompt1,
                'response1': panic_index_str,
                'prompt2': prompt2,
                'response2': resp2,
                'prompt3': prompt3,
                'response3': resp,
                'target_exit': target_exit.pos,
            }
            if agent.target_exit is not None and agent.target_exit != target_exit:
                # The target exit has changed
                logging.info(f"The target exit has changed, agent {agent.id} at {agent.cur_pos} changes its exit from {agent.target_exit.pos} to {target_exit.pos}")
            agent.target_exit = target_exit
            agent.update_state_history(agent_state)
            agent.target_exit_history.append(resp)

        for agent in self.cur_human_list:
            target_exit = agent.target_exit
            agent_target_dict[target_exit] = agent_target_dict.get(target_exit, []) + [agent]

        for exit in agent_target_dict:
            agents = agent_target_dict[exit]
            target_exit = exit
            # sort the agent with the increasing order of the distance to the exit
            agents.sort(key=lambda agent: math.sqrt((agent.cur_pos[0] - exit.pos[0]) ** 2 + (agent.cur_pos[1] - exit.pos[1]) ** 2))
            for agent in agents:
                # Get the information of grids around the agent
                occupied_grids = []
                agent_attribute_prompt = agent.get_attribute_prompt()
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        x = agent.cur_pos[0] + i
                        y = agent.cur_pos[1] + j
                        if i == 0 and j == 0:
                            continue
                        if x < 0 or y < 0 or x >= self.height or y >= self.width or self.next_grid[x][y] is not None:
                            occupied_grids.append((i, j))
                
                occupied_action = []
                for og in occupied_grids:
                    occupied_action.append([k for k,v in ACTIONS.items() if v == og][0])
                
                action_list = ""
                action_dict = {}
                action_alphabet_list = "abcdefghi"

                alphabet_count = 0
                for code, action in ACTIONS.items():
                    if code in occupied_action: pass
                    else:
                        action_list += f"{action_alphabet_list[alphabet_count]} - {action[0] + agent.cur_pos[0], action[1] + agent.cur_pos[1]}, "
                        action_dict[action_alphabet_list[alphabet_count]] = (action[0] + agent.cur_pos[0], action[1] + agent.cur_pos[1])
                        alphabet_count += 1

                prompt_action_stage4 = agent.form_action(target_exit, agent.cur_pos, action_list, alphabet_count)
                prompt_action = f"{self.env_short_prompt}\n {prompt_action_stage4}"
                logging.info(f"round {self.round} agent {agent.id} prompt 4: {prompt_action}")
                def reject_func(resp):
                    if resp[-1] == '.':
                        resp = resp[:-1]
                    if resp[-1] in action_alphabet_list:
                        return False
                    if 'a' <= resp[0] <= 'i' and resp[2] == '-':
                        return False
                    return True

                _, resp = agent.communicate(prompt_action, reject_func)
                if resp[-1] == '.':
                    resp = resp[:-1]
                agent.response4 = resp
                action = action_dict[resp]
                agent.velocity = 0
                if action is None:
                    logging.warning(f"agent {agent} cannot move")
                    continue
                # Update the next grid
                # new_pos = (agent.cur_pos[0] + action[0], agent.cur_pos[1] + action[1])
                new_pos = action
                # print(new_pos, agent.cur_pos, action)
                if self.next_grid[new_pos[0]][new_pos[1]] is not None:
                    continue
                if action[0] != 0 or action[1] != 0:
                    # As long as the agent moves, it will be considered as moving with velocity 1
                    agent.velocity = 1

                self.next_grid[agent.cur_pos[0]][agent.cur_pos[1]] = None
                agent.cur_pos = new_pos
                self.next_grid[agent.cur_pos[0]][agent.cur_pos[1]] = agent
                agent.pos_history.append(agent.cur_pos)
                agent.action = action
                if agent.state_history[-1]['round'] == self.round:
                    agent.state_history[-1]['prompt4'] = prompt_action
                    agent.state_history[-1]['response4'] = resp
                    agent.state_history[-1]['action'] = action
                    agent.state_history[-1]['velocity'] = agent.velocity
                else:
                    state = {
                        'round': self.round,
                        'prompt1': None,
                        'response1': None,
                        'prompt2': None,
                        'response2': None,
                        'prompt3': None,
                        'response3': None,
                        'prompt4': prompt_action,
                        'response4': resp,
                        'target_exit': target_exit.pos,
                        'action': action,
                        'velocity': agent.velocity,
                    }
                    agent.update_state_history(state)
                    

        # Update the grid
        self.grid = list(self.next_grid)

        self.round += 1
        # Log the agent and exit
        self.agent_log()
        self.exit_log()
        logging.info(f"#### After Round {self.round - 1} ####  num_escaped {self.num_escaped} num_dead {self.num_dead}")
        self.escaped_list.append(self.num_escaped)
        self.dead_list.append(self.num_dead)
        return self.grid

    def render(self, agent_list=None):
        grid = dc(self.grid)
        # print(grid)
        fig, ax = plt.subplots(figsize=(6,6))

        # Set the x and y range
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        # Draw the grid
        ax.set_xticks(np.arange(0, self.width+1, 1))
        ax.set_yticks(np.arange(0, self.height+1, 1))
        ax.grid(color='black')

        # Set the tick labels to be at each half integer mark
        ax.set_xticks(np.arange(0.5, self.width, 1), minor=True)
        ax.set_yticks(np.arange(0.5, self.height, 1), minor=True)
        ax.set_xticklabels(np.arange(0, self.width, 1), minor=True, fontsize=8)
        ax.set_yticklabels(np.arange(0, self.height, 1), minor=True, fontsize=8)

        # Hide major tick labels
        ax.tick_params(which='major', labelbottom=False, labelleft=False)

        # Only show grid for major ticks
        # ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        # Draw grid
        # plt.grid(True, color='k')
        ax.invert_yaxis()

        for exit in self.exit_list:
            plt.fill([exit.pos[1], exit.pos[1]+1, exit.pos[1]+1, exit.pos[1]], [exit.pos[0], exit.pos[0], exit.pos[0]+1, exit.pos[0]+1], 'pink')
        colors = ['r', 'y', 'g', 'b']
        # Draw empty cells
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] is None and (i,j) not in [exit.pos for exit in self.exit_list]:
                    plt.fill([j, j+1, j+1, j], [i, i, i+1, i+1], 'white')
                elif isinstance(grid[i][j], Wall):
                    if (i,j) not in [exit.pos for exit in self.exit_list]:
                        plt.fill([j, j+1, j+1, j], [i, i, i+1, i+1], 'gray')
                elif isinstance(grid[i][j], Obstacle):
                    plt.fill([j, j+1, j+1, j], [i, i, i+1, i+1], 'slateblue')
                elif isinstance(grid[i][j], Human):
                    # plt.scatter(j+0.5, i+0.5, c=colors[grid[i][j].capability % len(colors)])
                    plt.scatter(j+0.5, i+0.5, c='b')

        if agent_list:
            for agent in agent_list:
                if agent.status == "escaped" or agent.status == "dead":
                    continue
                x = [x+0.5 for (x,y) in agent.pos_history]
                y = [y+0.5 for (x,y) in agent.pos_history]
                # print(agent.pos_history)
                plt.plot(y, x)


        plt.savefig(f"{self.output_path}/escape_society_{str(self.round).zfill(4)}.png")
        plt.clf()
        plt.close()

    def render_visible(self, visible_grid, name):
        grid = dc(self.grid)
        fig, ax = plt.subplots(figsize=(6,6))

        # Set the x and y range
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        # Draw the grid
        ax.set_xticks(np.arange(0, self.width+1, 1))
        ax.set_yticks(np.arange(0, self.height+1, 1))
        ax.grid(color='black')

        # Set the tick labels to be at each half integer mark
        ax.set_xticks(np.arange(0.5, self.width, 1), minor=True)
        ax.set_yticks(np.arange(0.5, self.height, 1), minor=True)
        ax.set_xticklabels(np.arange(0, self.width, 1), minor=True, fontsize=8)
        ax.set_yticklabels(np.arange(0, self.height, 1), minor=True, fontsize=8)

        # Hide major tick labels
        ax.tick_params(which='major', labelbottom=False, labelleft=False)

        # Only show grid for major ticks
        # ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        # Draw grid
        # plt.grid(True, color='k')
        ax.invert_yaxis()

        for exit in self.exit_list:
            plt.fill([exit.pos[1], exit.pos[1]+1, exit.pos[1]+1, exit.pos[1]], [exit.pos[0], exit.pos[0], exit.pos[0]+1, exit.pos[0]+1], 'pink')

        for visible in visible_grid:
            plt.fill([visible[1], visible[1]+1, visible[1]+1, visible[1]], [visible[0], visible[0], visible[0]+1, visible[0]+1], 'yellow')

        colors = ['r', 'y', 'g']
        # Draw empty cells
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] is None:
                    continue
                    plt.fill([j, j+1, j+1, j], [i, i, i+1, i+1], 'white')
                elif isinstance(grid[i][j], Wall):
                    if (i,j) not in [exit.pos for exit in self.exit_list]:
                        plt.fill([j, j+1, j+1, j], [i, i, i+1, i+1], 'gray')
                elif isinstance(grid[i][j], Obstacle):
                    plt.fill([j, j+1, j+1, j], [i, i, i+1, i+1], 'paleblue')
                elif isinstance(grid[i][j], Human):
                    plt.scatter(j+0.5, i+0.5, c=colors[grid[i][j].group_id % len(colors)])

        plt.savefig(f"output/escape_visible/render_visible_{name}.png")
        plt.close()
