from .agent import Agent
from .chatgroup import ChatGroup, CommunityChatGroup, PrivateChatGroup
from .community import Community
import numpy as np

NAME_LIST = [
    "Olivia", "Emma", "Ava", "Sophia", "Isabella",
    "Charlotte", "Amelia", "Mia", "Harper", "Evelyn",
    "Liam", "Noah", "William", "James", "Oliver",
    "Benjamin", "Elijah", "Lucas", "Mason", "Logan",
    "Alexander", "Ethan", "Jacob", "Michael", "Henry",
    "Daniel", "Matthew", "Aiden", "Lucas", "Samuel",
    "Grace", "Lily", "Avery", "Nora", "Zoe",
    "Mila", "Aubrey", "Hannah", "Stella", "Victoria",
    "Jackson", "Sebastian", "Jack", "Owen", "Theodore",
    "Jayden", "Carter", "Julian", "Luke", "Grayson",
    "Ella", "Scarlett", "Sofia", "Chloe", "Aria",
    "Camila", "Penelope", "Riley", "Layla", "Lillian",
    "Wyatt", "Isaac", "Caleb", "Josiah", "Levi",
    "Mateo", "David", "John", "Ryan", "Isaiah",
    "Emily", "Elizabeth", "Sofia", "Avery", "Ella",
    "Scarlett", "Grace", "Chloe", "Layla", "Madison",
    "Evan", "Miles", "Dominic", "Xavier", "Jaxon",
    "Christopher", "Andrew", "Asher", "Joshua", "Nathan",
    "Savannah", "Aubrey", "Brooklyn", "Zoe", "Natalie",
    "Paisley", "Everly", "Bella", "Willow", "Hazel"
]

def find_by_name(name: str, obj_list: list):
    for obj in obj_list:
        if obj.name == name:
            return obj
    return None

class Society:
    """A base class that stores all the agents and chatgroups in the society."""
    def __init__(self, name, seed=0) -> None:
        self.name = name
        self.seed = seed
        self.agents = []
        self.chatgroups = []
        self.communities = []
        self.agent_count = 0
        self.chatgroup_count = 0
        self.community_count = 0
        self.round = 0
        self.agents_name_set = set()
        self.rng = np.random.default_rng(seed=seed)

    def reset(self):
        self.round = 0
        for agent in self.agents:
            agent.reset()
        for chatgroup in self.chatgroups:
            chatgroup.reset()

    def add_community(self, community_name: str=None) -> Community:
        """Add a community to the society."""
        if community_name is None:
            community_name = f"community_{self.chatgroup_count}"
        community = Community(community_name)
        self.communities.append(community)
        self.community_count += 1
        return community

    def add_agent(self, agent_name: str=None, community_name=None) -> Agent:
        """Add an agent to the society."""
        if agent_name is None:
            agent_name = self.rng.choice(NAME_LIST)
            while agent_name in self.agents_name_set:
                agent_name = self.rng.choice(NAME_LIST)
        else:
            if agent_name in self.agents_name_set:
                raise ValueError("Agent name already exists.")
        self.agents_name_set.add(agent_name)
        agent = Agent(agent_name)
        self.agents.append(agent)
        self.agent_count += 1

        if community_name is not None:
            if isinstance(community_name, Community):
                community = community_name
            elif isinstance(community_name, str):
                community = find_by_name(community_name, self.communities)
            elif isinstance(community_name, int):
                assert community_name < self.community_count, f"Community index {community_name} out of range."
                community = self.communities[community_name]
            if community is None:
                raise ValueError(f"Community {community_name} does not exist.")
            community.add_agent(agent)
            if community.chatgroup:
                community.chatgroup.add_agent(agent)

        return agent
    
    def add_chatgroup(self, chatgroup_name: str, type: str, community_name=None) -> ChatGroup:
        """Add a chatgroup to the society."""
        if find_by_name(chatgroup_name, self.chatgroups):
            raise ValueError(f"Chatgroup {chatgroup_name} already exists.")
        community = None
        if community_name is not None:
            if isinstance(community_name, Community):
                community = community_name
            elif isinstance(community_name, str):
                community = find_by_name(community_name, self.communities)
            elif isinstance(community_name, int):
                assert community_name < self.community_count, f"Community index {community_name} out of range."
                community = self.communities[community_name]
            if community is None:
                raise ValueError(f"Community {community_name} does not exist.")
        if type == "community":
            if community is None:
                raise ValueError("Community name must be specified for community chatgroup.")
            chatgroup = CommunityChatGroup(chatgroup_name, community)
        elif type == "private":
            chatgroup = PrivateChatGroup(chatgroup_name)
        else:
            raise ValueError(f"Chatgroup type {type} is not supported.")
        self.chatgroups.append(chatgroup)

    def chat(self):
        """Each chatgroup starts chatting."""
        for chatgroup in self.chatgroups:
            if chatgroup.need_chat():
                chatgroup.chat(self.round)
        
        self.round += 1
