import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_community.chat_models import ChatOllama
from IPython.display import Image, display

# Load environment variables from .env file (if needed)
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the Ollama chat model
llm = ChatOllama(model="deepseek-r1:1.5b")  # Use the appropriate model name for your Ollama setup

graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Build the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# Visualize the graph (optional)
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
    img = Image(graph.get_graph().draw_mermaid_png())
    img_file_path = "graph.png"
    with open(img_file_path, "wb") as f:
        f.write(img.data)
    print(f"Graph image saved to {img_file_path}")
    os.system(f"open {img_file_path}")  # Adjust for your OS if needed
except Exception as e:
    print(f"An error occurred: {e}")
    pass

# Chat loop
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break