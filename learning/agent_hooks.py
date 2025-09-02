# Imports
import asyncio
import random
from pydantic import BaseModel
from typing import Any
from agents import Agent, RunContextWrapper, AgentHooks, Runner, Tool,function_tool
from setupconfg import config

class CustomAgentHooks(AgentHooks):
    def __init__(self, display_name: str):
        self.event_counter = 0
        self.display_name = display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended with output {output}"
        )

    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {source.name} handed off to {agent.name}"
        )

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}"
        )

    async def on_tool_end(
        self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
    ) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with result {result}"
        )
     
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"📞 SYSTEM: {agent.name} is thinking...")
    
    async def on_llm_end(self, context, agent, response):
        print(f"🧠✨ SYSTEM: {agent.name} finished thinking")

@function_tool
def random_number(max: int) -> int:
    """
    Generate a random number up to the provided maximum.
    """
    return random.randint(0, max)


@function_tool
def multiply_by_two(x: int) -> int:
    """Simple multiplication by two."""
    return x * 2


class FinalResult(BaseModel):
    number: int


multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    hooks=CustomAgentHooks(display_name="Multiply Agent"),

)

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multiply agent.",
    tools=[random_number],
    handoffs=[multiply_agent],
    hooks=CustomAgentHooks(display_name="Start Agent"),


)


async def main() -> None:
    user_input = input("Enter a max number: ")
    await Runner.run(
        start_agent,
        input=f"Generate a random number between 0 and {user_input}.",
        run_config=config,
    )

    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())