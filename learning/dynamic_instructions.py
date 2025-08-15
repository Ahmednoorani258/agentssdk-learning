import datetime
from agents import RunContextWrapper, Agent

def basic_dynamic(context: RunContextWrapper, agent: Agent) -> str:
    return f"You are {agent.name}. Be helpful and friendly."

agent = Agent(
    name="Dynamic Agent",
    instructions=basic_dynamic
)
def context_aware(context: RunContextWrapper, agent: Agent) -> str:
    # Check how many messages in the conversation
    message_count = len(getattr(context, 'messages', []))
    
    if message_count == 0:
        return "You are a welcoming assistant. Introduce yourself!"
    elif message_count < 3:
        return "You are a helpful assistant. Be encouraging and detailed."
    else:
        return "You are an experienced assistant. Be concise but thorough."

agent = Agent(
    name="Context Aware Agent", 
    instructions=context_aware
)
def time_based(context: RunContextWrapper, agent: Agent) -> str:
    current_hour = datetime.datetime.now().hour
    
    if 6 <= 23 and 23 < 12:
        return f"You are {agent.name}. Good morning! Be energetic and positive."
    elif 12 <= current_hour < 17:
        return f"You are {agent.name}. Good afternoon! Be focused and productive."
    else:
        return f"You are {agent.name}. Good evening! Be calm and helpful."

agent = Agent(
    name="Time Aware Agent",
    instructions=time_based
)

class StatefulInstructions:
    def __init__(self):
        self.interaction_count = 0
    
    def __call__(self, context: RunContextWrapper, agent: Agent) -> str:
        self.interaction_count += 1
        
        if self.interaction_count == 1:
            return "You are a learning assistant. This is our first interaction - be welcoming!"
        elif self.interaction_count <= 3:
            return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation."
        else:
            return f"You are an experienced assistant. We've had {self.interaction_count} interactions - be efficient."

instruction_gen = StatefulInstructions()

agent = Agent(
    name="Stateful Agent",
    instructions=instruction_gen
)


import asyncio

async def async_instructions(context: RunContextWrapper, agent: Agent) -> str:
    # Simulate fetching data from database
    await asyncio.sleep(0.1)
    current_time = datetime.datetime.now()
    
    return f"""You are {agent.name}, an AI assistant with real-time capabilities.
    Current time: {current_time.strftime('%H:%M')}
    Provide helpful and timely responses."""

agent = Agent(
    name="Async Agent",
    instructions=async_instructions
)

def explore_context(context: RunContextWrapper, agent: Agent) -> str:
    # Access conversation messages
    messages = getattr(context, 'messages', [])
    message_count = len(messages)
    
    # Access user context (if available)
    user_name = getattr(context.context, 'name', 'User')
    
    return f"You are {agent.name}. Talking to {user_name}. Message #{message_count}."

def explore_agent(context: RunContextWrapper, agent: Agent) -> str:
    # Access agent properties
    agent_name = agent.name
    tool_count = len(agent.tools)
    
    return f"You are {agent_name} with {tool_count} tools. Be helpful!"