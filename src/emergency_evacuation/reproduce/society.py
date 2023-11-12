from multi_agents import Society
from .agent import *
import numpy as np
import math
from typing import List, Tuple
from matplotlib import pyplot as plt
from copy import deepcopy as dc
import logging
import pandas as pd
import os

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


class EscapeSociety(Society):
    def __init__(self, name, num_humans:int, agent_chat_range:int, width:int, height:int, exit_width:int=3, seed=0, need_obstacle=False, random_agent=True, is_panic=True) -> None:
        print(locals())
        super().__init__(name, seed)
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
        random_agent = random_agent if self.need_obstacle else True
        if random_agent:
            self.output_path = f"output/emergency_evacuation/reproduce/need_obstacle_{self.need_obstacle}/{self.num_humans}humans/is_panic_{self.is_panic}_seed{self.seed}"
        else:
            self.num_humans = 66 * 4
            self.output_path = f"output/emergency_evacuation/reproduce/need_obstacle_{self.need_obstacle}/fixed_agent/is_panic_{self.is_panic}_seed{self.seed}"
        os.makedirs(self.output_path, exist_ok=True)
        logging.basicConfig(filename=f"{self.output_path}/society.log", level=logging.INFO, filemode='w')
        logging.info(f"locals: {locals()}")
        

        self.gen_grid(self.need_obstacle)
        # self.grid_without_human = dc(self.grid)
        # self.next_grid = dc(self.grid_without_human) # next_grid should contain no humans
        self.add_human_reproduce(random_agent)
        self.cur_human_list = list(self.human_list)
        self.next_grid = list(self.grid)
        self.render()

        # Initialize the log
        df = pd.DataFrame(columns=['round', 'id', 'pos', 'status', 'overtaken_counts', 'congestion_degree', 'dist_to_nearest_exit', 'target_exit', 'velocity'])
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
    
    def agent_info_log(self):
        df = pd.DataFrame(columns=['id', 'init_pos', 'group_id', 'N0', 'Y0', 'Z0', 'alpha1', 'alpha2', 'alpha3', 'alpha4', 'alpha5', 'alpha6'])
        for agent in self.human_list:
            new_row = {
                'id': agent.id,
                'init_pos': agent.init_pos,
                'group_id': agent.group_id,
                'N0': agent.N0,
                'Y0': agent.Y0,
                'Z0': agent.Z0,
                'alpha1': agent.alpha1,
                'alpha2': agent.alpha2,
                'alpha3': agent.alpha3,
                'alpha4': agent.alpha4,
                'alpha5': agent.alpha5,
                'alpha6': agent.alpha6,
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
                'overtaken_counts': agent.Z, 
                'congestion_degree': agent.Y,
                'dist_to_nearest_exit': agent.dist_to_nearest_exit, 
                'target_exit': agent.target_exit, 
                'velocity': agent.velocity,
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
        group_prop = [0.3, 0.3, 0.2, 0.2]
        group_attributes = [GROUP1_ATTRIBUTES, GROUP2_ATTRIBUTES, GROUP3_ATTRIBUTES, GROUP4_ATTRIBUTES]
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
        for group_id, prob in enumerate(group_prop):
            group_num = int(self.num_humans * prob)
            for i, num in enumerate(group_attributes[group_id]["N0"]):
                x = group_attributes[group_id]
                x.update({"N0": i + 1})
                for _ in range(int(num * group_num)):
                    if not random_agent:
                        pos = pos_list.pop()
                    else:
                        pos = self.get_empty_grid()
                    new_human = Human(human_count, pos, self.width, self.height, x, self.seed)
                    self.grid[pos[0]][pos[1]] = new_human
                    self.human_list.append(new_human)
                    human_count += 1


    def chat(self):
        pass

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
        visual_range = calculateVisualRange(agent, target, agents, obstacles)
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
        for agent in self.cur_human_list:
            Y, beta0 = self.get_Y(agent)
            agent.Y, agent.beta0 = Y, beta0
            if Y > agent.Y0:
                agent.Z += 1
            if Y > agent.Y0 and agent.Z < agent.Z0:
                # Be overtaken
                logging.warning(f"agent {agent} be overtaken, Y={Y}, Y0={agent.Y0}, Z={agent.Z}, Z0={agent.Z0}")
                agent.status = "overtaken"
                continue
            elif Y > agent.Y0 and agent.Z == agent.Z0:
                # Dead
                self.grid[agent.cur_pos[0]][agent.cur_pos[1]] = None
                agent.status = "dead"
                agent.reset_cur_state()
                self.cur_human_list.remove(agent)
                self.num_dead += 1
                continue
            else:
                agent.status = "normal"

            # Decide the target exit
            target_exit = None
            min_ij = float('inf')
            if agent.group_id in [1, 3]:
                beta = beta0 * 1.2
            else:
                beta = beta0
            
            if self.is_panic:
                beta1 = 6 * beta
                beta2 = 1 / (6 * beta)
                beta3 = 1 / (4 * beta)
            else:
                beta1 = 1
                beta2 = 1
                beta3 = 1

            for exit in self.exit_list:
                # Calculate the distance to the exit
                dist = math.sqrt((exit.pos[0] - agent.cur_pos[0]) ** 2 + (exit.pos[1] - agent.cur_pos[1]) ** 2)
                agent.dist_to_nearest_exit = min(agent.dist_to_nearest_exit, dist)
                # Calculate the P_ij and Q_ij
                visible_grids = self.findVisibleGrids(agent, exit.pos, self.human_list, self.obstacle_list)
                if agent.cur_pos in visible_grids:
                    visible_grids.remove(agent.cur_pos)
                # self.render_visible(visible_grids, agent.id)

                P_ij = 0
                for (x, y) in visible_grids:
                    if self.grid[x][y] is not None:
                        P_ij += 1
                Q_ij = P_ij / len(visible_grids)
                k = 1

                ij = k * (math.pow(agent.alpha1, beta1) * dist + math.pow(agent.alpha2, beta2) * P_ij + math.pow(agent.alpha3, beta3) * Q_ij) / (agent.alpha1 + agent.alpha2 + agent.alpha3)
                if ij < min_ij:
                    min_ij = ij
                    target_exit = exit
            
            agent_target_dict[target_exit] = agent_target_dict.get(target_exit, []) + [agent]
            agent.target_exit = target_exit.pos


        for exit in agent_target_dict:
            agents = agent_target_dict[exit]
            target_exit = exit
            # sort the agent with the increasing order of the distance to the exit
            agents.sort(key=lambda agent: math.sqrt((agent.cur_pos[0] - exit.pos[0]) ** 2 + (agent.cur_pos[1] - exit.pos[1]) ** 2))
            for agent in agents:
                # print("agent", agent, "exit at", exit.pos)
                # Decide the action direction
                _, beta0 = self.get_Y(agent)
                if agent.group_id in [1, 3]:
                    beta = beta0 * 1.2
                else:
                    beta = beta0
                    
                if self.is_panic:
                    beta1 = 6 * beta
                    beta2 = 1 / (6 * beta)
                    beta3 = 1 / (4 * beta)
                else:
                    beta1 = 1
                    beta2 = 1
                    beta3 = 1
                opt_action = None
                suboptimal_action = None
                min_ij = float('inf')
                second_min_ij = float('inf')
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        x = agent.cur_pos[0] + i
                        y = agent.cur_pos[1] + j
                        if x < 0 or y < 0 or x >= self.height or y >= self.width:
                            continue
                        if self.next_grid[x][y] is not None:
                            continue
                        # Calculate the distance to the exit
                        dist = math.sqrt((target_exit.pos[0] - x) ** 2 + (target_exit.pos[1] - y) ** 2)
                        # Calculate the P_ij and Q_ij
                        visible_grids = self.findVisibleGrids(agent, target_exit.pos, self.human_list, self.obstacle_list)
                        P_ij = 0
                        for (x, y) in visible_grids:
                            if isinstance(self.grid[x][y], Human):
                                P_ij += 1
                        Q_ij = P_ij / len(visible_grids)
                        k = 1
                        J = (math.pow(agent.alpha4, beta1) * dist + math.pow(agent.alpha5, beta2) * P_ij + math.pow(agent.alpha6, beta3) * Q_ij) / (agent.alpha4 + agent.alpha5 + agent.alpha6)
                        if J < min_ij:
                            second_min_ij = min_ij
                            min_ij = J
                            suboptimal_action = opt_action
                            opt_action = (i, j)

                        elif J < second_min_ij:
                            second_min_ij = J
                            suboptimal_action = (i, j)
                
                # Choose the optimal action with probability 95% and the second optimal action with probability 5%
                if self.rng.random() < 0.95:
                    action = opt_action
                else:
                    action = suboptimal_action
                agent.velocity = 0
                if action is None:
                    logging.warning(f"agent {agent} cannot move")
                    continue
                # Update the next grid
                new_pos = (agent.cur_pos[0] + action[0], agent.cur_pos[1] + action[1])
                if self.next_grid[new_pos[0]][new_pos[1]] is not None:
                    continue
                if action[0] != 0 or action[1] != 0:
                    # As long as the agent moves, it will be considered as moving with velocity 1
                    agent.velocity = 1
                    
                self.next_grid[agent.cur_pos[0]][agent.cur_pos[1]] = None
                agent.cur_pos = new_pos
                self.next_grid[agent.cur_pos[0]][agent.cur_pos[1]] = agent
                agent.pos_history.append(agent.cur_pos)
            
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
        colors = ['r', 'g', 'b', 'y']
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
                    plt.scatter(j+0.5, i+0.5, c=colors[grid[i][j].group_id % len(colors)])
        
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

        colors = ['r', 'g', 'b', 'y']
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
