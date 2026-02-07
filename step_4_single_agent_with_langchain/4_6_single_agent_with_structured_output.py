from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_classic.agents import initialize_agent, AgentType
import re
from pydantic import BaseModel, Field

# Define a structured response model for weather


class WeatherResponse(BaseModel):
    city: str = Field(description="The city name")
    temperature: str = Field(description="The temperature")
    condition: str = Field(
        description="Weather condition (e.g., sunny, cloudy, rainy)")
    humidity: str = Field(description="Humidity level")


# Set up local Ollama model
# Stronger model with vision capabilities
llm = ChatOllama(
    model="llama3.2-vision:11b",  # The size of the model is 7.8GB!
    temperature=0,
)

# Create a structured LLM that automatically outputs WeatherResponse objects
structured_llm = llm.with_structured_output(WeatherResponse)


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city in JSON format."""
    messages = [
        ("system", "You are a weather assistant. Provide accurate weather information."),
        ("human", f"Provide weather details for {city}")
    ]
    result = structured_llm.invoke(messages)
    # Convert Pydantic model to dict then string for the agent
    return str(result.dict())


@tool
def add_numbers(query: str) -> int:
    """Add two numbers when the user explicitly asks for arithmetic, e.g. 'What is 5 + 7?'.

    Note: we deliberately implement this as a pure Python function instead of an LLMChain,
    because simple arithmetic is exact, fast, and cheap to compute directly. Using an LLM
    (via LLMChain) here would be slower, more expensive, and could introduce hallucinated
    results, so it's a poor fit for this kind of deterministic logic.

    Do NOT use this for weather or non-math questions.
    """
    numbers = re.findall(r"-?\d+", query)
    if len(numbers) < 2:
        # Fail gracefully so the agent can continue reasoning instead of crashing
        return 0
    a, b = map(int, numbers[:2])
    return a + b


tools = [get_weather, add_numbers]


# Create an agent that can call the tools (including the chain-backed weather tool)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,  # Stop after a small number of tool steps.
    early_stopping_method="generate",
)


# Run the agent with Ollama as the LLM
result = agent.invoke("what is the weather in sf?")
print("\nFinal answer:", result)
'''
Note:
The max iterations is set to 3, which could be too low for some complex queries. If the agent fails to find the answer within 3 iterations, it will stop and return the best guess. You can increase this number if you want the agent to have more chances to find the correct answer, but be mindful of potential infinite loops or excessive tool calls.
For example, I got the following output with max_iterations=3:
Final answer: {'input': 'what is the weather in sf?', 'output': 'Thought: I need to return a final answer based on the previous steps. However, the previous steps did not provide a final answer. The get_weather action was successful, but the subsequent actions were not valid tools.\n\nAction: get_weather\nAction Input: sf'}
The agent successfully called the get_weather tool and got a response, but it did not have enough iterations to process that response and return a final answer.
'''

result = agent.invoke("What is 5 + 7?")
print("\nFinal answer:", result)
