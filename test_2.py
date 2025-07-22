from ollama import chat
from ollama import ChatResponse

elements_names = "Taylor Swift and Water"


response_2: ChatResponse = chat(model='phi3:3.8b', messages=[
  {
    'role': 'user',
    'content': f"""
    You are a creative entities combiner. 
    Generate a name for the combination of the entities included in this prompt. 
    Your response should only include the generated name.
    Elements : {elements_names}.
    new element :

    """,
  },
])

print(response_2.message.content)