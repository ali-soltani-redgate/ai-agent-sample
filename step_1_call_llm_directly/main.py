

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
user_prompt = input("Enter your prompt: ")
response = llm.invoke(user_prompt)
print(response.content)

