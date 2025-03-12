from langchain_ollama import ChatOllama
from dotenv import load_dotenv

# Load environment variables from .env file (if needed)
load_dotenv()

llm = ChatOllama(model="deepseek-r1:1.5b")  # Use the appropriate model name for your Ollama setup
llm.invoke("Hello, world!")

