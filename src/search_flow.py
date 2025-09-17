from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from typing_extensions import TypedDict, Annotated
from typing import Literal
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import operator
from dotenv import load_dotenv
import json

load_dotenv(override=True)

def load_model(model_name: str):
    with open(f"models/{model_name}/inputs/schema.json", "r") as f:
        schema = json.load(f)
    with open(f"models/{model_name}/inputs/metrics.json", "r") as f:
        metrics = json.load(f)
    return schema, metrics

# Define LLM
llm = init_chat_model(
    "gemini-2.0-flash-exp",
    model_provider="google_genai",
    temperature=0
)

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

    
def llm_call(state: dict):
    """Create a dimensional model from the provided schema"""
    
    # Load model input data
    schema_data, metrics_data = load_model("test1")

    # Create prompt
    prompt = (
        f"You are an expert data engineer and architect and your goal is to design a dimensional model "
        f"with facts and dimension tables from a set of raw input tables and target business metrics.\n\n"
        f"You're provided with the raw data schema below:\n\n"
        f"{json.dumps(schema_data, indent=2)}\n\n"
        f"And the following metrics to be calculated from the dimensional model:\n\n"
        f"{json.dumps(metrics_data, indent=2)}\n\n"
        f"Please provide a dimensional model with fact and dimension tables, their columns, and relationships."
        )
    
    # Call LLM
    response = llm.invoke([SystemMessage(content=prompt)] + state["messages"])
    return {
        "messages": [response],
        "llm_calls": state.get('llm_calls', 0) + 1
    }




# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_edge("llm_call", END)

# Compile the agent
agent = agent_builder.compile()


# Show the agent
display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

# Invoke

messages = [HumanMessage(content="Test the tool with input 'Hello World'")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()