

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

class LlmClient():
    """A simple wrapper around the ChatAnthropic LLM client"""
    def __init__(self, model: str = "claude-3-haiku-20240307", temperature: int = 0):
        self.llm = ChatAnthropic(model=model, temperature=temperature)

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt) 


if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    llm = LlmClient()
    response = llm.invoke(user_prompt)
    print(response.content)
