import requests
import json

# Ollama HTTP API endpoint
ollama_api_endpoint = "http://localhost:11434/api/chat"

class OllamaClient:
    def __init__(self, model: str, base_url: str = ollama_api_endpoint):
        self.model = model
        self.base_url = base_url

    def chat(self, messages: list, stream: bool = False):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream # Set to True for streaming responses
        }
        response = requests.post(self.base_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")


# Example usage
client = OllamaClient(model="llama3.2")
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
response = client.chat(messages)

# Print the full response (for debugging)
print("Full response:")
print(json.dumps(response, indent=2))

# Print just the answer
print("\nAnswer:")
print(response["message"]["content"])
