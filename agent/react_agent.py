from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from agent.tools import get_current_datetime
from agent.tools import get_event_details
from agent.tools import get_speaker_bio
from agent.tools import read_schedule
from agent.tools import think
from utils.prompt import build_prompt


def build_graph():
    tools = [
        think,
        read_schedule,
        get_event_details,
        get_speaker_bio,
        get_current_datetime,
    ]
    agent = create_react_agent(
        ChatOpenAI(model="gpt-4o-mini"),
        tools,
        checkpointer=MemorySaver(),
        prompt=SystemMessage(build_prompt(tools)),
    )
    return agent
