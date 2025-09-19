from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import operator
from dotenv import load_dotenv
import json
from schemas import RawSchemaSpecs, MetricsSpecs

load_dotenv(override=True)

def load_model(model_name: str):
    with open(f"models/{model_name}/inputs/schema.json", "r") as f:
        schema_data = json.load(f)
        schema = RawSchemaSpecs(**schema_data)
    with open(f"models/{model_name}/inputs/metrics.json", "r") as f:
        metrics_data = json.load(f)
        metrics = MetricsSpecs(**metrics_data)
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
    schema, metrics = load_model("test1")

    # Create prompt
    prompt = (
        f"You are an expert data engineer and architect and your goal is to design a dimensional model "
        f"with facts and dimension tables from a set of raw input tables and target business metrics.\n\n"
        f"You're provided with the raw data schema below:\n\n"
        f"{schema.model_dump_json(indent=2)}\n\n"
        f"And the following metrics to be calculated from the dimensional model:\n\n"
        f"{metrics.model_dump_json(indent=2)}\n\n"
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

# Invoke
messages = [HumanMessage(content="Provide the dimensional model for this data.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()