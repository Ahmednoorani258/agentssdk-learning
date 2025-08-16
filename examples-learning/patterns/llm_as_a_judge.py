
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal
from setupconfg import config
from agents import Agent, ItemHelpers, Runner, TResponseInputItem, trace
from pretty_print import print_pretty_json

"""
This example shows the LLM as a judge pattern. The first agent generates an outline for a story.
The second agent judges the outline and provides feedback. We loop until the judge is satisfied
with the outline.
"""

story_outline_generator = Agent(
    name="story_outline_generator",
    instructions=(
        "You generate a very short story outline based on the user's input."
        "If there is any feedback provided, use it to improve the outline."
    ),
)


@dataclass
class EvaluationFeedback:
    feedback: str
    score: Literal["pass", "needs_improvement", "fail"]


evaluator = Agent[None](
    name="evaluator",
    instructions=(
        "You evaluate a story outline and decide if it's good enough."
        "If it's not good enough, you provide feedback on what needs to be improved."
        "Never give it a pass on the first try. After 2 attempts, you can give it a pass if story outline is good enough - do not go for perfection"
    ),
    output_type=EvaluationFeedback,
)


async def main() -> None:
    msg = "funny"
    input_items: list[TResponseInputItem] = ItemHelpers.input_to_new_input_list(msg)

    latest_outline: str | None = None

    # We'll run the entire workflow in a single trace
    with trace("LLM as a judge"):
        while True:
            story_outline_result = await Runner.run(
                story_outline_generator,
                input_items,
                run_config=config
            )

            input_items = story_outline_result.to_input_list()
           
            latest_outline = ItemHelpers.text_message_outputs(story_outline_result.new_items)
            
            # print_pretty_json(story_outline_result.new_items)
            # for item in story_outline_result.new_items:
            #     last_content = ItemHelpers.extract_last_content(item.raw_item)
            #     print("extract_last_content:", last_content)
            
            # for item in story_outline_result.new_items:
            #     if hasattr(item, "raw_item"):
            #         text_only = ItemHelpers.text_message_output(item)
            #         print("text_message_output:", text_only)
            
            # After generator run
            print("\n--- Using ItemHelpers methods ---")
            for item in story_outline_result.new_items:
                print("extract_last_content:", ItemHelpers.extract_last_content(item.raw_item))
                print("extract_last_text:", ItemHelpers.extract_last_text(item.raw_item))
                print("text_message_output:", ItemHelpers.text_message_output(item))

            print("text_message_outputs:", ItemHelpers.text_message_outputs(story_outline_result.new_items))


           
            evaluator_result = await Runner.run(evaluator, input_items,run_config=config)
            result: EvaluationFeedback = evaluator_result.final_output

            print(f"Evaluator score: {result.score}")

            if result.score == "pass":
                print("Story outline is good enough, exiting.")
                break

            print("Re-running with feedback")

            input_items.append({"content": f"Feedback: {result.feedback}", "role": "user"})

    print(f"Final story outline: {latest_outline}")


if __name__ == "__main__":
    asyncio.run(main())
