from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_milvus import Milvus

from langchain_core.documents import Document

from langchain_core.documents import Document
from typing_extensions import List, TypedDict

from langchain_core.tools import tool

from langgraph.graph import MessagesState, StateGraph

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import ToolNode

from uuid import uuid4

load_dotenv()

PROMPT = """ You are a language tutor analyzing student responses. Please focus on providing tips on grammar, vocabulary, propriety of language, and the such. 
Make sure to be positive and positive.

You MUST use the retrieve tool to get the student's conversation history before providing any analysis.

IMPORTANT: You have access to a retrieve tool that can fetch conversation data for any user_id. You MUST call this tool first to get the student's data.

Steps:
1. Use the retrieve tool with the user_id to get conversation history
2. Analyze the retrieved conversations
3. Provide specific feedback with examples from their conversations
4. Highlight key mistakes and provide constructive feedback
5. Suggest improvement resources

Do not provide any analysis without first retrieving the conversation data using the tool.

The user_id is provided in the state. Use the retrieve tool immediately.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

URI = "../database/vector_database.db"

vector_store = Milvus(
    embedding_function = embeddings, 
    connection_args={"uri": URI},
    index_params={"index_type": "FLAT", "metric_type": "L2"},
    partition_key_field="namespace",
)

def add_document(page_content: str, user_id: str):
    doc = [Document(
        page_content=page_content,
        metadata={"namespace": user_id}
    )]
    uuids = [str(uuid4())]
    vector_store.add_documents(documents = doc, ids=uuids)

def remove_document(uuid: str):
    vector_store.delete(ids=[uuid])

class State(TypedDict):
    messages: List
    question: str
    context: List[Document]
    answer: str
    user_id: str

graph_builder = StateGraph(State)

@tool
def retrieve(query: str, user_id: str):
    """Retrieve conversation history for a specific user_id. Use this tool to get the student's conversation data before analyzing their performance."""
    try:
        retrieved_docs = vector_store.similarity_search(query, k=5, search_kwargs={"expr": f'namespace == "{user_id}"'})
        if not retrieved_docs:
            return f"No conversation history found for user {user_id}"
        
        serialized = "\n\n".join(
            (f"Conversation {i+1}:\n{doc.page_content}")
            for i, doc in enumerate(retrieved_docs)
        )
        return f"Retrieved {len(retrieved_docs)} conversations for user {user_id}:\n\n{serialized}"
    except Exception as e:
        return f"Error retrieving data: {str(e)}"

# Step 1: Generate an AIMessage that may include a tool-call to be sent.
def query_or_respond(state: State):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    
    # Ensure user_id is passed to tool calls
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            if 'args' in tool_call:
                tool_call['args']['user_id'] = state['user_id']
    
    return {"messages": [response]}


# Step 2: Execute the retrieval.
tools = ToolNode([retrieve])


# Step 3: Generate a response using the retrieved content.
def generate(state: State):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if hasattr(message, 'type') and message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    if tool_messages:
        docs_content = "\n\n".join(doc.content for doc in tool_messages)
    else:
        docs_content = "No conversation data retrieved."
    
    system_message_content = (
        "You are a language tutor. You are analyzing your students' work to help them improve their language skills."
        "Focus on grammar."
        "Your job is to find the mistakes they make the most often and categorize them precisely."
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Make sure that you think hard and long and provide the best answer you can"
        "\n\n"
        f"{docs_content}"
    )
    
    # Get conversation messages
    conversation_messages = []
    for message in state["messages"]:
        if hasattr(message, 'type'):
            if message.type in ("human", "system"):
                conversation_messages.append(message)
            elif message.type == "ai" and not hasattr(message, 'tool_calls'):
                conversation_messages.append(message)
    
    if not conversation_messages:
        conversation_messages = [HumanMessage(content="Please analyze the student's conversation data.")]
    
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    return {"messages": [response]}

from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition

graph_builder.add_node(query_or_respond)
graph_builder.add_node(tools)
graph_builder.add_node(generate)

graph_builder.set_entry_point("query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"},
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", END)

analyzer = graph_builder.compile()

def create_report(user_id: str):
    input_messages = [HumanMessage(content=PROMPT)]
    return analyzer.invoke(
        {
            "messages": input_messages, 
            "user_id": user_id,
            "question": "",
            "context": [],
            "answer": ""
        }
    )["messages"][-1].content


#test
if __name__ == "__main__":
    print(create_report("1"))