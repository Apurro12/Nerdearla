
from typing import Annotated, cast
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import asyncio
from langgraph.types import interrupt, Command
from typing import Literal
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_response: str
    chatbot_response: str

graph_builder = StateGraph(State)

async def do_you_wanna_eat(state: State):
    user_input = None
    while user_input not in ['y', 'n']:
        user_input = interrupt('Do you want to eat something? y/n:')

    return {"messages": user_input, "user_response": user_input}

async def do_you_wanna_eat_edge(state: State) -> Literal[END, "cook_options"]:
    if state["user_response"] == "y":
        return "cook_options"
    
    return END

async def cook_options(state: State):
    user_input = None
    cook_options = ['Pizza', 'Tarta', 'Pasta']
    while user_input not in cook_options:
        user_input = interrupt(f'Choose an option: {"/".join(cook_options)}:')

    return {"messages": user_input, "user_response": user_input}

async def cook_options_edge(state: State) -> Literal['Pizza', 'Tarta', 'Pasta']:
    assert state["user_response"] in ['Pizza', 'Tarta', 'Pasta']
    user_choice = state["user_response"]
    assert user_choice in ['Pizza', 'Tarta', 'Pasta']
    return user_choice # type: ignore

async def pizza_node(state: State):
    chat_response = "Go to supermarket and buy an already made pizza!"
    return {"messages": chat_response, "chatbot_response": chat_response}

async def tarta_node(state: State):
    chat_response = "you need eggs, flour, sugar and butter. Go to supermarket and buy them!"
    return {"messages": chat_response, "chatbot_response": chat_response}

async def ask_for_italian_granma(state: State):
    user_input = None
    while user_input not in ['y', 'n']:
        user_input = interrupt('Do you have an Italian Grandma? y/n:')

    return {"messages": user_input, "user_response": user_input}


async def pasta_node(state: State):
    chat_response = "Ask your Italian Grandma for the recipe!"
    return {"messages": chat_response, "chatbot_response": chat_response}

async def ask_for_italian_granma_edge(state: State) -> Literal['Pasta_Alone', 'Pasta_Youtube']:
    if state["user_response"] == "y":
        return "Pasta_Youtube"
    return "Pasta_Alone"

async def Pasta_Alone(state: State):
    chat_response = "Sorry to hear that, I cannot help you, search in Youtube for that recipe!"
    return {"messages": chat_response, "chatbot_response": chat_response}

graph_builder.add_edge(START, "do_you_wanna_eat")
graph_builder.add_node("do_you_wanna_eat", do_you_wanna_eat)
graph_builder.add_conditional_edges("do_you_wanna_eat", do_you_wanna_eat_edge)
graph_builder.add_node("cook_options", cook_options)



graph_builder.add_conditional_edges("cook_options", cook_options_edge)

graph_builder.add_node("Pizza", pizza_node)
graph_builder.add_node("Tarta", tarta_node)
graph_builder.add_node("Pasta", ask_for_italian_granma)

graph_builder.add_conditional_edges("Pasta", ask_for_italian_granma_edge)

graph_builder.add_node("Pasta_Alone", Pasta_Alone)
graph_builder.add_node("Pasta_Youtube", pasta_node)



graph_builder.add_edge("Pizza", END)
graph_builder.add_edge("Tarta", END)
graph_builder.add_edge("Pasta_Alone", END)
graph_builder.add_edge("Pasta_Youtube", END)

graph = graph_builder.compile(
    checkpointer=InMemorySaver()
)