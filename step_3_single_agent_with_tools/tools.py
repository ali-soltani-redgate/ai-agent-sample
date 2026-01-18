def calculator(expression: str) -> str:
    """A simple calculator tool that evaluates a mathematical expression."""
    try:
        # WARNING: Using eval can be dangerous if you're evaluating untrusted input.
        # In a real application, consider using a safe math parser library.
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


def search_stub(query: str) -> str:
    # replace later with real search
    return f"Search results for '{query}' (stub)"


def get_tools():
    TOOLS = """
    You can use the following tools:

    1. calculator(expression: str) -> str
    Use for math calculations.

    2. search(query: str) -> str
    Use for factual lookup.

    When you want to use a tool, respond ONLY in JSON:

    {
    "tool": "<tool name>",
    "input": "<tool input>"
    }

    Otherwise, respond normally.
    """
    return TOOLS
