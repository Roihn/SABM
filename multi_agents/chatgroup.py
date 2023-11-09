import numpy as np

from multi_agents.community import Community


class ChatGroup:
    def __init__(self, name, type, community: Community = None, seed=0):
        self.name = name
        self.type = type
        self.seed = seed
        self.agent_list = []        
        self.chat_history = []        
        self.community = community
        self.rng = np.random.default_rng(seed=seed)
    
    def reset(self):
        self.chat_history = []

    def add_agent(self, agent):
        self.agent_list.append(agent)
        agent.add_chatgroup(self)

    def add_agents(self, agents):
        for agent in agents:
            self.add_agent(agent)

    def need_chat(self, **kwargs):
        raise NotImplementedError
    
    def chat(self):
        raise NotImplementedError


class CommunityChatGroup(ChatGroup):
    def __init__(self, name, community: Community):
        super().__init__(name, "community", community=community)
        community.set_chatgroup(self)
        self.add_agents(community.agent_list)

    def need_chat(self, **kwargs):
        return True

    def chat(self, round):
        chat_order = self.rng.permutation(len(self.agent_list))
        for id in chat_order:
            agent = self.agent_list[id]
            agent_rivals = agent.get_rivals(self.community)
            agent_aliases = agent.get_aliases(self.community)
            prompt = f"You are agent {agent.name}, and you are now chatting in chatgroup {self.name}.\n"
            prompt += f"Your rivals are {agent_rivals}.\n"
            prompt += f"Your aliases are {agent_aliases}.\n"
            prompt += f"Your chat history is {agent.get_context_history(chatgroup_name=self.name)}.\n"
            response = gpt4_chat(prompt) # TODO: implement gpt4_chat
            agent.record(round, self.name, prompt, response)

class PrivateChatGroup(ChatGroup):
    def __init__(self, name):
        super().__init__(name, "private")

    def add_agents(self, agent0, agent1):
        self.agent0 = agent0
        self.agent1 = agent1

    def need_chat(self, **kwargs):
        # TODO: add more conditions
        return False


class SpatialChatGroup(ChatGroup):
    def __init__(self, pos, seed=0):
        super().__init__(str(pos), "spatial", None, seed)
        self.pos = pos
