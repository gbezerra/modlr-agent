from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from typing_extensions import TypedDict, Annotated
from typing import Literal
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import operator
from dotenv import load_dotenv

load_dotenv(override=True)

# Define LLM
llm = init_chat_model(
    "gemini-2.0-flash-exp",
    model_provider="google_genai",
    temperature=0
)

# Define and bind tools

@tool
def test_tool(input: str) -> str:
    """A test tool that echoes the input."""
    return f"Echo: {input}"

tools = [test_tool]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

    
def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""
    prompt = "You are a helpful assistant tasked with asking questions."
    response = llm_with_tools.invoke([SystemMessage(content=prompt)] + state["messages"])
    return {
        "messages": [response],
        "llm_calls": state.get('llm_calls', 0) + 1
    }


def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

 # Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"
    # Otherwise, we stop (reply to the user)
    return END


# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent
agent = agent_builder.compile()



# Show the agent
display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

# Invoke

messages = [HumanMessage(content="Test the tool with input 'Hello World'")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()