import json

from langchain_core.tools import tool

from utils.schedule import get_schedule


@tool
def think(thought: str) -> str:
    """Use the tool to think about something.
           This is perfect to start your workflow.
           It will not collect new information or take any actions, but just append the thought to the log and return the result.
           Use it when complex reasoning or some cache memory or a scratchpad is needed.


           :param thought: A thought to think about and log.
           :return: The full log of thoughts and the new thought.
    """
    return thought


@tool
def read_schedule() -> str:
    """Use this tool to read the PyData schedule about which a user will ask questions.

    Returns:
        str: The PyData Amsterdam 2025 schedule data as JSON text.
    """
    schedule = get_schedule(out_format="dict")
    return json.dumps(schedule, indent=4)
