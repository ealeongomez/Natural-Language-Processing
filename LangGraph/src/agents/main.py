# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# Initialize the model
model = ChatOpenAI(model="gpt-4o-mini")

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent (commented out - use this when running directly)
# agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
# )