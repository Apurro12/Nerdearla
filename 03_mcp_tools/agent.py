from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "calculus_server": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        },
    }
)

async def create_agent():
    agent = create_react_agent(
        "openai:gpt-4.1-nano",
        tools = await client.get_tools(),
    )

    return agent


async def chat_async(message, history):
    #"Use the available tools to calculate 12 multiplied by 13"
    response = ""

    agent = await create_agent()
    async for j in agent.astream(input = {"messages": [{"role": "user", "content": message}]}):
        
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