import json

from langchain_core.tools import tool

from utils.datetime import current_datetime
from utils.schedule import get_descriptions
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


@tool
def get_current_datetime() -> str:
    """Get the current CET date and time.

    Returns:
        str: The current date and time in format YYYY-MM-DD HH:MM:SS
    """
    return current_datetime()


@tool
def get_event_details(event_id: str) -> str:
    """Get detailed information about a specific event.

    Args:
        event_id: The ID of the event to get details for.

    Returns:
        str: The detailed description of the event.
    """
    descriptions = get_descriptions(out_format="dict")
    return json.dumps(descriptions.get(event_id, {}), indent=4)
