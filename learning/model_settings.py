from setupconfg import config
from agents import Agent, Runner,ModelSettings, function_tool,enable_verbose_stdout_logging
from openai.types import Reasoning 

from pretty_print import print_pretty_json
enable_verbose_stdout_logging()

# <<<<<<<<<<<<<___________Model Setting_________________________>>>>>>>>>>>>>>>>>>>>>>>>>

# Low temperature (0.1) = Very focused, consistent answers
agent_focused = Agent(
    name="Math Tutor",
    instructions="You are a precise math tutor.",
    model_settings=ModelSettings(temperature=0.1)
)

# High temperature (0.9) = More creative, varied responses
agent_creative = Agent(
    name="Story Writer",
    instructions="You are a creative storyteller.",
    model_settings=ModelSettings(temperature=2.1)
)

# <<<<<<<<<<<<<___________Tool Choice_________________________>>>>>>>>>>>>>>>>>>>>>>>>>
@function_tool
def calculator(input: str) -> str:
    """A simple calculator tool."""
    try:
        # Evaluate the expression safely
        result = eval(input)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"
@function_tool
def weather_tool(input: str) -> str:
    return "The weather is sunny today."

# Agent can decide when to use tools (default)
agent_auto = Agent(
    name="Smart Assistant",
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="auto")
)

# Agent MUST use a tool (even if not needed)
agent_required = Agent(
    name="Tool User",
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="required"),
    # reset_tool_choice=False
)

# Agent CANNOT use tools (chat only)
agent_no_tools = Agent(
    name="Chat Only",
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="none")
)





# <<<<<<<<<<<<<___________Max Tokens_________________________>>>>>>>>>>>>>>>>>>>>>>>>>
# Short, concise responses
agent_brief = Agent(
    name="Brief Assistant",
    model_settings=ModelSettings(max_tokens="")
)

# Longer, detailed responses
agent_detailed = Agent(
    name="Detailed Assistant", 
    model_settings=ModelSettings(max_tokens=1000)
)

# <<<<<<<<<<<<<___________Advance (Parallel calls)_____________________>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<___________Advance (Parallel calls)_____________________>>>>>>>>>>>>>>>>>>>>>>>>>
# Agent can use multiple tools at once
@function_tool
def translator(input: str) -> str:
    return "The translation is: " + input
parallel_agent = Agent(
    name="Multi-Tasker",
    tools=[weather_tool, calculator, translator],
    model_settings=ModelSettings(
        tool_choice="auto",
        parallel_tool_calls=True  # Use multiple tools simultaneously
    )
)

# Agent uses tools one at a time
sequential_agent = Agent(
    name="One-at-a-Time",
    tools=[weather_tool, calculator, translator],
    model_settings=ModelSettings(
        tool_choice="auto",
        parallel_tool_calls=False  # Use tools one by one
    )
)

# <<<<<<<<<<<<<___________Advance (TOP_P)_____________________>>>>>>>>>>>>>>>>>>>>>>>>>

# More focused vocabulary
focused_agent = Agent(
    name="Focused",
    model_settings=ModelSettings(
        # top_p=1,              # Use only top 30% of vocabulary
        # frequency_penalty=0.5,   # Avoid repeating words
        # presence_penalty=0.3,     # Encourage new topics
        # max_tokens=100
    ),
    
)


# <<<<<<<<<<<<<___________model setting( to_json_dict(), resolve(), truncation, reasoning, metadata, store, include_usage, response_include, extra_query, extra_body, extra_headers, extra_args,  )
# base_Settings = ModelSettings(
#     max_tokens=50,
# )

# check_agent = Agent(
#     name="Check Agent",
#     instructions="You are a checking agent.",
#     model_settings=base_Settings.resolve(
#         ModelSettings(
#         temperature=0.5,
#         max_tokens=100,
#         )
#     )   
# )
# _____________________>>>>>>>>>>>>>>>>>>>>>>>>>


check_agent = Agent(
    name="Check Agent",
    instructions="think about the query and provide a detailed response.",  
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="high")
    )
    
)

def main():
    uinput = input("Enter your query: ")
    res = Runner.run_sync(check_agent,uinput,run_config=config,)
    print_pretty_json(check_agent.model_settings.to_json_dict())
    # print_pretty_json(check_agent.model_settings)
    print(res.final_output)
    
if __name__ == "__main__":
    main()