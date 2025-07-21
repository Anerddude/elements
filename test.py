import requests

# Define the API endpoint and model
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:1.5b"

# Define your prompt
prompt = "Explain quantum computing in simple terms."

# Send a POST request to Ollama
response = requests.post(
    OLLAMA_API_URL,
    json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False  # Set to True if you want streaming responses
    }
)

# Print the response
if response.status_code == 200:
    print(response.json()["response"])
else:
    print("Error:", response.text)