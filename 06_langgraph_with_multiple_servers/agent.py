from typing import Annotated, Literal
import uuid
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import InMemorySaver
import asyncio
import langgraph.types
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt, Command
from langchain_mcp_adapters.client import MultiServerMCPClient

class State(TypedDict):
    messages: Annotated[list, add_messages]
    accepted_tool_call: Literal["y", "n", None]

mcp_server = "mcp_server"
client = MultiServerMCPClient(
    {
        mcp_server: {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        },
    }
)  # type: ignore


# Define agent nodes
async def chatbot(state: State):
    # Load tools within a managed session
    async with client.session(mcp_server) as session:
        tools = await load_mcp_tools(session)

        # Create model with tools
        model = init_chat_model("gpt-4o-mini").bind_tools(tools)
        response = await model.ainvoke(state["messages"])
        return {"messages": [response]}

async def tools(state: State):
    async with client.session(mcp_server) as session:
        tools = await load_mcp_tools(session)
        tool_node = ToolNode(tools=tools)
        return await tool_node.ainvoke(state)
    
# Edges
def tools_condition(
        state: State,
        messages_key: str = "messages"
    ) -> Literal["tool_calling_permission_node", "__end__"]:

    messages = state[messages_key]
    ai_message = messages[-1]

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tool_calling_permission_node"
    return "__end__"

def tool_calling_permission_edge(state: State) -> Literal["reject_tool_call_node","tools"]:
    if state["accepted_tool_call"] == "y":
        return "tools"
    
    return "reject_tool_call_node"
    


def reject_tool_call_node(state: State):
    # Is returning the reject, this should be splitted later
    return {"messages": {
                'role': 'tool',
                'name': state["messages"][-1].tool_calls[0]["name"],
                'tool_call_id': state["messages"][-1].tool_calls[0]["id"],
                'content': f'tool call rejected: {state["accepted_tool_call"]}'
            }}

def tool_calling_permission_node(state: State):
    user_input = interrupt('Accept tool calling (y/n)?')
    return {"accepted_tool_call": user_input}

# Build graph
graph_builder = StateGraph(State)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_conditional_edges("chatbot", tools_condition)

graph_builder.add_node("tool_calling_permission_node", tool_calling_permission_node)

graph_builder.add_node("reject_tool_call_node", reject_tool_call_node)
graph_builder.add_node("tools", tools)

graph_builder.add_conditional_edges("tool_calling_permission_node", tool_calling_permission_edge)

graph_builder.add_edge("reject_tool_call_node", "chatbot")
graph_builder.add_edge("tools", "chatbot")

checkpointer = InMemorySaver()
graph = graph_builder.compile(
    checkpointer=checkpointer
)

# The compiled graph is something like this
# https://mermaid.live/edit#pako:eNqNUsGO2yAQ_RU0vSSS7brYJDFZ5dJ8wp66rixig01LwMK43W2Uf19MUrerbKOeYJj33rwZ5gS1aThQiOO41LXRQra01AgJZX7WHbMuRAjVo_3BKVJSc2ZLHeCtZX2HHvfbUpeuqgbn4VW1eHrod3P08LHffV1SSoW0g5uAXtUdjFtcz-X05oxRVc2Ul2-rntujHAZpdKW9ucW9ZGBb_o3XrppxF9q7r3O1IcgOy4t1rpvZeLjPthW7uJ4bQnG8Q1fv27_6QXHiE1f6beJeE9t_NnFT7J7MpdC7Ov_JDSOZscNtq34aw54L1HDBRuWQkErRDwKLVIho2o2447LtHP2U4DeE8PsBHpue1dK90PQNYJrzVe4gDitRQwStlQ1QZ0cewdH7ZVMIp2khS3AdP_ISqL82zH4vodRnz-mZ_mLM8TfNmrHtgAqmBh-NfcMc30vmN_cPxP8Yt5_NqB1QEhSAnuAZKN7kCcnX6Wa9zrKc4E0EL0ALkmRFvkpxSoocF8U5gl-hYpqQFVmnKc5wscGrjJDzK5IDMEw

config = RunnableConfig({"configurable": {"thread_id": uuid.uuid4()}})

async def run_agent(message: str, comand: Command | None = None):
    yielded_response = ""
    stream_message = State({"messages": [message], "accepted_tool_call": None}) if comand is None else comand
    async for async_stream_response in graph.astream(stream_message, config):
        if "chatbot" in async_stream_response:
            tool_calls = async_stream_response["chatbot"]["messages"][0].tool_calls
            if len(tool_calls):
                yielded_response += f"Tool calls: {tool_calls}"
                yielded_response += "\n \n"

            content = async_stream_response["chatbot"]["messages"][0].content
            if content:
                yielded_response += f"Content: {content}"
                yielded_response += "\n \n"


        if 'tools' in async_stream_response:
            yielded_response += f"Tool responses: {list(map(lambda row: {row.name: row.content}, async_stream_response['tools']['messages']))}"
            yielded_response += "\n \n"

        interrupt_condition = ("__interrupt__" in async_stream_response) and (type(async_stream_response["__interrupt__"]) == tuple) and (len(async_stream_response["__interrupt__"]) == 1) and (type(async_stream_response["__interrupt__"][0]) == langgraph.types.Interrupt)
        if interrupt_condition:
            yielded_response += async_stream_response["__interrupt__"][0].value
            yielded_response += "\n \n"

        if "tool_calling_permission_node" in async_stream_response:
            yielded_response += f"You responded: {async_stream_response['tool_calling_permission_node']['accepted_tool_call']}"
            yielded_response += "\n \n"

        if "reject_tool_call_node" in async_stream_response:
            yielded_response += f"Rejected tool calling: {async_stream_response['reject_tool_call_node']['messages']['name']}"
            yielded_response += "\n \n"


        yield yielded_response

async def run_agent_with_stop(message:str, history: list):
    """Example of how to consume yielded responses from outside"""
    
    next_node = (await graph.aget_state(config)).next
    is_human_accepting_tool_call = next_node != ('tool_calling_permission_node',)
    if is_human_accepting_tool_call:
        async for yielded_data in run_agent(message):
            yield yielded_data

    else:
        command = Command(resume=message)
        async for yielded_data in run_agent("", command):
            yield yielded_data




async def consume_agent_responses():
    """Example of how to consume yielded responses from outside"""
    print("Starting agent execution...")
    async for yielded_data in run_agent("Use the tools to calculate 5+7."):
        print("---")
        print(f"{yielded_data}")
        print("---")


    command = Command(resume="n")
    async for yielded_data in graph.astream(command, config):
        print("---")
        print(f"{yielded_data}")
        print("---")


    print("Agent execution completed!")



#if __name__ == "__main__":
# {"messages":"Use the tools to calculate 5+7."}
#    asyncio.run(consume_agent_responses())
