from setupconfg import config
from agents import Agent , Runner, SQLiteSession

# # What happens automatically:
# session = SQLiteSession("user_123")

# # Turn 1
# result1 = Runner.run_sync(agent, "Hello", session=session)
# # Memory now: [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}]

# # Turn 2
# result2 = Runner.run_sync(agent, "How are you?", session=session)
# # Memory loads previous history + adds new messages
# # Memory now: [previous messages + new user message + new assistant response]

# Create session memory
temp_session = SQLiteSession("my_first_conversation")
persistent_session = SQLiteSession("user_123", "conversations.db")
print("=== First Conversation with Memory ===")

# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Be friendly and remember our conversation.",
)

# Turn 1
result1 = Runner.run_sync(
    agent,
    "Hi! My name is Alex and I love pizza.",
    session=temp_session,
    run_config=config
)
print("Agent:", result1.final_output)

# Turn 2 - Agent should remember your name!
result2 = Runner.run_sync(
    agent,
    "What's my name?",
    session=temp_session,
    run_config=config
)
print("Agent:", result2.final_output)  # Should say "Alex"!

# Turn 3 - Agent should remember you love pizza!
result3 = Runner.run_sync(
    agent,
    "What food do I like?",
    session=temp_session,
    run_config=config
)
print("Agent:", result3.final_output)  # Should mention pizza!

# Use temporary session
result1 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=temp_session,
    run_config=config
)

# Use persistent session
result2 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=persistent_session,
    run_config=config
)

# res = Runner.run(agent,'hi',run_config=config,)