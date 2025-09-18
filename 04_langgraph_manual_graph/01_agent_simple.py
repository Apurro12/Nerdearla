from typing import Annotated
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

class State(TypedDict):
    messages: Annotated[list, add_messages]

async def create_agent():
    """Create and run the agent with proper MCP session management"""
    client = MultiServerMCPClient(
        {
            "calculus_server": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    # Load tools within a managed session
    async with client.session("calculus_server") as session:
        tools = await load_mcp_tools(session)

        # Create model with tools
        model = init_chat_model("gpt-4o-mini").bind_tools(tools)

        # Define agent nodes
        async def chatbot(state: State):
            return {"messages": [model.invoke(state["messages"])]}

        async def tools_node(state: State):
            tool_node = ToolNode(tools=tools)
            return await tool_node.ainvoke(state)

        # Build graph
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_node("tools", tools_node)
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")
        graph = graph_builder.compile()

        # Run the agent
        response = await graph.ainvoke({"messages": ["Use the tools to calculate 5+7."]})
        return response

if __name__ == "__main__":
    response = asyncio.run(create_agent())
    print(response)