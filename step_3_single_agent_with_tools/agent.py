import ollama
import json

from tools import get_tools, calculator, search_stub

SYSTEM_PROMPT = f"""
You are a helpful AI agent.
{get_tools()}
"""

def agent_loop(user_input):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    for _ in range(5):  # max steps
        response = ollama.chat(
            model="llama3.2",
            messages=messages
        )

        content = response["message"]["content"]
        print("\nLLM:", content)

        # Try parsing tool call
        try:
            result = tool_call(content)
            messages.append({"role": "assistant", "content": content})
            messages.append({
                "role": "user",
                "content": f"Tool result: {result}"
            })

        except json.JSONDecodeError:
            # Final answer
            return content

    return "Agent stopped (max steps reached)"

def tool_call(content):
    tool_call = json.loads(content)
    tool_name = tool_call["tool"]
    print("Tool requested:", tool_name)
    tool_input = tool_call["input"]
    print("Tool input:", tool_input)

    if tool_name == "calculator":
        result = calculator(tool_input)
    elif tool_name == "search":
        result = search_stub(tool_input)
    else:
        result = "Unknown tool"
    print("Tool result:", result)
    return result

if __name__ == "__main__":
    user_input = input("User prompt: ")
    print(agent_loop(user_input))
   