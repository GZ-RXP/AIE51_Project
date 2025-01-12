# First we initialize the model we want to use.
from langchain_openai import ChatOpenAI

base_url = ""
api_key = ""
model = "Qwen2.5-7B-Instruct"
model = ChatOpenAI(base_url=base_url,
            api_key=api_key,
            model=model,
            # max_tokens=512,
            # max_completion_tokens = 2048,
            temperature=0.01,
            top_p=0.3
            )


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool


# @tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")
# @tool
def generate_report():
    """Use this to generate report."""
    return """
    [REPORT] this is a report sample for testing
    Accuracy: 0.9
    Precision: 0.8
    Recall: 0.7
    F1: 0.6
    """
# @tool
def send_via_sms(phone_number: str, message: str):
    """Use this to send a message via sms."""
    print(f"Sending '{message}' to {phone_number} via sms...")
    return f"Sent '{message}' to {phone_number}"

tools = [get_weather,generate_report,send_via_sms]


# Define the graph

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(model, tools=tools, state_modifier="you are a helpful assistant, using the tools to help the user")

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "what is the weather in sf"),("assistant", "it is sunny"),("user", "what about the weather in nyc?")]}
print_stream(graph.stream(inputs, stream_mode="values"))
result = graph.invoke(input= {"messages": [("user", "can you sent a 'hello world' message via sms to my mobile 1234567890?")]})
print(type(result),result["messages"][-1].content)