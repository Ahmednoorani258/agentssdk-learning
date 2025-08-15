from dataclasses import dataclass, field, replace
from typing import List
# shallow copy 
# deep copy

import copy

list1 = [[1, 2], [3, 4]]
# shallow_copy = copy.copy(list1)  # Shallow copy

# shallow_copy[0].append(99)

# print("Original:", list1)   # Both changed!
# print("Copy:    ", shallow_copy)



deep_copy = copy.deepcopy(list1)
deep_copy[0].append(100)

# print("Original:", list1)   # Unchanged
# print("Copy:    ", deep_copy)




@dataclass
class Agent:
    name: str
    instructions: str
    tools: List[str] = field(default_factory=list)

agent1 = Agent(name="Original", instructions="Follow the plan", tools=["Hammer", "Wrench"])
agent2 = replace(agent1, name="Cloned")  # Shallow copy

# print(agent1.tools is agent2.tools)  # True → same list object
# agent2.tools.append("Screwdriver")
# print("Agent1 tools:", agent1.tools)  # Uh-oh, also changed!


agent3 = replace(agent1, name="Safe Clone", tools=agent1.tools.copy())
agent3.tools.append("Pliers")

# print("Agent1 tools:", agent1.tools)  # unchanged
# print("Agent3 tools:", agent3.tools)



# agent4 = copy.deepcopy(agent1)
# agent4.tools.append("Drill")

# print("Agent1 tools:", agent1.tools)  # unchanged
# print("Agent4 tools:", agent4.tools)




@dataclass
class Agent:
    name: str
    instructions: str
    tools: List[str] = field(default_factory=list)

    def clone(self, **changes):
        return replace(self, **changes)

# Example usage
a = Agent("A", "Test", ["tool1"])
b = a.clone(name="B", tools=a.tools.copy())

b.tools.append("tool2")
print(a.tools)
print(b.tools)

print(a.tools is b.tools)  # False → different lists