from __future__ import annotations
import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from pretty_print import print_pretty_json
from setupconfg import config

"""
This example shows how to use guardrails.

Guardrails are checks that run in parallel to the agent's execution.
They can be used to do things like:
- Check if input messages are off-topic
- Check that input messages don't violate any policies
- Take over control of the agent's execution if an unexpected input is detected

In this example, we'll setup an input guardrail that trips if the user is asking to do math homework.
If the guardrail trips, we'll respond with a refusal message.
"""


### 1. An agent-based guardrail that is triggered if the user is asking to do math homework
class CustomerSupportOutput(BaseModel):
    reasoning: str
    is_not_customer_support_query: bool


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check that user only ask about customer support issues and its related queries.",
    output_type=CustomerSupportOutput,
)


@input_guardrail
async def math_guardrail(
    context: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """This is an input guardrail function, which happens to call an agent to check if the input
    is only related to customer support reltated queries.
    """
    result = await Runner.run(guardrail_agent, input, context=context.context,run_config=config)
    final_output = result.final_output_as(CustomerSupportOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_not_customer_support_query,
    )

### 2. The run loop

async def main():
    agent = Agent(
        name="Customer support agent",
        instructions="You are a customer support agent. You help customers with their questions.",
        input_guardrails=[math_guardrail],
    )

    input_data: list[TResponseInputItem] = []

    while True:
        user_input = input("Enter a message: ")
        input_data.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        try:
            result = await Runner.run(agent, input_data,run_config=config)
            print(result.final_output)
            print("\n\n<<<<<<<<<<<<__________________Input Guardrail Result_____________________________>>>>>>>>>>\n\n")
            print_pretty_json(result.input_guardrail_results)
            print("\n\n<<<<<<<<<<<<__________________NewItems_____________________________>>>>>>>>>>\n\n")
            print_pretty_json(result.new_items)
            print("\n\n<<<<<<<<<<<<__________________Raw Response_____________________________>>>>>>>>>>\n\n")
            print_pretty_json(result.raw_responses)
            print("\n\n<<<<<<<<<<<<__________________history_____________________________>>>>>>>>>>\n\n")
            print_pretty_json(result.to_input_list())
            # If the guardrail didn't trigger, we use the result as the input for the next run
            input_data = result.to_input_list()
        except InputGuardrailTripwireTriggered as e:
            # If the guardrail triggered, we instead add a refusal message to the input
            message = "Sorry, I can't help you with your math homework."
            print(message)
            input_data.append(
                {
                    "role": "assistant",
                    "content": message,
                }
            )
            print("\n\n<<<<<<<<<<<<__________________Input Data_____________________________>>>>>>>>>>\n\n")
            print_pretty_json(input_data)
            print("\n\n<<<<<<<<<<<<__________________agent_____________________________>>>>>>>>>>\n\n")
            print_pretty_json(agent)
            print("\n\n<<<<<<<<<<<<__________________Error_____________________________>>>>>>>>>>\n\n")
            print_pretty_json(e)
    # Sample run:
    # Enter a message: What's the capital of California?
    # The capital of California is Sacramento.
    # Enter a message: Can you help me solve for x: 2x + 5 = 11
    # Sorry, I can't help you with your math homework.


if __name__ == "__main__":
    asyncio.run(main())
