from agents import Agent,RunHooks, Runner,  function_tool
import random
import time
from datetime import datetime
from setupconfg import config

class DetailedAgentHooks(RunHooks):
    def __init__(self):
        self.start_time = None
        self.llm_calls = 0
        self.tool_calls = 0
    
    async def on_agent_start(self, context, agent):
        self.start_time = time.time()
        self.llm_calls = 0
        self.tool_calls = 0
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"🕘 [{timestamp}] {agent.name} became active")
    
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        self.llm_calls += 1
        print(f"📞 LLM Call #{self.llm_calls}: {agent.name} asking AI for guidance")
        print(f"   Input: {len(input_items)} items to think about")
    
    async def on_llm_end(self, context, agent, response):
        print(f"🧠✨ LLM Call #{self.llm_calls} completed")
        print(f"   AI response length: {len(str(response))} characters")
    
    async def on_tool_start(self, context, agent, tool):
        self.tool_calls += 1
        print(f"🔨 Tool #{self.tool_calls}: {agent.name} using {tool.name}")
    
    async def on_tool_end(self, context, agent, tool, result):
        print(f"✅🔨 Tool #{self.tool_calls} completed")
        print(f"   Result preview: {str(result)[:50]}...")
    
    async def on_handoff(self, context, agent, source):
        print(f"🏃‍♂️➡️🏃‍♀️ {agent.name} received work from {source.name}")
        print(f"   Work is being transferred due to specialization")
    
    async def on_agent_end(self, context, agent, output):
        duration = time.time() - self.start_time if self.start_time else 0
        print(f"✅ {agent.name} FINISHED in {duration:.2f} seconds")
        print(f"📊 Total: {self.llm_calls} AI calls, {self.tool_calls} tool uses")
        print(f"🎯 Final result: {str(output)[:100]}...")




@function_tool("random_number")
def random_number(max: int) -> int:
    """Generate a random number up to the provided max."""
    return random.randint(0, max)


@function_tool("multiply_by_two")
def multiply_by_two(x: int) -> int:
    """Return x times two."""
    return x * 2


multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
)

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multipler agent. give both the addition and multiplication",
    tools=[random_number],
    handoffs=[multiply_agent],
)

hooks = DetailedAgentHooks()

async def main() -> None:
    user_input = input("Enter a max number: ")
    ans = await Runner.run(
        start_agent,
        hooks=hooks,
        input=f"Generate a random number between 0 and {user_input}.",
        run_config=config
    )

    print(ans.final_output)

    print("Done!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())# Use it with your agent

