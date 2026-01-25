from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_classic.agents import initialize_agent, AgentType
import re

# Local Ollama model
# Stronger model with vision capabilities
llm = ChatOllama(
    model="llama3.2-vision:11b",  # The size of the model is 7.8GB!
    temperature=0,
)


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
# This tool should only have one input as per LangChain's tool definition requirements. It can't take multiple parameters.
def add_numbers(query: str) -> int:
    """Add two numbers when the user explicitly asks for arithmetic, e.g. 'What is 5 + 7?'. Do NOT use this for weather or non-math questions."""
    numbers = re.findall(r"-?\d+", query)
    if len(numbers) < 2:
        # Fail gracefully so the agent can continue reasoning instead of crashing
        return 0
    a, b = map(int, numbers[:2])
    return a + b


# Create an agent that can call the get_weather tool
agent = initialize_agent(
    tools=[get_weather, add_numbers],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5, # Stop after a small number of tool steps. If we don't this, the stronger model may keep going indefinitely and never stop.
    early_stopping_method="generate",
)


# Run the agent with Ollama as the LLM
result = agent.invoke("what is the weather in sf?")
print("\nFinal answer:", result)

result = agent.invoke("What is 5 + 7?")
print("\nFinal answer:", result)
