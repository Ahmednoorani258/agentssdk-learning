from agents import Agent, Runner,handoff, RunContextWrapper, function_tool, enable_verbose_stdout_logging
from setupconfg import config
from agents.extensions import handoff_filters
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pretty_print import print_pretty_json
from pydantic import BaseModel
import asyncio

# enable_verbose_stdout_logging()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  part 1  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EscalationData(BaseModel):
    reason: str
    order_id: str

async def on_escalation(ctx: RunContextWrapper, input_data: EscalationData):
    print(f"Escalating order {input_data.order_id} because: {input_data.reason}")


escalation_agent = Agent(
    name="Escalation agent"    
)


escalation_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_escalation,
    input_filter=handoff_filters.remove_all_tools,
    input_type=EscalationData, # The LLM must provide this data
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Your primary job is to diagnose the user's problem.
    If it is about billing, handoff to the Billing Agent.
    If it is about refunds, handoff to the Refund Agent.""",
    handoffs=[handoff(escalation_handoff,is_enabled=True)],
)

async def main():
    res = await Runner.run(triage_agent, "I need a refund for order #123.",  run_config=config )
    return res

res = asyncio.run(main())
print_pretty_json(res.last_agent)   
print_pretty_json(res.final_output)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  part 2  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



faq_agent = Agent(name="FAQ agent")

faq_handoff = handoff(
    agent=faq_agent,
    # This removes all tool call/output history for the next agent.
    input_filter=handoff_filters.remove_all_tools,
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  part 3  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# triage_agent = Agent(
#     name="Triage Agent",
#     instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
#     Your primary job is to diagnose the user's problem.
#     If it is about billing, handoff to the Billing Agent.
#     If it is about refunds, handoff to the Refund Agent."""
# )

# async def main():
#     # Turn 1: Triage hands off to the Refunds specialist
#     result1 = await Runner.run(triage_agent, "I need a refund for order #123.", run_config=config)
#     print(f"Reply from: {result1.last_agent.name}")
#     print(f"Message: {result1.final_output}")

#     # The user replies: "Thanks, how long will it take?"
#     follow_up_message = {"role": "user", "content": "Thanks, how long will it take?"}

#     # --- PATTERN 2: CONTINUE WITH THE SPECIALIST ---
#     # Get the agent that answered last (e.g., the Refunds Agent)
#     specialist = result1.last_agent
#     # Create the input for the next turn, including all prior history
#     follow_up_input = result1.to_input_list() + [follow_up_message]

#     # Run the next turn starting directly with the specialist
#     result2 = await Runner.run(specialist, follow_up_input , run_config=config)
#     print(f"Reply from: {result2.last_agent.name}")
#     print(f"Message: {result2.final_output}")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  part 4  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import asyncio

# # --- Define the data for our "briefing note" ---
# class HandoffData(BaseModel):
#     summary: str

# # --- Define our specialist agents ---
# billing_agent = Agent(name="Billing Agent", instructions="Handle billing questions.")
# technical_agent = Agent(name="Technical Support Agent", instructions="Troubleshoot technical issues.")

# # --- Define our on_handoff callback ---
# def log_the_handoff(ctx: RunContextWrapper, input_data: HandoffData):
#     print(f"\n[SYSTEM: Handoff initiated. Briefing: '{input_data.summary}']\n")

# # --- TODO 1: Create the advanced handoffs ---

# # Create a handoff to `billing_agent`.
# # - Override the tool name to be "transfer_to_billing".
# # - Use the `log_the_handoff` callback.
# # - Require `HandoffData` as input.
# to_billing_handoff = handoff(
#     agent=billing_agent,
#     tool_name_override="transfer_to_billing",
#     on_handoff=log_the_handoff,
#     input_type=HandoffData,
# )

# # Create a handoff to `technical_agent`.
# # - Use the `log_the_handoff` callback.
# # - Require `HandoffData` as input.
# # - Add an input filter: `handoff_filters.remove_all_tools`.
# to_technical_handoff = handoff(
#     agent=technical_agent,
#     on_handoff=log_the_handoff,
#     input_type=HandoffData,
#     input_filter=handoff_filters.remove_all_tools,
# )

# @function_tool
# def diagnose() -> str:
#     """A dummy diagnosis tool."""
#     return "The user's payment failed."

# # --- Triage Agent uses the handoffs ---
# triage_agent = Agent(
#     name="Triage Agent",
#     instructions="First, use the 'diagnose' tool. Then, based on the issue, handoff to the correct specialist with a summary.",
#     tools=[
#         diagnose,
#     ],
#     handoffs=[to_billing_handoff, to_technical_handoff],
# )


# async def main():
#     print("--- Running Scenario: Billing Issue ---")
#     result = await Runner.run(triage_agent, "My payment won't go through.", run_config=config)
#     print(f"Final Reply From: {result.last_agent.name}")
#     print(f"Final Message: {result.final_output}")

# asyncio.run(main())