from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.chains import LLMChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import re

# Set up local Ollama model
# Stronger model with vision capabilities
llm = ChatOllama(
    model="llama3.2-vision:11b",  # The size of the model is 7.8GB!
    temperature=0,
)


# Define a prompt template for the weather tool
weather_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a weather assistant. Answer very briefly."
        ),
        HumanMessagePromptTemplate.from_template(
            "City: {city}\nWeather:"
        ),
    ]
)

# ----- Weather chain wrapped as a tool -----
weather_chain = LLMChain(llm=llm, prompt=weather_prompt)


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return weather_chain.run(city=city)


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
    max_iterations=5,  # Stop after a small number of tool steps.
    early_stopping_method="generate",
)


# Run the agent with Ollama as the LLM
result = agent.invoke("what is the weather in sf?")
print("\nFinal answer:", result)

result = agent.invoke("What is 5 + 7?")
print("\nFinal answer:", result)
