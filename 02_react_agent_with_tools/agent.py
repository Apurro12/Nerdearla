from langgraph.prebuilt import create_react_agent
from tools_langchain import multiply
import time 

agent = create_react_agent(
    "openai:gpt-4.1-nano",
    tools = [multiply],
)

def chat(message, history):
    #"Use the available tools to calculate 12 multiplied by 13"

    response = ""
    for j in agent.stream(input = {"messages": [{"role": "user", "content": message}]}):
        time.sleep(1)
        
        if "agent" in j:
            tool_calls = j["agent"]["messages"][0].tool_calls
            if len(tool_calls):
                response += f"Tool calls: {tool_calls}"
                response += "\n"

            content = j["agent"]["messages"][0].content
            if content:
                response += f"Content: {content}\n"
                response += "\n"

        if "tools" in j:
            response += f"Tool responses: {list(map(lambda row: {row.name: row.content}, j['tools']['messages']))}"
            response += "\n"

    return response



async def chat_async(message, history):
    #"Use the available tools to calculate 12 multiplied by 13"

    response = ""
    async for j in agent.astream(input = {"messages": [{"role": "user", "content": message}]}):
        time.sleep(1)
        
        if "agent" in j:
            tool_calls = j["agent"]["messages"][0].tool_calls
            if len(tool_calls):
                response += f"Tool calls: {tool_calls}"
                response += "\n \n"

            content = j["agent"]["messages"][0].content
            if content:
                response += f"Content: {content}"
                response += "\n \n"

        if "tools" in j:
            response += f"Tool responses: {list(map(lambda row: {row.name: row.content}, j['tools']['messages']))}"
            response += "\n \n"

        yield response