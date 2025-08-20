import sqlite3
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_core.messages import HumanMessage

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, MessagesState, StateGraph

from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

load_dotenv()

db = sqlite3.connect("../database/conversation_history.db", check_same_thread=False)

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

prompt_text = """You are a language tutor. You will be engaging in spoken conversations with a person who wants to learn {language}. 
Please make sure to engage in interesting conversations and bounce off of what they are saying.
Make sure that your vocabulary matches their level and use proper grammar. Be natural.
Additionally, it is important that you do not include any symbols such as asteriks in your responses. 
Your responses should of paramount important be conversational. That means on the shorter end and casual. 
Answer all conversations in {language}"""


prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", prompt_text),
        MessagesPlaceholder(variable_name="messages")
    ]
)

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

# Define a new graph
workflow = StateGraph(state_schema=State)


# Define the function that calls the model
def call_model(state: State): 
    # Create the prompt with all conversation history
    prompt = prompt_template.invoke({"language": state["language"], "messages": state["messages"]})
    
    # Invoke the model with the full conversation context
    response = model.invoke(prompt)
    
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = SqliteSaver(db)
app = workflow.compile(checkpointer=memory)

def converse(query: str, language: str = "English", config: dict = {"configurable": {"thread_id": "default"}}):
    """ Chat with the tutor with conversation memory.
    Args:
        query: The user's message
        language: The language to respond in
        thread_id: Unique identifier for the conversation thread
    """
    input_messages = [HumanMessage(content=query)]
    return app.stream(
        {"messages": input_messages, "language": language}, config, stream_mode="messages",
    )

#test
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "Default"}}
    for chunk, _ in converse("Hello there. What is my name?"):
        print(chunk.content)
    for chunk, _ in converse("Very good!"):
        print(chunk.content)
    
    

