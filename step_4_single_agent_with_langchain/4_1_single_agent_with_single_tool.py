from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_classic.agents import initialize_agent, AgentType


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


# Local Ollama model
llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


# Create an agent that can call the get_weather tool
agent = initialize_agent(
    tools=[get_weather],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)


# Run the agent with Ollama as the LLM
result = agent.run("what is the weather in sf?")
print("\nFinal answer:", result)


