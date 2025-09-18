from typing import Annotated
from langchain_tavily import TavilySearch
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

"""Initialize the MCP client and load tools"""
client = MultiServerMCPClient(
    {
        "calculus_server": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        },
    }
)

async def load_tools():
    async with client.session("calculus_server") as session:
        tools = await load_mcp_tools(session)

    return tools

async def load_model():
    chat_model = init_chat_model("gpt-4o-mini").bind_tools(await load_tools())

    return chat_model



class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2)
tools = [tool]

#llm = init_chat_model("gpt-4o-mini")
#llm_with_tools = llm.bind_tools(tools)

async def chatbot(state: State):
    model = await load_model()
    return {"messages": [model.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

async def create_tool_node(state: State):
    tools = await load_tools()
    tool_node = ToolNode(tools=tools)

    return tool_node

graph_builder.add_node("tools", create_tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

if __name__ == "__main__":
    response = asyncio.run(
        graph.ainvoke({"messages": ["Search in tavily what is the capital of France"]})
    )
    print(response)