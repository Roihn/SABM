# from .chatgroup import ChatGroup

class Community:
    def __init__(self, name):
        self.name = name
        self.agent_list = []
        self.alias_community_list = []
        self.rival_community_list = []
        self.chatgroup = None
    
    def add_agent(self, agent):
        self.agent_list.append(agent)
        agent.add_community(self)
    
    def repr(self):
        return f"community {self.name}: {self.agent_list}"

    def add_alias_community(self, community):
        self.alias_community_list.append(community)
    
    def add_rival_community(self, community):
        self.rival_community_list.append(community)
    
    def get_alias_agents(self):
        alias_agents = set()
        for community in self.alias_community_list:
            alias_agents.union(set(community.agent_list))
        return list(alias_agents)

    def get_rival_agents(self):
        rival_agents = set()
        for community in self.rival_community_list:
            rival_agents.union(set(community.agent_list))
        return list(rival_agents)

    def set_chatgroup(self, chatgroup):
        if self.chatgroup is not None:
            raise Exception(f"chatgroup of community {self.name} has already been set")
        self.chatgroup = chatgroup
