from langgraph.prebuilt import create_react_agent
from tools_langchain import multiply
from langchain_core.messages import AIMessage, ToolMessage

agent = create_react_agent(
    "openai:gpt-5-2025-08-07",
    tools = [multiply],
)

user_input = "Use the available tools to calculate 12 multiplied by 13?"
for j in agent.stream(input = {"messages": [{"role": "user", "content": user_input}]}):
    
    if "agent" in j:
        tool_calls = j["agent"]["messages"][0].tool_calls
        if len(tool_calls):
            print("Tool calls:", tool_calls)

        content = j["agent"]["messages"][0].content
        if content:
            print("Content:", content)

    if "tools" in j:
        print("Tool responses:", list(map(lambda row: {row.name: row.content}, j["tools"]["messages"])))