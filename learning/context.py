import asyncio
from pretty_print import print_pretty_json
from dataclasses import dataclass
from agents import Agent, Runner,enable_verbose_stdout_logging
from agents import Agent, function_tool, RunContextWrapper
from setupconfg import config
# enable_verbose_stdout_logging()
@dataclass
class UserContext:
    username: str
    email: str | None = None

@function_tool()
async def search(local_context: RunContextWrapper[UserContext], query: str) -> str:
    import time
    time.sleep(30)  # Simulating a delay for the search operation
    return "No results found."

async def special_prompt(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    # who is user?
    # which agent
    print(f"\nUser: {special_context.context},\n Agent: {agent.name}\n")
    return f"You are a math expert. User: {special_context.context.username}, Agent: {agent.name}. Please assist with math-related queries."

math_agent: Agent = Agent(
    name="Genius",
    instructions=special_prompt,
    tools=[search]
)
# [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

async def call_agent():
    # Call the agent with a specific input
    user_context = UserContext(username="abdullah")

    output = await Runner.run(
        starting_agent=math_agent, 
        input="search for the best math tutor in my area",
        context=user_context,
        run_config=config,
        )
    print(math_agent.get_system_prompt)
    print(math_agent.instructions)
    print_pretty_json(output.raw_responses)
    print(f"\n\nOutput: {output.final_output}\n\n")
    
asyncio.run(call_agent())