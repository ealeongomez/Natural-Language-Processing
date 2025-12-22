# ====================================================================================
# Libraries
# ====================================================================================

# Basic libraries
import random
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# LangGraph libraries
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model

# OpenAI models
gtp_llm = init_chat_model(model="gpt-4o-mini", temperature=1)

# ====================================================================================
# Class 
# ====================================================================================
class State(MessagesState):
    customer_name: str
    my_age: int

def node_1(state: State):
    history = state["messages"]
    new_state: State = {}
    if state.get("customer_name") is None:
        new_state["customer_name"] = "John Doe"
    else:
        new_state["my_age"] = random.randint(20, 30)
    
    ai_message = gtp_llm.invoke(history)
    new_state["messages"] = [ai_message]

    return new_state

# ====================================================================================
# Create the graph
# ====================================================================================


builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()
