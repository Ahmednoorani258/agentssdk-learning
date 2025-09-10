from agents import Agent, Runner, ModelSettings, function_tool, enable_verbose_stdout_logging
from setupconfg import config, model
from pretty_print import print_pretty_json

# start small
# print_pretty_json(enable_verbose_stdout_logging())


lowercase_agent = Agent(
    name="LowerCaser",
    instructions="Convert the input text to lowercase.",
    model = model
)

titlecase_agent = Agent(
    name="TitleCaser",
    instructions="Convert the input text to titlecase.",
)
@function_tool
async def to_titlecase(text: str) -> str:
    return (await Runner.run(titlecase_agent,  input=text,run_config=config)).final_output
    

orchestration_agent = Agent(
    name="Orchestrator",
    instructions="Decide whether to use the LowerCaser or TitleCaser agent based on the input text. If the input text is in all uppercase, use the LowerCaser agent. If the input text is in all lowercase, use the TitleCaser agent. Otherwise, return the input text as is.",
    model= ModelSettings(
        tool_choice="required"
    ),
    tools=[
        lowercase_agent.as_tool(
            tool_name='LowerCaser',
            tool_description='Use this tool to convert text to lowercase. Input should be a string in all uppercase letters.'
        ),
        to_titlecase
    ]
)

async def main():
    res = await Runner.run(orchestration_agent,run_config=config, input="convert this to both lowerand titlecase HELLO WORLD")
    print(res.final_output)
# res = Runner.run_sync(orchestration_agent,run_config=config, input="convert this to both lowerand titlecase HELLO WORLD")
# print(res.final_output)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())