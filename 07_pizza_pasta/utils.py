from langchain_core.runnables import RunnableConfig
import uuid
from langgraph.types import interrupt, Command
from agent import State, graph
import asyncio
import langgraph.types

config = RunnableConfig({"configurable": {"thread_id": uuid.uuid4()}})

async def run_agent(message: str, comand: Command | None = None):
    yielded_response = ""
    stream_message = State({
        "messages": [message], 
        "user_response": "", 
        "chatbot_response": ""
    }) if comand is None else comand
    
    async for async_stream_response in graph.astream(stream_message, config):
        interrupt_condition = ("__interrupt__" in async_stream_response) and (type(async_stream_response["__interrupt__"]) == tuple) and (len(async_stream_response["__interrupt__"]) == 1) and (type(async_stream_response["__interrupt__"][0]) == langgraph.types.Interrupt)
        if interrupt_condition:
            yielded_response += async_stream_response["__interrupt__"][0].value
            yielded_response += "\n \n"

        for node_name, node_data in async_stream_response.items():
            if isinstance(node_data, dict) and "chatbot_response" in node_data:
                messages = node_data["chatbot_response"]
                yielded_response += str(messages) + "\n \n"

        yield yielded_response
        

async def run_agent_with_stop(message:str, history: list):
    """Example of how to consume yielded responses from outside"""

    state = await graph.aget_state(config)
    next_node = state.next

    # Check if graph is in a stopped state (no next nodes to execute)
    is_not_stopped = not next_node or len(next_node) == 0

    if is_not_stopped:
        async for yielded_data in run_agent(message):
            yield yielded_data

    else:
        command = Command(resume=message)
        async for yielded_data in run_agent("", command):
            yield yielded_data

async def main():
    async for response in run_agent_with_stop("Hello", []):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())